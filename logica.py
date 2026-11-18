"""Funciones simples del tutor. Solo se utilizan bibliotecas de Python."""
import csv
import json
from pathlib import Path


def leer_json(ruta, valor_inicial):
    ruta = Path(ruta)
    if not ruta.exists():
        return valor_inicial
    with ruta.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(ruta, datos):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def cargar_preguntas(ruta):
    with open(ruta, encoding="utf-8", newline="") as archivo:
        preguntas = list(csv.DictReader(archivo))
    if not preguntas:
        raise ValueError("No hay preguntas en el archivo CSV.")
    for pregunta in preguntas:
        requeridos = ["id", "tema", "nivel", "pregunta", "a", "b", "c", "correcta", "explicacion"]
        if any(not pregunta.get(campo) for campo in requeridos):
            raise ValueError("Hay una pregunta incompleta en el CSV.")
        if pregunta["correcta"].upper() not in ("A", "B", "C"):
            raise ValueError("Las respuestas deben ser A, B o C.")
    if len({p["id"] for p in preguntas}) != len(preguntas):
        raise ValueError("Los identificadores de preguntas deben ser únicos.")
    return preguntas


def resultados_tema(historial, tema):
    intentos = [r for r in historial if r["tema"] == tema]
    aciertos = sum(1 for r in intentos if r["acierto"])
    return {"intentos": len(intentos), "aciertos": aciertos,
            "porcentaje": round(100 * aciertos / len(intentos)) if intentos else 0}


def recomendar_tema(preguntas, historial):
    """Primero explora temas no evaluados; después trabaja el de menor porcentaje."""
    temas = list(dict.fromkeys(p["tema"] for p in preguntas))
    sin_evaluar = [tema for tema in temas if not resultados_tema(historial, tema)["intentos"]]
    if sin_evaluar:
        return sin_evaluar[0]
    return min(temas, key=lambda tema: (resultados_tema(historial, tema)["porcentaje"],
                                        resultados_tema(historial, tema)["intentos"]))


def elegir_pregunta(preguntas, historial, configuracion):
    """Selecciona tema según progreso y dificultad según desempeño por tema."""
    tema = recomendar_tema(preguntas, historial)
    avance = resultados_tema(historial, tema)
    nivel = "reto" if (avance["intentos"] >= configuracion["intentos_para_reto"] and
                       avance["porcentaje"] >= configuracion["porcentaje_para_reto"]) else "basico"
    candidatas = [p for p in preguntas if p["tema"] == tema and p["nivel"] == nivel]
    if not candidatas:
        candidatas = [p for p in preguntas if p["tema"] == tema]
    usadas = {respuesta["id_pregunta"] for respuesta in historial}
    pendientes = [p for p in candidatas if p["id"] not in usadas]
    return (pendientes or candidatas)[0]


def registrar_respuesta(estudiantes, nombre, pregunta, opcion):
    opcion = opcion.upper()
    if opcion not in ("A", "B", "C"):
        raise ValueError("Debes elegir A, B o C.")
    estudiantes.setdefault(nombre, [])
    acierto = opcion == pregunta["correcta"].upper()
    estudiantes[nombre].append({"id_pregunta": pregunta["id"], "tema": pregunta["tema"],
                                "respuesta": opcion, "acierto": acierto})
    return acierto


def resumen_estudiante(historial):
    intentos = len(historial)
    aciertos = sum(1 for item in historial if item["acierto"])
    return {"intentos": intentos, "aciertos": aciertos,
            "porcentaje": round(100 * aciertos / intentos) if intentos else 0}
