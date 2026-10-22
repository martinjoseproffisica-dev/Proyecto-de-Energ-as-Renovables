# La energía renovable como contenido escolar

Aplicación académica interactiva desarrollada con Streamlit y Plotly para presentar la investigación sobre la enseñanza de las energías renovables en Cruz del Eje.

## Incluye
- Presentación del proyecto y resultados de investigación.
- Mapa energético local con ubicaciones de referencia.
- Laboratorio hidráulico con modelo 3D esquemático y cálculo de potencia.
- Calculadora de calor transferido al agua y explorador conceptual de fases del compostaje.
- Propuestas didácticas para cuatro niveles.
- **Registro de campo** con las fotografías aportadas en el PDF y el video de la visita.

## Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en Streamlit Community Cloud
1. Crear un repositorio nuevo en GitHub.
2. Subir `app.py`, `requirements.txt`, `.streamlit/config.toml`, `README.md` y la carpeta `assets/`.
3. En Streamlit Community Cloud, crear una app seleccionando el repositorio, la rama `main` y `app.py`.

## Nota sobre los materiales
Las fotografías se extrajeron de un PDF de 20 páginas aportado para este proyecto y se guardaron en `assets/`. El video original también se incluye como `assets/registro_visita.mp4`. Revisar el video antes de la exposición: contiene segmentos que podrían no corresponder al tema central.

Los modelos y curvas ilustrativas deben distinguirse de los datos reales relevados. Confirmar con el equipo los nombres, ubicaciones y valores técnicos antes de publicar la aplicación como documento institucional.
