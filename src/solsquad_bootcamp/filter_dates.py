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

    
    def filter_by_birthdate(df, mode='after'):
        #Comprobamos el modo de filtrado de la función
        if    mode==0 or str(mode).strip().lower()=='after':  mode=0
        elif  mode==1 or str(mode).strip().lower()=='before': mode=1
        else: 
            typer.echo("Not a valid input")
            return None

        #Obtenemos la fecha y la mostramos para confirmar que se ha interpretado bien
        given_date = pd.to_datetime(typer.prompt(f"Date {'after' if mode==0 else 'before'} which accounts where created: "))
        typer.echo(f"Date selected: {given_date}")
        
        #Obtenemos la máscara correspondiente
        if mode==0: mask = pd.to_datetime(df['birthdate'], format='%Y-%m-%d') > given_date
        else:       mask = pd.to_datetime(df['birthdate'], format='%Y-%m-%d') < given_date

        return df[mask]
    
    
    df = filter_by_birthdate(df, mode='after')

    output = typer.prompt("Extracted file name")
    df.to_csv("data/" + output, index=False)
    print("File saved as: data/" + output)