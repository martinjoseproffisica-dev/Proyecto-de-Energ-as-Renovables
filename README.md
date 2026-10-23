# La energía renovable como contenido escolar (versión 8)

Aplicación académica interactiva con Streamlit, Plotly y three.js.

## Qué cambió en esta versión
- **Versión 8**: selector de tema compacto (botón «Tema» con 8 gamas), fondo de Física muy tenue con intensidad regulable, barra superior de una línea, menú lateral que se cierra y se abre en todas las secciones, y numeración del menú igual a la del encabezado de cada sección (00 a 10).
- **Portada**: solo la foto del equipo y todos los datos (integrantes, espacios curriculares, profesores). El cartel verde queda en «Inicio».
- **Temas**: cuatro opciones arriba a la derecha (Bosque, Océano, Atardecer, Noche).
- **Navegación**: al tocar «Siguiente», «Anterior», «Comenzar» o el menú, la página vuelve al comienzo.
- **Contenido nuevo desde la presentación**: antecedentes, hipótesis, método, análisis curricular, voces docentes, contraste de hipótesis, limitaciones y cierre.
- **Laboratorio hidráulico**: turbina 3D con corte, vista explosionada, flujo de agua animado y gráficos de potencia.
- **Compostaje**: corte de la pila con temperaturas, curva por fases y balance de calor.

## Archivos
- `app.py`, `requirements.txt`, `.streamlit/config.toml`
- `componentes/turbina3d.html` (modelo 3D)
- `assets/` (conservá tus fotos y el video: `equipo_estudiantes.jpg`, `relevamiento_01.jpg` … `relevamiento_20.jpg`, `registro_visita.mp4`)

## Fotos nuevas que podés sumar a `assets/`
- `ingreso_cruz_del_eje.jpg`: ingreso a la ciudad (sección «Cruz del Eje»).
- `dique_cruz_del_eje.jpg`: dique (secciones «Cruz del Eje» y «Mapa energético local»).
- `ipea_211.jpg`: foto del IPEA (opcional, sección «Mapa energético local»).
- `figura_saberes.png` y `figura_normativa.png` ya vienen incluidas.
Si una foto no está, la app muestra un recuadro con el nombre exacto del archivo.

## Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
```
