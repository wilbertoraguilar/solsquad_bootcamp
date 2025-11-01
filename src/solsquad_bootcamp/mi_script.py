from __future__ import annotations

import os
from typing import Any

import typer
import pandas as pd

def read_csv_to_df(path: str) -> Any:
    if not os.path.isabs(path):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        path = os.path.join(repo_root, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at: {path}")

    return pd.read_csv(path)


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

    # Convierto la columna cumple al tipo fecha
    df["birthdate"] = pd.to_datetime(df["birthdate"])

    # TAREA #3: Cuentas de individuos con 3 años o menos
    ## Guardo la fecha de hace 3 años
    fecha_limite = pd.Timestamp.today() - pd.DateOffset(years=3)
    print("Filtrando desde:", fecha_limite)

    ## Guardo las filas de individuos con 3 años de edad o menos.
    df_filtrado = df[df["birthdate"] > fecha_limite]
    
    output = typer.prompt("Extracted file name")
    print("File saved as: data/" + output)


def filtered(path: str = "data/mock-data.csv") -> None:
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
    output = typer.prompt("Extracted file name")
    years = typer.prompt("Maximum age") # Parámetro: edad umbral (puede ser entero o decimal)
