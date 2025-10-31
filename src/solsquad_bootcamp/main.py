from __future__ import annotations

import os
from typing import Any

import typer
import pandas as pd
import numpy as np

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

    # La fecha en formato 'YYYY-MM-DD' porque los datos base están
    # en ese formato y será más fácil procesarlos
    fecha_input = input("Introduzca una fecha en formato 'YYYY-MM-DD': ")

    # Se transforma el String en dato tipo fecha
    fecha_input = pd.to_datetime(fecha_input)

    '''
        Filtrado para el caso 1.
        Para calcular que sean menores de 3 años he calculado la diferencia en dias entre
        la fecha de hoy y la de creación de cuenta y la he dividido entre 365.25 para sacar 
        la difrencia de años entre una y otra 

        hoy = pd.Timestamp('today').normalize() #Normalize para que no coja la hora/minuto/día
        filtered_1 = df[ ((hoy - pd.to_datetime(df['birthdate'])) / np.timedelta64(1, 'D')) / 365.25 < 3 ]
    '''
    filtered_2 = df[ pd.to_datetime(df['birthdate']) > fecha_input]
    filtered_2.to_csv("data/" + output, index=False)
    
    print("File saved as: data/" + output)
