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
    date = typer.prompt("Enter the limit date (YYYY-MM-DD). Only accounts created *after* this date will be included:")
    filtered = df[df['birthdate'] > date]
    filtered.to_csv("data/" + output, index=False)
    
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
 
    df["birthdate"] = pd.to_datetime(df["birthdate"], errors="coerce")
    b = df["birthdate"]
    as_of = pd.Timestamp.today().normalize()

    try:
        y = int(str(years).strip())
    except Exception:
        typer.echo(f"Valor inválido para la edad: {years}. Debe ser un entero.")
        raise typer.Exit(code=1)

    # Edad exacta en años cumplidos (vectorizada)
    has_had_birthday = (b.dt.month < as_of.month) | (
        (b.dt.month == as_of.month) & (b.dt.day <= as_of.day)
    )
    has_had_birthday = has_had_birthday.fillna(False)

    age_years_int = (as_of.year - b.dt.year) - (~has_had_birthday).astype(int)

    # Filtra: fechas válidas, edad no negativa (por si hay fechas futuras) y edad == y
    mask_valid = b.notna()
    mask_nonnegative = age_years_int >= 0
    filtered = df.loc[mask_valid & mask_nonnegative & (age_years_int == y)].copy()

    filtered.to_csv("data/" + output, index=False)
    print("File saved as: data/" + output)