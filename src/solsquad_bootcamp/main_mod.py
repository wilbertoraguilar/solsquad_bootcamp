from __future__ import annotations

import os
from typing import Any
from datetime import datetime

import typer
import pandas as pd

def read_csv_to_df(path: str) -> Any:
    if not os.path.isabs(path):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        path = os.path.join(repo_root, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at: {path}")

    return pd.read_csv(path)

def calculate_age(birthdate: str) -> int:
    try:
        birth_date = pd.to_datetime(birthdate, errors="coerce")
        today = pd.Timestamp(datetime.today().date())
        if pd.isnull(birth_date):
            return None
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        return age
    except Exception:
        return None

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
    
    df["age"] = df["birthdate"].apply(calculate_age)

    try:
        age = typer.prompt("Enter age to filter by", type=int)
        filtered_df = df[df["age"] == age]
        typer.echo(f"Filtered {len(filtered_df)} rows with age = {age}")

        if filtered_df.empty:
            typer.echo("No rows match the given age. Exiting.")
            raise typer.Exit(code=0)
    except Exception as e:
        typer.echo(f"Error filtering by age: {e}")
        raise typer.Exit(code=1)

    
    output = typer.prompt("Extracted file name")
    filtered_df.to_csv("data/" + output, index=False)
    print("File saved as: data/" + output)
