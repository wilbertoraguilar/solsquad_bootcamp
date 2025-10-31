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
    output = typer.prompt("Extracted file name")
    df.to_csv("data/" + output, index=False)
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
    df['birthdate'] = pd.to_datetime(df['birthdate'], errors='coerce') 
    b = df["birthdate"]

    # Fecha de referencia (hoy, normalizada a 00:00)
    as_of = pd.Timestamp.today().normalize()

    try:
        y = float(str(years).strip())
    except Exception:
        typer.echo(f"Valor de 'Maximum age' inválido: {years}")
        raise typer.Exit(code=1)
    
    # Filtrado según entero vs decimal
    if float(y).is_integer():
        # Edad en años cumplidos (precisa al día) usando vectorización
        has_had_birthday = (b.dt.month < as_of.month) | (
            (b.dt.month == as_of.month) & (b.dt.day <= as_of.day)
        )
        # Para NaT, has_had_birthday será NaN -> rellena a False para que no reste 1
        has_had_birthday = has_had_birthday.fillna(False)

        age_years_int = (as_of.year - b.dt.year) - (~has_had_birthday).astype(int)
        # Descarta filas con birthdate inválida
        mask_valid = b.notna()
        filtered = df.loc[mask_valid & (age_years_int < int(y))].copy()
    else:
        # Edad en años (decimal) usando 365.2425 días/año
        age_years_float = (as_of - b) / pd.Timedelta(days=365.2425)
        # Descarta NaT
        mask_valid = b.notna()
        filtered = df.loc[mask_valid & (age_years_float < y)].copy()


    filtered.to_csv("data/" + output, index=False)
    print("File saved as: data/" + output)


 
