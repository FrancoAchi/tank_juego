import os 
import json

def cargar_puntajes():
    if os.path.exists("puntajes.json"):
        with open("puntajes.json", "r") as file:
            return json.load(file)
    else:
        return []

def guardar_puntajes(puntajes):
    with open("puntajes.json", "w") as file:
        json.dump(puntajes, file, indent=2)

