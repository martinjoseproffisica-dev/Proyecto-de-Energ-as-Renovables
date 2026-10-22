import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Energía renovable · Cruz del Eje", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --ink:#142b2b; --muted:#55706b; --green:#146b55; --lime:#c9f36b; --paper:#f5f7f1; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
/* Contraste accesible para controles y datos */
.stApp, [data-testid="stAppViewContainer"] { color:#142b2b !important; }
.stMarkdown, .stMarkdown p, .stMarkdown li, label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p { color:#142b2b !important; }
[data-testid="stSlider"] label, [data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label { color:#142b2b !important; font-weight:700 !important; }
[data-testid="stSlider"] [data-testid="stTickBar"] + div, [data-testid="stSlider"] [data-testid="stThumbValue"] { color:#142b2b !important; }
[data-testid="stNumberInput"] input, [data-testid="stTextInput"] input { color:#142b2b !important; background:#ffffff !important; }
[data-testid="stMetricValue"] { color:#146b55 !important; }
.stButton button, .stLinkButton a { border-radius:12px !important; font-weight:700 !important; background:#ffffff !important; color:#173b35 !important; border:1px solid #b8cec4 !important; }
.stButton button:hover, .stLinkButton a:hover { background:#e4f2e9 !important; color:#103b31 !important; border-color:#43836d !important; }
.stButton button[kind="primary"], .stButton button[data-testid*="baseButton-primary"] { background:#146b55 !important; color:#ffffff !important; border:1px solid #146b55 !important; }
.stButton button[kind="primary"] *, .stButton button[data-testid*="baseButton-primary"] * { color:#ffffff !important; }
.stMarkdown a { color:#075f88 !important; text-decoration:underline !important; font-weight:600; }
[data-testid="stSlider"] [data-testid="stThumbValue"] { background:#146b55 !important; color:#ffffff !important; }
[data-testid="stSlider"] [data-testid="stTickBar"] div { color:#142b2b !important; }
[data-testid="stMetricLabel"] { color:#34554d !important; }
.stAlert, [data-testid="stAlert"] * { color:#142b2b !important; }
.nav-note { color:#55706b; font-size:.9rem; }
[data-testid="stPlotlyChart"] { border-radius:14px; overflow:hidden; }
.stApp { background:var(--paper); color:var(--ink); }
[data-testid="stSidebar"] { background:#102f2d; }
[data-testid="stSidebar"] * { color:#f4f7ed !important; }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.035em; }
.hero { padding:2.8rem 2.8rem 2.5rem; border-radius:24px; color:white; background:linear-gradient(110deg,rgba(9,39,36,.94),rgba(20,107,85,.65)),url('https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=1800&q=85'); background-size:cover;background-position:center; min-height:370px; display:flex; flex-direction:column; justify-content:flex-end; }
.eyebrow { text-transform:uppercase; letter-spacing:.16em; font-size:.75rem; font-weight:700; color:#d7f69a; }
.hero h1 { color:white; font-size:clamp(2.5rem,5vw,4.7rem); line-height:.98; max-width:850px; margin:.8rem 0 1rem; }
.hero p { color:#eef7ec; font-size:1.12rem; max-width:720px; }
.pill { display:inline-block; padding:.35rem .75rem; border:1px solid rgba(255,255,255,.4); border-radius:99px; font-size:.8rem; margin:.15rem .25rem .15rem 0; }
.card { background:white; padding:1.25rem 1.35rem; border:1px solid #e1e9df; border-radius:18px; height:100%; box-shadow:0 6px 24px rgba(21,54,43,.035); }
.card .kicker { color:var(--green); font-size:.75rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; }
.card h3 { margin:.4rem 0; }
.big-number { font-family:'Space Grotesk',sans-serif; font-size:2.1rem; font-weight:700; color:var(--green); }
.section-label { color:var(--green); font-weight:700; text-transform:uppercase; letter-spacing:.14em; font-size:.75rem; }
.callout { background:#e8f3dd; border-left:4px solid #78a943; padding:1rem 1.2rem; border-radius:0 12px 12px 0; }
.small-muted { color:#60756d; font-size:.88rem; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚡ Energía renovable")
    st.caption("Investigación educativa · Cruz del Eje")
    pages = ["Inicio", "La investigación", "Mapa energético local", "Cruz del Eje", "Registro de campo", "Laboratorio hidráulico 3D", "Compostaje y calor", "Propuestas didácticas", "Resultados y conclusiones"]
    def set_page(target):
        st.session_state["nav_page"] = target
        st.session_state["_scroll_to_top"] = True
    def mark_scroll_to_top():
        st.session_state["_scroll_to_top"] = True
    page = st.radio("RECORRIDO", pages, label_visibility="collapsed", key="nav_page", on_change=mark_scroll_to_top)
    st.divider()
    st.markdown("**Profesorado Universitario de Física**")
    st.caption("UPC · Sede Cruz del Eje · 2026")
    st.caption("Proyecto académico interactivo")

# Al cambiar de sección, la presentación comienza desde el encabezado.
if st.session_state.pop("_scroll_to_top", False):
    st.components.v1.html("""
    <script>
    const goTop = () => {
      try {
        window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
        const main = window.parent.document.querySelector('[data-testid="stMain"]');
        const app = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        if (main) main.scrollTo({top: 0, left: 0, behavior: 'instant'});
        if (app) app.scrollTo({top: 0, left: 0, behavior: 'instant'});
      } catch (e) { window.parent.scrollTo(0, 0); }
    };
    goTop(); setTimeout(goTop, 120);
    </script>
    """, height=0)

def heading(kicker, title, desc=None):
    st.markdown(f'<div class="section-label">{kicker}</div><h1>{title}</h1>', unsafe_allow_html=True)
    if desc: st.markdown(desc)

def metric_card(kicker, number, desc):
    st.markdown(f'<div class="card"><div class="kicker">{kicker}</div><div class="big-number">{number}</div><div>{desc}</div></div>', unsafe_allow_html=True)

if page == "Inicio":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Investigación · Educación · Territorio</div>
      <h1>La energía renovable como contenido escolar</h1>
      <p>Análisis curricular y propuestas de transposición didáctica en Cruz del Eje y Córdoba.</p>
      <div><span class="pill">Inicial</span><span class="pill">Primario</span><span class="pill">Secundario</span><span class="pill">Superior</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown("### Una investigación que conecta el aula con el territorio")
    st.markdown("El proyecto analiza cómo se enseñan las energías renovables en los documentos curriculares y en las prácticas docentes, y qué brechas existen frente al conocimiento físico del potencial energético local.")
    cols=st.columns(3)
    with cols[0]: metric_card("Caso de estudio", "Cruz del Eje", "Dique, central hidroeléctrica y parque solar.")
    with cols[1]: metric_card("Trabajo de campo", "6 docentes", "Entrevistas a docentes de cuatro niveles educativos.")
    with cols[2]: metric_card("Producto", "4 propuestas", "Una propuesta didáctica para cada nivel educativo.")
    st.write("")
    st.markdown('<div class="callout"><b>Idea central</b><br>La ausencia del contexto local en los documentos curriculares no equivale a su ausencia en el aula: su incorporación depende, en gran medida, de la iniciativa docente y de los recursos disponibles.</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("### Explorar el proyecto")
    cols=st.columns(3)
    items=[("01 · Investigación","Pregunta, objetivos, marco teórico y método."),("02 · Territorio","Mapa energético local y recursos del caso."),("03 · Laboratorios","Exploraciones interactivas de potencia hidráulica y calor.")]
    for c,(t,d) in zip(cols,items):
        with c: st.markdown(f'<div class="card"><div class="kicker">Explorar</div><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
    st.markdown("### Ir directamente a una sección")
    jump_cols = st.columns(3)
    for col, label, target in zip(jump_cols, ["Ver el mapa local", "Abrir laboratorio hidráulico", "Explorar compostaje y calor"], ["Mapa energético local", "Laboratorio hidráulico 3D", "Compostaje y calor"]):
        with col:
            st.button(label, use_container_width=True, on_click=set_page, args=(target,))

elif page == "La investigación":
    heading("01 · El proyecto", "¿Cómo se enseñan las energías renovables?", "La investigación compara lo que prescriben los documentos, lo que declaran los docentes y el conocimiento físico del potencial energético local.")
    st.markdown("### Pregunta de investigación")
    st.markdown('<div class="callout">¿Cómo se enseñan las energías renovables en los documentos curriculares y en las prácticas docentes de los cuatro niveles, y qué brechas hay frente al conocimiento físico del potencial energético local?</div>',unsafe_allow_html=True)
    st.write("")
    a,b=st.columns(2)
    with a:
        st.markdown("#### Objetivo general")
        st.write("Analizar cómo se enseñan las energías renovables en los documentos y en las percepciones docentes de los cuatro niveles, identificar brechas frente al conocimiento físico local y elaborar propuestas de transposición didáctica.")
    with b:
        st.markdown("#### Objetivos específicos")
        st.markdown("1. Analizar presencia, profundidad y continuidad en los documentos.\n2. Relevar concepciones, apoyos y dificultades docentes.\n3. Evaluar la presencia del contexto energético local.\n4. Analizar la coherencia vertical entre niveles.\n5. Diseñar propuestas por nivel.")
    st.divider()
    st.markdown("### Marco conceptual: tres saberes")
    cols=st.columns(3)
    for c,n,t,d in zip(cols,["01","02","03"],["Saber sabio","Saber a enseñar","Saber enseñado"],["Visita técnica a la central Ferroviario y pliego de EPEC.","Progresiones de Ciencias Naturales y Tecnología, y plan de la Licenciatura en HST.","Entrevistas a seis docentes de los cuatro niveles."]):
        with c: st.markdown(f'<div class="card"><div class="kicker">{n}</div><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
    st.markdown("También completan el marco la alfabetización científica y el enfoque CTSA, el aprendizaje situado y la articulación curricular vertical.")
    st.markdown("### Método")
    st.markdown("- **Documentos:** progresiones de Ciencias Naturales, Educación Tecnológica y Computación, y plan de la Licenciatura en HST.\n- **Entrevistas:** seis docentes; entrevistas semiestructuradas de 15 a 20 minutos, anónimas.\n- **Visitas:** central Ferroviario, con entrevista a un técnico, e IPEA N.° 211, con entrevista a un docente.\n\n<small>Investigación cualitativa exploratoria, con muestra por conveniencia.</small>",unsafe_allow_html=True)

elif page == "Mapa energético local":
    heading("02 · Territorio", "Mapa energético local", "Un mapa de referencia para conectar la investigación con los lugares que la hacen concreta.")
    import pandas as pd
    locations = pd.DataFrame([
        {"Lugar":"Dique Cruz del Eje / Arturo Illia", "Latitud":-30.76194, "Longitud":-64.75248, "Tipo":"Agua y generación", "Detalle":"Embalse asociado al riego y a la generación hidroeléctrica."},
        {"Lugar":"IPEA N.º 211 Presidente Arturo Illia", "Latitud":-30.74969, "Longitud":-64.73899, "Tipo":"Biomasa y educación", "Detalle":"Institución educativa vinculada al relevamiento sobre compostaje."},
        {"Lugar":"Central hidroeléctrica El Ferroviario (EPEC)", "Latitud":-30.74950, "Longitud":-64.79675, "Tipo":"Generación hidroeléctrica", "Detalle":"Ubicación identificada mediante el código de mapa 7623+68."},
        {"Lugar":"Parque Solar Fotovoltaico Cruz del Eje (expediente ambiental 2026)", "Latitud":-30.746833, "Longitud":-64.727333, "Tipo":"Energía solar fotovoltaica", "Detalle":"Coordenadas publicadas en el aviso de proyecto ambiental de 2026: Pedanía San Marcos, fuera del ejido urbano."},
    ])
    figmap = go.Figure()
    figmap.add_trace(go.Scattermap(
        lat=locations["Latitud"], lon=locations["Longitud"], mode="markers+text",
        text=["Dique Arturo Illia", "IPEA N.º 211", "Central El Ferroviario", "Parque solar · proyecto 2026"], textposition="top right",
        marker=dict(size=[18,15,17,16], color=["#167d72", "#d6a73b", "#2864b4", "#e1a52e"]),
        customdata=locations[["Tipo", "Detalle"]].values,
        hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
    ))
    figmap.update_layout(map=dict(style="open-street-map", center=dict(lat=-30.753, lon=-64.763), zoom=10.5),
                         height=510, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)",
                         legend=dict(orientation="h"))
    st.plotly_chart(figmap, use_container_width=True)
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="card"><div class="kicker">Agua</div><h3>Dique Arturo Illia</h3><p>Un sistema donde el agua cumple funciones de regulación, riego y generación. Es el punto de partida para conversar sobre altura, caudal y potencia.</p><a href="https://www.diquesdecordoba.com.ar/dique-cruz-del-eje/" target="_blank">Consultar ficha del dique ↗</a></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><div class="kicker">Biomasa</div><h3>IPEA N.º 211</h3><p>La investigación incorpora las prácticas de compostaje como oportunidad para estudiar procesos exotérmicos y recuperación de calor.</p><a href="https://mapa.educacion.gob.ar/legajo/140256100" target="_blank">Consultar ficha educativa ↗</a></div>', unsafe_allow_html=True)
    st.markdown("### Central hidroeléctrica El Ferroviario")
    st.write("El punto de El Ferroviario corresponde al código de ubicación 7623+68. Para el parque solar se prioriza la ubicación informada en el aviso de proyecto ambiental de 2026: Pedanía San Marcos, fuera del ejido urbano de Cruz del Eje.")
    st.link_button("Abrir El Ferroviario en Google Maps", "https://www.google.com/maps/search/?api=1&query=7623%2B68%20Cruz%20del%20Eje%2C%20C%C3%B3rdoba")
    st.link_button("Consultar aviso ambiental 2026 del parque solar", "https://cadenacentro.com/ultimas/audiencia-publica-ambiental-digital-proyecto-parque-solar-fotovoltaico-cruz-del-eje-2/")
    st.link_button("Consultar antecedente técnico de EPEC (2022)", "https://www.epec.com.ar/docs/imagenes/comunidad/blog/88/ANEXO3_PROYECTOS_PROPUESTOS_POR_EPEC_Convocatoria2022.pdf")
    st.caption("Hay una diferencia entre la ubicación consignada en el documento de EPEC de 2022 (frente a la central hidroeléctrica) y la ubicación del expediente ambiental difundido en 2026. El mapa muestra la ubicación más reciente publicada y conserva el antecedente como fuente de contexto.")

elif page == "Registro de campo":
    heading("02 · Evidencias del territorio", "Registro de campo", "Fotografías aportadas para documentar la visita a la central hidroeléctrica y al IPEA N.º 211.")
    st.markdown("### Central hidroeléctrica Ferroviario")
    st.write("Equipamiento, turbinas, instrumentos y sectores de la instalación registrados durante el relevamiento.")
    central_cols = st.columns(3)
    for idx, col in zip(range(1, 11), central_cols * 4):
        with col:
            st.image(f"assets/relevamiento_{idx:02d}.jpg", use_container_width=True, caption=f"Registro de campo · imagen {idx}")
    st.divider()
    st.markdown("### IPEA N.º 211 y espacios de compostaje")
    st.write("Espacios de la institución educativa, invernadero y pilas de material orgánico incluidos en el registro fotográfico.")
    school_cols = st.columns(3)
    for idx, col in zip(range(11, 21), school_cols * 4):
        with col:
            st.image(f"assets/relevamiento_{idx:02d}.jpg", use_container_width=True, caption=f"Registro de campo · imagen {idx}")
    st.divider()
    st.markdown("### Video de la visita")
    st.caption("Registro audiovisual de la visita técnica.")
    st.video("assets/registro_visita.mp4")

elif page == "Cruz del Eje":
    heading("02 · Anclaje territorial", "Un caso energético real", "El contexto local permite conectar conceptos físicos, infraestructura y decisiones ambientales con lugares cercanos a la comunidad educativa.")
    st.markdown("El caso local permite analizar distintas formas de aprovechamiento energético y discutir su relación con la educación ambiental.")
    cols=st.columns(3)
    with cols[0]:
        st.markdown('<div class="card"><div class="kicker">Agua</div><h3>Dique Arturo Illia</h3><p>Recurso vinculado al riego y a la generación hidroeléctrica.</p></div>',unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="card"><div class="kicker">Electricidad</div><h3>Central Ferroviario</h3><p>Caída neta relevada de 28 m y potencia informada de 0,5 MW. Elevación de tensión de 380 V a 13.200 V.</p></div>',unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div class="card"><div class="kicker">Sol</div><h3>Parque solar fotovoltaico</h3><p>El aviso ambiental difundido en 2026 ubica el proyecto en Pedanía San Marcos, fuera del ejido urbano de Cruz del Eje. La documentación de EPEC de 2022 consignaba un emplazamiento distinto.</p><a href="https://cadenacentro.com/ultimas/audiencia-publica-ambiental-digital-proyecto-parque-solar-fotovoltaico-cruz-del-eje-2/" target="_blank">Consultar aviso ambiental 2026 ↗</a></div>',unsafe_allow_html=True)
    st.write("")
    st.markdown("### ¿Por qué importa el contexto local?")
    st.write("En el análisis documental, ningún documento menciona explícitamente Cruz del Eje, el dique o EPEC. Sin embargo, cinco de los seis docentes entrevistados usan o mencionan el contexto local. Esto muestra una distancia entre lo prescripto y lo enseñado.")
    st.markdown("### Marco normativo citado en el trabajo")
    laws = [
        ("Constitución Nacional · artículo 41", "https://www.argentina.gob.ar/normativa/nacional/804/texto", "Derecho a un ambiente sano y deber de preservarlo."),
        ("Ley 25.675 · General del Ambiente", "https://www.argentina.gob.ar/normativa/nacional/79980/texto", "Principios de política ambiental, educación e información ambiental."),
        ("Ley 27.621 · Educación Ambiental Integral", "https://www.argentina.gob.ar/normativa/nacional/ley-27621-350594/texto", "Establece la educación ambiental integral como política pública nacional."),
        ("Ley provincial 10.823 · adhesión de Córdoba a la Ley 27.621", "https://legislaturacba.gob.ar/wp-content/uploads/2022/06/29-06-2022-LEY-10.823-Adhi%C3%A9rese-la-Provincia-de-C%C3%B3rdoba-a-las-disposiciones-de-la-Ley-Nacional-N%C2%BA-27621-Implementaci%C3%B3n-de-la-Educaci%C3%B3n-Ambiental-Integral.pdf", "Adhesión provincial a la Ley Nacional de Educación Ambiental Integral."),
        ("Ley 5.589 · Código de Aguas de Córdoba", "https://www.argentina.gob.ar/normativa/provincial/ley-5589-123456789-0abc-defg-985-5000ovorpyel/actualizacion", "Norma provincial sobre aprovechamiento, conservación y protección de las aguas."),
    ]
    for law_title, law_url, law_desc in laws:
        st.markdown(f'<div class="card" style="margin-bottom:.65rem;padding:1rem 1.15rem"><a href="{law_url}" target="_blank">{law_title} ↗</a><p style="margin:.35rem 0 0">{law_desc}</p></div>', unsafe_allow_html=True)

elif page == "Laboratorio hidráulico 3D":
    heading("04 · Simulación interactiva", "Laboratorio hidráulico", "Modificá las variables del modelo para explorar cómo se relacionan la altura de caída, el caudal y la potencia hidráulica.")
    st.markdown('<div class="callout"><b>Modelo idealizado</b><br>La potencia hidráulica disponible se estima con P = ρ · g · Q · H. La potencia eléctrica depende además de la eficiencia del sistema. Los controles permiten explorar escenarios; no son mediciones de la central.</div>',unsafe_allow_html=True)
    c1,c2=st.columns([1,1.35])
    with c1:
        st.markdown("#### Variables del modelo")
        h=st.slider("Altura neta H (m)",1.0,40.0,28.0,0.5)
        q=st.slider("Caudal Q (m³/s)",0.1,4.0,2.3,0.1)
        eff=st.slider("Eficiencia global (%)",20,95,80,1)
        rho=1000; g=9.81
        p_h=rho*g*q*h/1e6
        p_e=p_h*eff/100
        st.metric("Potencia hidráulica estimada",f"{p_h:.3f} MW")
        st.metric("Potencia eléctrica estimada",f"{p_e:.3f} MW",help="Potencia hidráulica multiplicada por la eficiencia supuesta.")
        st.caption("El valor de eficiencia es un supuesto modificable para fines didácticos.")
    with c2:
        st.markdown("#### Modelo 3D de una turbina hidráulica")
        st.caption("Esquema didáctico de los componentes principales; no es un plano constructivo de la central Ferroviario.")
        # Modelo volumétrico conceptual de turbina Francis horizontal, con carcasa en corte.
        # La geometría ilustra el recorrido del agua; no representa dimensiones constructivas reales.
        fig = go.Figure()
        ang = np.linspace(-0.35, 5.15, 110)  # abertura frontal para ver el interior
        cross = np.linspace(0, 2*np.pi, 28)
        A, T = np.meshgrid(ang, cross)
        # Voluta metálica en corte: tubo curvo de sección variable alrededor del rodete.
        major = 0.88 + 0.08*np.sin(A)
        minor = 0.22 + 0.07*(A-ang.min())/(ang.max()-ang.min())
        Xv = (major + minor*np.cos(T))*np.cos(A)
        Yv = (major + minor*np.cos(T))*np.sin(A)
        Zv = 0.49 + minor*np.sin(T)
        fig.add_trace(go.Surface(x=Xv, y=Yv, z=Zv, surfacecolor=np.broadcast_to(minor, Xv.shape),
            colorscale=[[0,"#718792"],[0.45,"#c6d2d6"],[1,"#526b77"]],
            opacity=.66, showscale=False, name="Carcasa espiral (corte)",
            hovertemplate="Carcasa espiral: distribuye el agua alrededor del rodete<extra></extra>"))
        # Bridas y tuberías de entrada/salida, representadas como tubos con líneas gruesas.
        fig.add_trace(go.Scatter3d(x=[-2.75,-2.25,-1.75,-1.18], y=[1.28,1.22,0.98,0.63], z=[0.50,0.50,0.50,0.50],
            mode="lines", line=dict(color="#1a91c8", width=28), name="Entrada de agua",
            hovertemplate="Entrada de agua a presión<extra></extra>"))
        fig.add_trace(go.Scatter3d(x=[1.05,1.55,2.05,2.55], y=[0,0,0,0], z=[0.18,0.18,0.18,0.18],
            mode="lines", line=dict(color="#238fc0", width=24), name="Salida / tubo de aspiración",
            hovertemplate="Salida del agua hacia el canal de restitución<extra></extra>"))
        # Bridas metálicas visibles en los extremos de las tuberías.
        for x0, y0, z0 in [(-2.15,1.22,.50),(1.52,0,.18)]:
            phi = np.linspace(0,2*np.pi,50)
            fig.add_trace(go.Scatter3d(x=np.full_like(phi,x0), y=y0+.20*np.cos(phi), z=z0+.20*np.sin(phi),
                mode="lines", line=dict(color="#d8e0e3",width=5), showlegend=False, hoverinfo="skip"))
        # Anillo guía / distribuidor alrededor del rodete.
        phi=np.linspace(0,2*np.pi,100)
        for z0, rad in [(0.40,.82),(0.62,.82)]:
            fig.add_trace(go.Scatter3d(x=rad*np.cos(phi), y=rad*np.sin(phi), z=np.full_like(phi,z0),
                mode="lines", line=dict(color="#c0a36d",width=9), name="Distribuidor" if z0==.40 else None,
                showlegend=(z0==.40), hovertemplate="Distribuidor: orienta el flujo hacia los álabes<extra></extra>"))
        # Rodete, eje horizontal y palas curvadas.
        fig.add_trace(go.Scatter3d(x=[-0.12,0.12], y=[0,0], z=[0.51,0.51], mode="lines",
            line=dict(color="#b77a29",width=18), name="Cubo del rodete", hovertemplate="Cubo del rodete<extra></extra>"))
        for a0 in np.linspace(0,2*np.pi,10,endpoint=False):
            radii=np.linspace(.16,.73,14)
            curve=a0 + 0.30*(radii-.16)/(.73-.16)
            fig.add_trace(go.Scatter3d(x=radii*np.cos(curve), y=radii*np.sin(curve),
                z=.51+0.06*np.sin(np.linspace(0,np.pi,14)), mode="lines",
                line=dict(color="#e7b44f",width=10), showlegend=False,
                hovertemplate="Álabe curvado del rodete<extra></extra>"))
        # Eje de transmisión hacia el generador, colocado a la izquierda del rodete.
        fig.add_trace(go.Scatter3d(x=[-0.10,-0.55,-0.85,-1.08], y=[0,0,0,0], z=[0.51,0.51,0.51,0.51],
            mode="lines", line=dict(color="#d0d6da",width=13), name="Eje de transmisión",
            hovertemplate="El eje transmite el giro al generador<extra></extra>"))
        # Generador cilíndrico horizontal: malla lateral y tapas.
        gx=np.linspace(-1.95,-1.05,28); gp=np.linspace(0,2*np.pi,60)
        GX, GP = np.meshgrid(gx, gp)
        GY=.40*np.cos(GP); GZ=.51+.40*np.sin(GP)
        fig.add_trace(go.Surface(x=GX,y=GY,z=GZ,colorscale=[[0,"#425966"],[.5,"#8fa0a9"],[1,"#d0d8dc"]],
            showscale=False,opacity=.98,name="Generador eléctrico",hovertemplate="Generador: convierte energía mecánica en eléctrica<extra></extra>"))
        for x0 in [-1.95,-1.05]:
            fig.add_trace(go.Scatter3d(x=np.full_like(gp,x0),y=.40*np.cos(gp),z=.51+.40*np.sin(gp),
                mode="lines",line=dict(color="#344955",width=7),showlegend=False,hoverinfo="skip"))
        # Etiquetas espaciales para lectura inmediata.
        labels=[(-2.25,.40,1.02,"GENERADOR"),(-1.15,.05,.95,"EJE"),(.05,.90,1.03,"RODETE"),(.95,-.15,.90,"CARCASA / DISTRIBUIDOR"),(-2.65,1.42,.88,"ENTRADA"),(2.00,.25,.52,"SALIDA")]
        for lx,ly,lz,txt in labels:
            fig.add_trace(go.Scatter3d(x=[lx],y=[ly],z=[lz],mode="text",text=[txt],
                textfont=dict(size=10,color="#18343a"),showlegend=False,hoverinfo="skip"))
        fig.update_layout(height=560, margin=dict(l=0,r=0,t=8,b=10), paper_bgcolor="rgba(0,0,0,0)",
            scene=dict(xaxis=dict(visible=False,range=[-3.1,2.9]),yaxis=dict(visible=False,range=[-1.65,1.65]),
            zaxis=dict(visible=False,range=[-0.1,1.35]),aspectmode="manual",aspectratio=dict(x=1.8,y=1.05,z=.85),
            camera=dict(eye=dict(x=1.65,y=1.8,z=1.25))),
            legend=dict(orientation="h",y=-.04,font=dict(color="#142b2b",size=10)),font=dict(color="#142b2b"))
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Ver esquema de referencia de una turbina hidráulica"):
            st.image("assets/turbina_referencia_componentes.png", use_container_width=True, caption="Esquema de referencia aportado para identificar entrada de agua, distribuidor, rodete, eje, generador y salida.")
            st.caption("Esquema de referencia de los componentes principales de una turbina hidráulica.")
        st.markdown("**Partes identificables**")
        pcols = st.columns(3)
        for col, name, desc in zip(pcols, ["Entrada / distribuidor", "Rodete y eje", "Generador / salida"], ["El agua llega guiada hacia la turbina.", "El flujo transfiere energía al conjunto móvil.", "El eje acciona el generador; el agua continúa hacia la salida."]):
            with col:
                st.markdown(f'<div class="card"><h3 style="font-size:1rem">{name}</h3><p style="font-size:.88rem">{desc}</p></div>', unsafe_allow_html=True)
    st.markdown("#### Explorá el resultado")
    xs=np.linspace(.1,4,50)
    ys=rho*g*xs*h*eff/100/1e6
    f2=go.Figure(go.Scatter(x=xs,y=ys,mode="lines",line=dict(width=3,color="#16836a"),name="Potencia eléctrica estimada"))
    f2.add_trace(go.Scatter(x=[q],y=[p_e],mode="markers",marker=dict(size=12,color="#f1bd4b"),name="Escenario actual"))
    f2.update_layout(height=300,margin=dict(l=10,r=10,t=20,b=10),xaxis_title="Caudal Q (m³/s)",yaxis_title="Potencia (MW)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="white")
    st.plotly_chart(f2,use_container_width=True)
    st.info("La potencia estimada aumenta en proporción directa al caudal cuando la altura y la eficiencia permanecen constantes.")

elif page == "Compostaje y calor":
    heading("04 · Biomasa y energía térmica", "Compostaje y calor", "Explorá las fases de un proceso biológico y diferenciá el calor transferido al agua de la energía realmente recuperable.")
    st.markdown("La investigación describe que en la escuela se mide la temperatura de las pilas, pero no se registra directamente el calor liberado. Esta calculadora es un ejercicio didáctico: estima el calor necesario para elevar la temperatura de una masa de agua.")
    c1,c2=st.columns([1,1])
    with c1:
        mass=st.number_input("Masa de agua (kg)",min_value=1.0,max_value=10000.0,value=100.0,step=10.0)
        t0=st.slider("Temperatura inicial (°C)",0,40,20)
        t1=st.slider("Temperatura final (°C)",20,90,40)
        days=st.slider("Días de suministro",1,30,18)
        cp=4186
        delta=max(0,t1-t0)
        heat=mass*cp*delta
        kwh=heat/3.6e6
        st.metric("Calor transferido al agua",f"{heat:,.0f} J")
        st.metric("Equivalencia energética",f"{kwh:.2f} kWh")
    with c2:
        st.markdown('<div class="card"><div class="kicker">Modelo físico</div><h3>Q = m · c · ΔT</h3><p><b>m</b>: masa de agua (kg)<br><b>c</b>: calor específico del agua (aprox. 4186 J/kg·°C)<br><b>ΔT</b>: variación de temperatura</p><hr><div class="kicker">Escenario elegido</div><div class="big-number">{:.1f} °C</div><p>Incremento de temperatura del agua durante el cálculo.</p><p class="small-muted">La calculadora no predice el calor real disponible en una pila de compost. Para eso se necesitan mediciones y un modelo de pérdidas, duración y recuperación térmica.</p></div>'.format(delta),unsafe_allow_html=True)
    st.write("")
    st.markdown("### Tres procesos estudiados en el IPEA")
    cols=st.columns(3)
    data=[("Compost","Estiércol, paja y restos vegetales.","Entre 3 y 6 meses"),("Bokashi","Materiales similares, con levadura, azúcar y polvillo de maíz.","Alrededor de 20 días"),("Lombricompuesto","Material que ya pasó la fase termófila, procesado con lombrices.","Etapa final")]
    for c,(title,desc,time) in zip(cols,data):
        with c: st.markdown(f'<div class="card"><div class="kicker">{time}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.caption("Los tiempos son los consignados en el material de investigación y pueden variar según las condiciones de proceso.")
    st.link_button("Abrir la aplicación de compostaje del IPEA", "https://manejo-de-variables-compost-upc-fisica.streamlit.app/", use_container_width=True)
    st.caption("La aplicación enlazada es un recurso complementario independiente; se abre en otra pestaña o ventana según el navegador.")
    st.divider()
    st.markdown("### Explorador conceptual de fases")
    st.write("La curva siguiente es un esquema didáctico, no una serie de mediciones del IPEA. Sirve para relacionar el tiempo transcurrido con las fases habituales mencionadas en la presentación.")
    day = st.slider("Día del proceso (escenario ilustrativo)", 1, 120, 18)
    timeline_x = np.arange(1, 121)
    # Conceptual curve, intentionally labelled illustrative rather than measured.
    timeline_y = 22 + 38*np.exp(-((timeline_x-18)/17)**2) + 18*np.exp(-((timeline_x-38)/27)**2) - 0.08*timeline_x
    timeline_y = np.clip(timeline_y, 20, 65)
    tf = go.Figure(go.Scatter(x=timeline_x, y=timeline_y, mode="lines", line=dict(color="#16836a", width=3), name="Curva conceptual"))
    tf.add_vline(x=day, line_dash="dash", line_color="#d6a73b")
    tf.add_trace(go.Scatter(x=[day], y=[timeline_y[day-1]], mode="markers", marker=dict(size=12, color="#d6a73b"), name="Día seleccionado"))
    tf.update_layout(height=300, margin=dict(l=10,r=10,t=20,b=10), xaxis_title="Día", yaxis_title="Temperatura (°C)", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white")
    st.plotly_chart(tf, use_container_width=True)
    if day < 7:
        phase = "Etapa inicial / mesófila (referencia conceptual)"
    elif day < 35:
        phase = "Posible etapa de mayor actividad térmica (referencia conceptual)"
    elif day < 75:
        phase = "Enfriamiento (referencia conceptual)"
    else:
        phase = "Maduración (referencia conceptual)"
    st.info(f"Día {day}: {phase}. La fase real debe identificarse con mediciones de la pila y criterios técnicos, no solo con el día del proceso.")
    st.markdown("### Del modelo a una pregunta de investigación")
    st.write("¿Qué mediciones harían falta para estimar el calor que una pila podría transferir? Considerá masa, variación de temperatura, duración, pérdidas térmicas y eficiencia del sistema de intercambio.")

elif page == "Propuestas didácticas":
    heading("06 · Transposición didáctica", "Cuatro niveles, un territorio", "Las propuestas responden a brechas y demandas identificadas en el análisis. Son diseños a validar: todavía no se aplicaron en el aula.")
    tabs=st.tabs(["Inicial","Primario","Secundario","Superior"])
    with tabs[0]:
        st.markdown("### Descubriendo la fuerza del Sol, el viento y el agua")
        st.markdown("- **Calor y luz del Sol:** comparar agua al Sol y a la sombra.\n- **Fuerza del viento:** molinillos de papel y preguntas sobre el movimiento.\n- **Agua que empuja:** canaletas y ruedas de paleta.\n- **Salida optativa:** visita al IPEA N.° 211, sujeta a acuerdo institucional.\n\n**Evaluación:** registro de observaciones, portafolio de dibujos y rúbrica cualitativa.")
    with tabs[1]:
        st.markdown("### El circuito energético regional de Cruz del Eje")
        st.markdown("- **Paisaje energético:** mapa y fotografías del dique y de la central.\n- **Maquetas y kits:** depósito, manguera, turbina y LED.\n- **Eficiencia energética:** relevar artefactos en watts y proponer una campaña familiar.\n- **Visita optativa:** comparar la maqueta con la central real.\n\nPrimer ciclo: identificar fuentes. Segundo ciclo: explicar cómo funciona una central.")
    with tabs[2]:
        st.markdown("### Un puente entre Tecnología y Física")
        st.markdown("1. **Tecnología:** diagrama de bloques desde la toma de agua al transformador.\n2. **Física:** potencia hidráulica P = ρ·g·Q·H con H = 28 m y ensayo de Faraday-Lenz.\n3. **Caso IPEA:** compost, bokashi y lombricompuesto como procesos exotérmicos.\n4. **Página web:** cargar temperaturas, calcular calor y simular su recuperación.\n\nEvaluación mediante rúbrica del producto, indicadores de logro y cierre con Padlet o Mentimeter.")
    with tabs[3]:
        st.markdown("### Hidrodinámica, riesgos laborales y gestión ambiental")
        st.markdown("- **Modelización:** Bernoulli con pérdidas y número de Reynolds en la tubería.\n- **Riesgos laborales:** matriz IPERC para la central y el IPEA, riesgos eléctricos, alturas y espacios confinados, y procedimiento LOTO.\n- **Balance de calor:** explorar si el calor del compost podría calentar agua o un invernadero.\n\n**Producto:** proyecto de práctica profesionalizante, con manual de seguridad y auditoría ambiental.")
    st.divider()
    st.markdown("### Recursos digitales")
    st.markdown("- [Aviso ambiental 2026 · Parque Solar Fotovoltaico Cruz del Eje](https://cadenacentro.com/ultimas/audiencia-publica-ambiental-digital-proyecto-parque-solar-fotovoltaico-cruz-del-eje-2/)\n- [Antecedente técnico 2022 · EPEC](https://www.epec.com.ar/docs/imagenes/comunidad/blog/88/ANEXO3_PROYECTOS_PROPUESTOS_POR_EPEC_Convocatoria2022.pdf)\n- [Mapa educativo nacional · IPEA N.º 211](https://mapa.educacion.gob.ar/legajo/140256100)\n- [Central hidroeléctrica Cruz del Eje · EPEC](https://web.epec.com.ar/generacion_central_h_cruz-eje.html)\n- [Ley de Educación Ambiental Integral · Argentina.gob.ar](https://www.argentina.gob.ar/normativa/nacional/ley-27621-350594/texto)")

else:
    heading("07 · Hallazgos", "¿Qué nos dice la investigación?", "Los resultados son exploratorios: la muestra por conveniencia no permite generalizar a todos los docentes o instituciones.")
    cols=st.columns(3)
    with cols[0]: metric_card("Contexto local en documentos", "0", "Documentos que lo mencionan de forma explícita, según el análisis.")
    with cols[1]: metric_card("Contexto local en docentes", "5 de 6", "Docentes que lo usan o lo mencionan en sus clases.")
    with cols[2]: metric_card("Demanda de apoyos", "5 de 6", "Docentes que piden recursos o capacitación didáctica.")
    st.write("")
    labels=["H1 · Profundidad","H2 · Apoyos","H3 · Contexto local","H4 · Articulación"]
    states=["Confirmada parcialmente","Parcialmente sostenida","Confirmada en documentos; no en prácticas","Confirmada parcialmente"]
    for lab,state in zip(labels,states):
        st.markdown(f'<div class="card" style="margin-bottom:.6rem"><b>{lab}</b><br><span class="small-muted">{state}</span></div>',unsafe_allow_html=True)
    st.markdown("### Conclusiones")
    st.markdown("1. La ausencia en el currículo no equivale a ausencia en el aula.\n2. El anclaje local depende de la iniciativa docente y de la institución.\n3. La articulación entre niveles existe donde hay un dispositivo que la sostiene.\n4. Hace falta un recurso con rigor físico: visitas, maquetas y herramientas digitales.")
    st.markdown("### Limitaciones y próximos pasos")
    st.markdown("- La muestra por conveniencia no permite generalizar.\n- Se analizan prácticas declaradas, no observadas.\n- El nivel superior está representado por una sola docente.\n- Las propuestas deben validarse con docentes y la página web debe probarse en una escuela.\n- Próximos pasos: ampliar la muestra y desarrollar guías de actividades por nivel.")

st.divider()
# Navegación secuencial: mantiene el menú lateral y añade un recorrido con flechas.
current_index = pages.index(page)
nav_left, nav_mid, nav_right = st.columns([1, 2, 1])
with nav_left:
    if current_index > 0:
        st.button("← Anterior", use_container_width=True, on_click=set_page, args=(pages[current_index - 1],))
with nav_mid:
    st.markdown(f'<div class="nav-note" style="text-align:center;padding-top:.55rem">Sección {current_index + 1} de {len(pages)} · {page}</div>', unsafe_allow_html=True)
with nav_right:
    if current_index < len(pages) - 1:
        st.button("Siguiente →", use_container_width=True, type="primary", on_click=set_page, args=(pages[current_index + 1],))
st.markdown("<div style='display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#60756d;font-size:.85rem'><span>La energía renovable como contenido escolar</span><span>Profesorado Universitario de Física · UPC · 2026</span></div>",unsafe_allow_html=True)
