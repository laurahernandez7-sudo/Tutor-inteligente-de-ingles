"""Tutor de Inglés Personalizado. Ejecuta: python app.py"""
import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from logica import (cargar_preguntas, elegir_pregunta, guardar_json, leer_json,
                    recomendar_tema, registrar_respuesta, resultados_tema,
                    resumen_estudiante, estimar_conocimiento, validar_configuracion)


def iniciar():
    carpeta = Path(__file__).resolve().parent
    configuracion = leer_json(carpeta / "configuracion.json", {})
    validar_configuracion(configuracion)
    preguntas = cargar_preguntas(carpeta / "datos" / "preguntas.csv")
    lecciones = leer_json(carpeta / "datos" / "lecciones.json", {})
    ruta_estudiantes = carpeta / "datos" / "estudiantes.json"
    estudiantes = leer_json(ruta_estudiantes, {})

    ventana = tk.Tk()
    ventana.title("Tutor de Inglés Personalizado | Inglés A1")
    ventana.geometry("920x650")
    ventana.minsize(760, 560)
    ventana.configure(padx=18, pady=14)

    nombre_actual = tk.StringVar()
    nombre_entrada = tk.StringVar()
    seleccion_tema = tk.StringVar()
    respuesta = tk.StringVar()
    mensaje = tk.StringVar(value="Escribe tu nombre para comenzar.")
    pregunta_actual = [None]
    preguntas_sesion = [0]

    ttk.Label(ventana, text="Tutor de Inglés Personalizado", font=("Arial", 19, "bold")).pack(anchor="w")
    ttk.Label(ventana, text="Mini aula virtual con BKT: contenidos, evaluación personalizada y progreso | Nivel A1").pack(anchor="w", pady=(2, 12))
    acceso = ttk.Frame(ventana)
    acceso.pack(fill="x", pady=4)
    ttk.Label(acceso, text="Estudiante:").pack(side="left")
    ttk.Entry(acceso, textvariable=nombre_entrada, width=32).pack(side="left", padx=8)
    estado = ttk.Label(acceso, textvariable=nombre_actual)
    estado.pack(side="right")
    pestanas = ttk.Notebook(ventana)
    pestanas.pack(expand=True, fill="both", pady=12)
    inicio_tab = ttk.Frame(pestanas, padding=18)
    clases_tab = ttk.Frame(pestanas, padding=18)
    prueba_tab = ttk.Frame(pestanas, padding=18)
    progreso_tab = ttk.Frame(pestanas, padding=18)
    docente_tab = ttk.Frame(pestanas, padding=18)
    for texto, marco in [("Inicio", inicio_tab), ("Lecciones", clases_tab),
                         ("Quiz adaptativo", prueba_tab), ("Mi progreso", progreso_tab),
                         ("Vista docente", docente_tab)]:
        pestanas.add(marco, text=texto)

    ttk.Label(inicio_tab, text="Bienvenido al aula de inglés A1", font=("Arial", 15, "bold")).pack(anchor="w", pady=8)
    ttk.Label(inicio_tab, text="1. Ingresa tu nombre.  2. Estudia una lección.\n"
                                     "3. Responde el quiz.  4. Revisa la recomendación y tu progreso.",
              justify="left", font=("Arial", 12)).pack(anchor="w", pady=10)
    recomendacion = ttk.Label(inicio_tab, text="", wraplength=650, font=("Arial", 12))
    recomendacion.pack(anchor="w", pady=15)

    ttk.Label(clases_tab, text="Contenido de aprendizaje", font=("Arial", 14, "bold")).pack(anchor="w")
    selector = ttk.Combobox(clases_tab, textvariable=seleccion_tema, values=list(lecciones), state="readonly", width=36)
    selector.pack(anchor="w", pady=12)
    if lecciones:
        selector.current(0)
    texto_leccion = tk.Text(clases_tab, height=18, wrap="word", font=("Arial", 12), padx=10, pady=10)
    texto_leccion.pack(fill="both", expand=True)
    texto_leccion.config(state="disabled")

    ttk.Label(prueba_tab, text="Evaluación personalizada", font=("Arial", 14, "bold")).pack(anchor="w")
    indicacion = ttk.Label(prueba_tab, text="Ingresa tu nombre y abre esta pestaña para comenzar automáticamente.")
    indicacion.pack(anchor="w", pady=8)
    enunciado = ttk.Label(prueba_tab, text="", font=("Arial", 14), wraplength=780)
    enunciado.pack(anchor="w", pady=14)
    opciones = []
    for letra in ("A", "B", "C"):
        boton = ttk.Radiobutton(prueba_tab, text=letra, variable=respuesta, value=letra)
        boton.pack(anchor="w", pady=6)
        opciones.append(boton)
    resultado = ttk.Label(prueba_tab, text="", wraplength=740, font=("Arial", 11))
    resultado.pack(anchor="w", pady=14)
    acciones = ttk.Frame(prueba_tab)
    acciones.pack(anchor="w", pady=6)

    ttk.Label(progreso_tab, text="Resultados personales", font=("Arial", 14, "bold")).pack(anchor="w")
    resumen_texto = ttk.Label(progreso_tab, text="")
    resumen_texto.pack(anchor="w", pady=10)
    tabla = ttk.Treeview(progreso_tab, columns=("tema", "intentos", "aciertos", "porcentaje", "dominio"), show="headings", height=7)
    for columna, etiqueta, ancho in [("tema", "Tema", 250), ("intentos", "Intentos", 100),
                                    ("aciertos", "Aciertos", 100), ("porcentaje", "% aciertos", 110), ("dominio", "Dominio BKT", 130)]:
        tabla.heading(columna, text=etiqueta)
        tabla.column(columna, width=ancho)
    tabla.pack(fill="x", pady=6)
    proxima = ttk.Label(progreso_tab, text="")
    proxima.pack(anchor="w", pady=10)

    ttk.Label(docente_tab, text="Resumen local de estudiantes", font=("Arial", 14, "bold")).pack(anchor="w")
    ttk.Label(docente_tab, text="Prototipo educativo: esta vista no tiene contraseña ni debe usarse con datos sensibles.",
              wraplength=700).pack(anchor="w", pady=8)
    tabla_docente = ttk.Treeview(docente_tab, columns=("nombre", "intentos", "aciertos", "porcentaje"), show="headings", height=10)
    for columna, etiqueta in [("nombre", "Estudiante"), ("intentos", "Intentos"),
                              ("aciertos", "Aciertos"), ("porcentaje", "% aciertos")]:
        tabla_docente.heading(columna, text=etiqueta)
        tabla_docente.column(columna, width=150)
    tabla_docente.pack(fill="both", expand=True, pady=6)

    def refrescar_progreso():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for fila in tabla_docente.get_children():
            tabla_docente.delete(fila)
        for nombre, historial in sorted(estudiantes.items()):
            r = resumen_estudiante(historial)
            tabla_docente.insert("", "end", values=(nombre, r["intentos"], r["aciertos"], r["porcentaje"]))
        nombre = nombre_actual.get()
        if not nombre:
            return
        historial = estudiantes.get(nombre, [])
        r = resumen_estudiante(historial)
        resumen_texto.config(text=f"Preguntas respondidas: {r['intentos']} | Correctas: {r['aciertos']} | Acierto global: {r['porcentaje']}%")
        for tema in lecciones:
            t = resultados_tema(historial, tema)
            tabla.insert("", "end", values=(tema, t["intentos"], t["aciertos"],
                                            f"{t['porcentaje']}%",
                                            f"{estimar_conocimiento(historial, tema, configuracion):.0%}"))
        tema = recomendar_tema(preguntas, historial, configuracion)
        dominio = estimar_conocimiento(historial, tema, configuracion)
        aviso = f"BKT estima {dominio:.0%} de dominio en {tema}. Te recomendamos estudiarlo."
        proxima.config(text=aviso)
        recomendacion.config(text=aviso + " Puedes revisar las lecciones antes de continuar el quiz.")

    def ver_leccion(*_):
        tema = seleccion_tema.get()
        if tema not in lecciones:
            return
        info = lecciones[tema]
        contenido = (f"TEMA: {tema}\n\nOBJETIVO\n{info['objetivo']}\n\n"
                     f"EXPLICACIÓN\n{info['explicacion']}\n\n"
                     f"EJEMPLOS\n" + "\n".join(f"• {ejemplo}" for ejemplo in info["ejemplos"]))
        texto_leccion.config(state="normal")
        texto_leccion.delete("1.0", "end")
        texto_leccion.insert("end", contenido)
        texto_leccion.config(state="disabled")

    def nueva_pregunta():
        nombre = nombre_actual.get()
        if not nombre:
            messagebox.showwarning("Acceso", "Primero ingresa tu nombre.")
            return
        if preguntas_sesion[0] >= configuracion["preguntas_por_sesion"]:
            # Una nueva sesión conserva el historial para seguir actualizando BKT.
            preguntas_sesion[0] = 0
            pregunta_actual[0] = None
        p = elegir_pregunta(preguntas, estudiantes.get(nombre, []), configuracion)
        pregunta_actual[0] = p
        respuesta.set("")
        resultado.config(text="")
        indicacion.config(text=f"Pregunta {preguntas_sesion[0] + 1} de {configuracion['preguntas_por_sesion']} | "
                              f"Tema: {p['tema']} | Nivel: {p['nivel']}")
        enunciado.config(text=p["pregunta"])
        for boton, letra in zip(opciones, ("a", "b", "c")):
            boton.config(text=f"{letra.upper()}. {p[letra]}")

    def responder():
        p = pregunta_actual[0]
        if p is None:
            # Si se presiona «Enviar» antes de generar la siguiente pregunta,
            # mostramos la pregunta sin registrar una respuesta falsa.
            if not nombre_actual.get():
                messagebox.showwarning("Acceso", "Primero escribe tu nombre y pulsa Ingresar.")
            elif preguntas_sesion[0] >= configuracion["preguntas_por_sesion"]:
                indicacion.config(text="Sesión terminada. Pulsa Iniciar / siguiente pregunta para una nueva sesión.")
            else:
                nueva_pregunta()
            return
        if not respuesta.get():
            messagebox.showwarning("Respuesta", "Selecciona A, B o C.")
            return
        nombre = nombre_actual.get()
        anterior = estimar_conocimiento(estudiantes.get(nombre, []), p["tema"], configuracion)
        acierto = registrar_respuesta(estudiantes, nombre, p, respuesta.get())
        nuevo = estimar_conocimiento(estudiantes[nombre], p["tema"], configuracion)
        guardar_json(ruta_estudiantes, estudiantes)
        preguntas_sesion[0] += 1
        respuesta_correcta = p[p["correcta"].lower()]
        resultado.config(text=("¡Correcto! " if acierto else f"Necesitas repasar. Era: {respuesta_correcta}. ") + p["explicacion"] +
                        f"  |  Dominio BKT: {anterior:.0%} → {nuevo:.0%}")
        pregunta_actual[0] = None
        indicacion.config(text=f"Registrada {preguntas_sesion[0]} de {configuracion['preguntas_por_sesion']}. "
                              "Lee la explicación y pulsa Iniciar / siguiente pregunta para continuar."
                              if preguntas_sesion[0] < configuracion["preguntas_por_sesion"]
                              else "Sesión completada. Pulsa Iniciar / siguiente pregunta para una nueva sesión.")
        refrescar_progreso()

    def entrar():
        nombre = " ".join(nombre_entrada.get().strip().split())
        if not nombre:
            messagebox.showwarning("Nombre", "Escribe tu nombre.")
            return
        nombre_actual.set(nombre)
        estudiantes.setdefault(nombre, [])
        guardar_json(ruta_estudiantes, estudiantes)
        preguntas_sesion[0] = 0
        pregunta_actual[0] = None
        resultado.config(text="")
        refrescar_progreso()
        pestanas.select(inicio_tab)
        mensaje.set(f"Sesión iniciada para {nombre}.")

    def al_cambiar_pestana(_evento=None):
        # Evita que el alumno llegue al cuestionario sin tener pregunta activa.
        if (pestanas.select() == str(prueba_tab) and nombre_actual.get()
                and pregunta_actual[0] is None
                and preguntas_sesion[0] < configuracion["preguntas_por_sesion"]):
            nueva_pregunta()

    pestanas.bind("<<NotebookTabChanged>>", al_cambiar_pestana)
    ttk.Button(acceso, text="Ingresar", command=entrar).pack(side="left")
    ttk.Button(acciones, text="Iniciar / siguiente pregunta", command=nueva_pregunta).pack(side="left", padx=4)
    ttk.Button(acciones, text="Enviar respuesta", command=responder).pack(side="left", padx=4)
    ttk.Button(progreso_tab, text="Actualizar", command=refrescar_progreso).pack(anchor="w", pady=5)
    ttk.Button(docente_tab, text="Actualizar lista", command=refrescar_progreso).pack(anchor="w", pady=5)
    selector.bind("<<ComboboxSelected>>", ver_leccion)
    ttk.Label(ventana, textvariable=mensaje).pack(anchor="w")
    ver_leccion()
    refrescar_progreso()
    ventana.mainloop()


if __name__ == "__main__":
    try:
        iniciar()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print("No se pudo iniciar el tutor:", error)
        print("Comprueba que los archivos CSV y JSON están en sus carpetas.")
