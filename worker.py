import pandas as pd
from datetime import datetime, timedelta
import requests

WEBHOOK = "https://hooks.slack.com/services/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"
TOLERANCIA_MIN = 60

# leer archivos
fichadas = pd.read_csv("fichadas.csv")
calendario = pd.read_csv("calendario.csv")

ahora = datetime.now()
hoy_str = ahora.strftime("%-d/%-m/%Y")

# filtrar fichadas de hoy
fichadas_hoy = fichadas[
    (fichadas["Fecha"] == hoy_str) &
    (fichadas["Tipo"] == "In")
]

presentes = set(fichadas_hoy["Legajo"])

ausentes = []

for _, row in calendario.iterrows():
    legajo = row["legajo"]
    nombre = row["Colaborador"]
    hora_str = row["horario"]

    hora_inicio = datetime.strptime(hora_str, "%H:%M")
    hora_inicio = hora_inicio.replace(
        year=ahora.year,
        month=ahora.month,
        day=ahora.day
    )

    limite = hora_inicio + timedelta(minutes=TOLERANCIA_MIN)

    if ahora > limite and legajo not in presentes:
        ausentes.append((nombre, hora_str))

mensaje = "📊 Ausentes:\n\n"

for nombre, horario in ausentes:
    mensaje += f"- {nombre} (entrada {horario})\n"

mensaje += f"\nTotal: {len(ausentes)}"

requests.post(WEBHOOK, json={"text": mensaje})
