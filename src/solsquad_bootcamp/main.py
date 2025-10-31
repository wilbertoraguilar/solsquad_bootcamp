from __future__ import annotations
import os
import datetime
from typing import Any

import typer
import pandas as pd


# === 1️⃣ Definición de la función para leer el CSV ===
def read_csv_to_df(path: str) -> Any:
    if not os.path.isabs(path):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        path = os.path.join(repo_root, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at: {path}")

    return pd.read_csv(path)


# === 2️⃣ Función principal (usa la anterior) ===
def main(path: str = "data/mock-data.csv") -> None:
    try:
        df = read_csv_to_df(path)
    except Exception as exc:
        typer.echo(f"Error loading CSV: {exc}")
        raise typer.Exit(code=1)

    typer.echo(f"Loaded '{path}': {len(df)} rows x {len(df.columns)} cols")
    typer.echo("First 5 rows:")
    try:
        typer.echo(df.head(n=5).to_string(index=False))
    except Exception:
        typer.echo(str(df.head()))

    # === FILTRO: cuentas con menos de 3 años ===
    df["birthdate"] = pd.to_datetime(df["birthdate"], errors="coerce")
    today = datetime.datetime.today()
    three_years_ago = today.replace(year=today.year - 3)
    df = df[df["birthdate"] > three_years_ago]
    typer.echo(f"Filtered accounts less than 3 years old: {len(df)} rows")

    # === Guardar resultado ===
    output = typer.prompt("Extracted file name (e.g. filtered_3years.csv)")
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/" + output, index=False)
    print("✅ File saved as: data/" + output)

