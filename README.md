# Tutor de Inglés Personalizado con BKT

Prototipo académico de **Sistemas Inteligentes (cuarto semestre)**, Universidad de Ibagué.

**Autoras:** María Fernanda Rodríguez (`maria.rodriguez22@estudiantesunibague.edu.co`) y Laura Sofía Hernández (`laura.hernandez7@estudiantesunibague.edu.co`).  
**Docente:** Alexandra La Cruz (`alexandra.lacruz@unibague.edu.co`).

## ¿Qué hace?
Es una aplicación de escritorio en Python básico, con cinco pestañas: Inicio, Lecciones, Quiz adaptativo, Mi progreso y Vista docente. Practica inglés A1 con cuatro lecciones y un banco de 32 preguntas. No es una página web ni un sistema que diagnostique dificultades de aprendizaje.

Su parte inteligente utiliza **Bayesian Knowledge Tracing (BKT)**: actualiza la **probabilidad estimada de dominio** para cada tema a partir de las respuestas de cada estudiante. Es un modelo probabilístico sencillo; no usa redes neuronales ni servicios externos.

## Ejecutar (Windows)
1. Descarga el repositorio como ZIP en **Code → Download ZIP** y extrae la carpeta completa.
2. Instala Python 3.10 o posterior con Tkinter. No se requiere `pip` ni librerías de terceros.
3. Abre la carpeta que contiene `app.py`; en la barra de dirección escribe `cd "Tutor-inteligente-de-ingles-main" ` y presiona Enter.
4. Ejecuta: `py app.py` (o `python app.py`).
5. Ingresa un nombre ficticio, estudia una lección, responde el quiz y consulta **Mi progreso**.

En Linux/macOS usa `python3 app.py` si Tkinter está disponible.

## Modelo BKT explicado con números
Para cada estudiante y cada tema se calcula `P(L)`, probabilidad de conocer esa habilidad. Cada respuesta actualiza la probabilidad con el teorema de Bayes y una transición de aprendizaje.

Los parámetros están en `configuracion.json`:

| Parámetro | Valor ilustrativo | Significado |
|---|---:|---|
| `inicial` | 0.30 | P(L0): probabilidad de conocimiento antes de responder |
| `aprendizaje` | 0.15 | P(T): aprendizaje por oportunidad de práctica |
| `adivinar` | 0.20 | P(G): acierto sin dominio |
| `desliz` | 0.10 | P(S): error a pesar del dominio |

Si responde **bien**:
`posterior = (P * (1 - S)) / (P * (1 - S) + (1 - P) * G)`

Si responde **mal**:
`posterior = (P * S) / (P * S + (1 - P) * (1 - G))`

Después:
`P_nueva = posterior + (1 - posterior) * T`

Con los valores iniciales, un acierto estima aproximadamente **71 %** de dominio y un error, **19 %**. No son porcentajes de acierto: son estimaciones del modelo. Los cuatro parámetros se fijaron como ejemplo académico y **no se entrenaron con datos de estudiantes**.

## ¿Cómo elige el siguiente ejercicio?
1. Explora los temas todavía no evaluados para obtener una primera respuesta de cada uno.
2. Cuando todos tienen respuestas, recomienda el de **menor dominio BKT**.
3. Si el tema cuenta con **dos intentos o más** y su dominio BKT alcanza **0.75**, propone nivel `reto`; de lo contrario, nivel `basico`.
4. Evita repetir preguntas hasta agotar las disponibles en ese nivel.
5. Registra el historial local en `datos/estudiantes.json`. Se recalcula BKT a partir de ese historial cuando se abre la aplicación.

Los parámetros educativos no son constantes globales de Python: se editan en `configuracion.json`. Las preguntas y respuestas están en CSV.

## Archivos del repositorio

```text
app.py                      Interfaz Tkinter
logica.py                   Cálculo BKT, selección y guardado
configuracion.json          Valores configurables del modelo
datos/preguntas.csv         32 ejercicios A1
datos/lecciones.json        4 lecciones
pruebas/test_logica.py      13 pruebas automáticas
README.md                   Este documento
.gitignore                  Excluye registros locales y archivos temporales
```

## Pruebas
Desde la carpeta del programa, ejecuta:

```bash
py -m unittest discover -s pruebas -v
```

El resultado esperado en esta versión es **`Ran 13 tests` y `OK`**. Los casos comprueban fórmulas BKT con aciertos y errores, independencia por tema, configuraciones, selección de dificultad, lectura CSV y guardado JSON. Esto verifica el software, **no** demuestra una mejora de aprendizaje real.

## Limitaciones
- Valores BKT propuestos para demostración; no ajustados estadísticamente.
- Solo cuatro temas y 32 preguntas.
- Sin autenticación ni servicio web; se recomienda usar nombres ficticios.
- No diagnostica dislexia u otras condiciones y no ha sido validado en participantes reales.
- La vista docente sirve solamente como demostración local.

## Enlaces de entrega
- **Código GitHub:** https://github.com/laurahernandez7-sudo/Tutor-inteligente-de-ingles
- **Datos Drive:** https://drive.google.com/drive/folders/1mugCjFFBAV3XXrO9VuerbwRmmz-xFoUG?usp=sharing 
  
**Referencia base BKT:** Corbett, A. T., y Anderson, J. R. (1994). *Knowledge tracing: Modeling the acquisition of procedural knowledge*. User Modeling and User-Adapted Interaction, 4, 253–278. https://doi.org/10.1007/BF01099821
