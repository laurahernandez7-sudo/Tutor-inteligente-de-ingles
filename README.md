# Tutor de Inglés Personalizado

**Prototipo académico de Sistemas Inteligentes, cuarto semestre, Universidad de Ibagué.**

**Autoras:** María Fernanda Rodríguez (`maria.rodriguez22@estudiantesunibague.edu.co`) y Laura Sofía Hernández (`laura.hernandez7@estudiantesunibague.edu.co`).  
**Docente:** Alexandra La Cruz (`alexandra.lacruz@unibague.edu.co`).

## ¿Qué es?
Una aplicación de escritorio con apariencia de aula virtual sencilla: tiene inicio, lecciones, quiz adaptativo, progreso y vista docente. Trabaja contenidos básicos de inglés A1. **No es una copia técnica de Canvas/Moodle ni una web**: imita su organización por módulos y usa solamente Python y su biblioteca estándar.

El componente inteligente es una **regla adaptativa explicable**: primero recorre temas no evaluados, después recomienda el tema con menor porcentaje de aciertos. Cuando el estudiante obtiene al menos el porcentaje configurado y acumula suficientes intentos en ese tema, recibe preguntas de nivel reto. No se usa aprendizaje automático ni se afirma detectar trastornos de aprendizaje.

## Requisitos
- Python 3.10 o superior con **Tkinter**. En Windows, la instalación oficial de Python normalmente incluye Tkinter.
- No necesitas internet, bases de datos externas, API, pip ni instalar paquetes.
- Mantén la estructura de carpetas como viene en el ZIP.

## Ejecutar (Windows)
1. Descarga y descomprime **todo** el ZIP.
2. Abre la carpeta `Tutor_de_Ingles_Personalizado` en el Explorador de archivos.
3. Haz clic en la barra de dirección de la carpeta, escribe `cmd` y pulsa Enter.
4. Escribe `py app.py` y pulsa Enter. Si Windows no reconoce `py`, prueba `python app.py`.
5. Si no abre, prueba `py -m tkinter` para verificar que la interfaz gráfica esté instalada.

## Ejecutar (Mac / Linux)
Abre una terminal en la carpeta del proyecto y usa `python3 app.py`. Es necesaria una sesión gráfica; si no abre, comprueba Tkinter (`python3 -m tkinter`).

## Guía de uso
1. Escribe un nombre de demostración, por ejemplo **Estudiante Demo**, y haz clic en **Ingresar**.
2. Abre **Lecciones**, cambia entre los 4 temas y lee la explicación.
3. Ve a **Quiz adaptativo**, haz clic en **Iniciar / siguiente pregunta**, selecciona A, B o C y pulsa **Enviar respuesta**.
4. Lee la explicación. Presiona **Iniciar / siguiente pregunta** para continuar hasta completar cinco respuestas.
5. Abre **Mi progreso**: verás aciertos por tema y el tema recomendado.
6. Abre **Vista docente**: muestra un resumen de nombres y resultados guardados en este computador.
7. Para empezar otra sesión del mismo estudiante, vuelve a pulsar **Ingresar** con el mismo nombre. La información anterior continúa guardada.

**Demostración de adaptación:** ingresa como `Estudiante Demo`. Contesta mal la primera pregunta del tema `Verb to be` y bien las preguntas de `Personal pronouns`, `Articles a/an` y `Present simple`. La siguiente pregunta prioriza `Verb to be` por tener menor porcentaje de aciertos. El progreso puede comprobarse en **Mi progreso**.

## Archivos
- `app.py`: pantallas y botones hechos con Tkinter.
- `logica.py`: carga de datos, evaluación, recomendación y guardado.
- `datos/preguntas.csv`: **32 preguntas** propias del prototipo, 4 temas y 2 niveles.
- `datos/lecciones.json`: contenido de las **4 lecciones**.
- `configuracion.json`: parámetros editables de duración de sesión y nivel reto.
- `datos/estudiantes.json`: historial local creado al utilizar el programa. No subas datos reales de estudiantes a GitHub.
- `pruebas/test_logica.py`: 8 pruebas automatizadas.
- Los materiales de entrega (informe PDF, video y guiones) se comparten por separado; no son necesarios para ejecutar el código.

## Probar la lógica
En la terminal, desde la carpeta del proyecto:

```bash
py -m unittest discover -s pruebas -v
```

En Mac/Linux cambia `py` por `python3`. El resultado esperado para la versión entregada es `Ran 8 tests` y `OK`. Esto verifica la lógica; **no es un experimento pedagógico con estudiantes**.

## ¿Cómo se personaliza?
- **Inicio:** si un tema nunca se ha evaluado, comienza por él.
- **Diagnóstico progresivo:** el programa visita temas todavía no evaluados.
- **Refuerzo:** después elige el tema que tenga menos aciertos porcentuales.
- **Reto:** configura `intentos_para_reto` y `porcentaje_para_reto` en `configuracion.json`.
- **Retroalimentación:** cada respuesta incluye si fue correcta, cuál era la respuesta adecuada y por qué.
- **Persistencia:** los resultados se almacenan en JSON y se recuperan por nombre.

### Restricción de código sin constantes
No hay constantes globales de configuración (por ejemplo, `NOTA_MINIMA = 75`) ni respuestas de preguntas incrustadas en el algoritmo. Las reglas ajustables viven en `configuracion.json`, y los contenidos en CSV/JSON. En cualquier programa deben existir algunos valores literales, como nombres de campos, etiquetas de botones y respuestas A/B/C; eliminarlos literalmente impediría que funcione.

## Limitaciones que deben explicar con honestidad
- Funciona en un solo equipo y los usuarios se identifican **por nombre**, sin contraseña. Usar nombres inventados durante la demostración.
- No es servicio web, no tiene autenticación real ni servidor multiusuario.
- Un porcentaje de aciertos en pocas preguntas no representa una medición certificada del nivel de inglés.
- No diagnostica dislexia ni ninguna condición o dificultad clínica de aprendizaje.
- Las pruebas automatizadas no prueban mejoras reales de aprendizaje. Eso necesitaría participantes, consentimiento y más sesiones.

## Enlaces de entrega
- **GitHub:** https://github.com/laurahernandez7-sudo/Tutor-inteligente-de-ingles
- **Drive:** subir `datos/preguntas.csv` y `datos/lecciones.json` a Drive, compartir la carpeta con la docente y pegar la URL.
- **Video de tres minutos:** grabar la pantalla ejecutando `app.py`, subir el video y agregar su URL al informe.

Para evaluar el código basta con descargar este repositorio y ejecutar `py app.py`. El informe PDF, el video y sus guiones se entregan aparte.