# La energía renovable como contenido escolar

Aplicación académica interactiva desarrollada con Streamlit y Plotly para presentar una investigación sobre la enseñanza de las energías renovables en Cruz del Eje, Córdoba.

## Portada del equipo
La primera pantalla es **Presentación del equipo**. Para mostrar la foto grupal, cargá la imagen en la carpeta `assets/` con este nombre exacto: `equipo_estudiantes.jpg`. La ruta completa debe ser `assets/equipo_estudiantes.jpg`. Si la foto aún no está, la aplicación muestra un recuadro de reemplazo y sigue funcionando.

Para cambiar los nombres de ejemplo, editá la lista `team_members` en `app.py` dentro de la sección `Presentación del equipo`. Agregá o quitá integrantes según corresponda.

## Contenidos
- Presentación del proyecto, objetivos, metodología y resultados.
- Mapa energético local con el dique, IPEA N.º 211, central El Ferroviario y la ubicación más reciente publicada para el proyecto de parque solar.
- Laboratorio hidráulico 3D y cálculo de potencia.
- Simulación conceptual de compostaje y estimación del calor transferido al agua.
- Propuestas didácticas para los niveles inicial, primario, secundario y superior.
- Galería de fotografías y video del relevamiento de campo.
- Accesos a legislación ambiental y fuentes técnicas.

## Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicación en Streamlit Community Cloud
1. Subir `app.py`, `requirements.txt`, `.streamlit/config.toml`, `README.md` y `assets/` a un repositorio GitHub. Conservá los nombres de los archivos existentes y agregá `assets/equipo_estudiantes.jpg` cuando tengas la fotografía grupal.
2. Crear una aplicación en Streamlit Community Cloud y seleccionar ese repositorio, la rama `main` y el archivo `app.py`.

## Criterio de lectura de los datos
Los resultados de la investigación, los valores informados en el relevamiento y las simulaciones didácticas se presentan diferenciados. Las ubicaciones del mapa se acompañan con enlaces a sus fuentes. El expediente ambiental difundido en 2026 ubica el proyecto de parque solar en Pedanía San Marcos; un documento de EPEC de 2022 consignaba otro emplazamiento, por lo que ambos antecedentes se distinguen en la aplicación.
