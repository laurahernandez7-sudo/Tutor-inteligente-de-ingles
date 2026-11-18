"""Ejecutar: python -m unittest discover -s pruebas -v"""
import tempfile
import unittest
from pathlib import Path

from logica import (cargar_preguntas, elegir_pregunta, guardar_json, leer_json,
                    recomendar_tema, registrar_respuesta, resultados_tema,
                    resumen_estudiante)


class PruebasTutor(unittest.TestCase):
    def setUp(self):
        self.preguntas = [
            {"id": "1", "tema": "To be", "nivel": "basico", "correcta": "A"},
            {"id": "2", "tema": "To be", "nivel": "reto", "correcta": "B"},
            {"id": "3", "tema": "Articles", "nivel": "basico", "correcta": "C"},
            {"id": "4", "tema": "Articles", "nivel": "reto", "correcta": "B"},
        ]
        self.configuracion = {"intentos_para_reto": 2, "porcentaje_para_reto": 75}

    def test_inicia_por_un_tema_no_evaluado(self):
        self.assertEqual(recomendar_tema(self.preguntas, []), "To be")

    def test_cambia_al_tema_sin_evaluar(self):
        datos = {"Ana": []}
        registrar_respuesta(datos, "Ana", self.preguntas[0], "A")
        self.assertEqual(recomendar_tema(self.preguntas, datos["Ana"]), "Articles")

    def test_refuerza_el_tema_con_mas_errores(self):
        datos = {"Ana": []}
        registrar_respuesta(datos, "Ana", self.preguntas[0], "B")
        registrar_respuesta(datos, "Ana", self.preguntas[2], "C")
        self.assertEqual(recomendar_tema(self.preguntas, datos["Ana"]), "To be")

    def test_sube_a_reto_por_desempeno(self):
        datos = {"Ana": []}
        registrar_respuesta(datos, "Ana", self.preguntas[0], "A")
        registrar_respuesta(datos, "Ana", self.preguntas[0], "A")
        registrar_respuesta(datos, "Ana", self.preguntas[2], "C")
        registrar_respuesta(datos, "Ana", self.preguntas[2], "C")
        pregunta = elegir_pregunta(self.preguntas, datos["Ana"], self.configuracion)
        self.assertEqual(pregunta["nivel"], "reto")

    def test_registra_errores_y_aciertos(self):
        datos = {}
        self.assertFalse(registrar_respuesta(datos, "Ana", self.preguntas[0], "B"))
        self.assertTrue(registrar_respuesta(datos, "Ana", self.preguntas[0], "A"))
        self.assertEqual(resumen_estudiante(datos["Ana"]), {"intentos": 2, "aciertos": 1, "porcentaje": 50})

    def test_estadistica_por_tema(self):
        datos = {"Ana": []}
        registrar_respuesta(datos, "Ana", self.preguntas[0], "B")
        self.assertEqual(resultados_tema(datos["Ana"], "To be")["porcentaje"], 0)

    def test_guarda_y_lee_json(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "progreso.json"
            guardar_json(ruta, {"Ana": [{"acierto": True}]})
            self.assertTrue(leer_json(ruta, {})["Ana"][0]["acierto"])

    def test_lee_preguntas_reales(self):
        ruta = Path(__file__).resolve().parents[1] / "datos" / "preguntas.csv"
        preguntas = cargar_preguntas(ruta)
        self.assertEqual(len(preguntas), 32)
        self.assertEqual(len({p["tema"] for p in preguntas}), 4)


if __name__ == "__main__":
    unittest.main()
