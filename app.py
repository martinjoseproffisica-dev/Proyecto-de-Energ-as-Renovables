import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Energía renovable · Cruz del Eje", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --ink:#142b2b; --muted:#55706b; --green:#146b55; --lime:#c9f36b; --paper:#f5f7f1; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
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
    page = st.radio("RECORRIDO", ["Inicio", "La investigación", "Mapa energético local", "Cruz del Eje", "Registro de campo", "Laboratorio hidráulico 3D", "Compostaje y calor", "Propuestas didácticas", "Resultados y conclusiones"], label_visibility="collapsed")
    st.divider()
    st.markdown("**Profesorado Universitario de Física**")
    st.caption("UPC · Sede Cruz del Eje · 2026")
    st.caption("Proyecto académico interactivo")

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
    st.markdown('<div class="callout"><b>Lectura del mapa</b><br>Las ubicaciones del dique y del IPEA se representan con coordenadas publicadas en fuentes cartográficas y educativas. La ubicación exacta de la central Ferroviario debe confirmarse con el relevamiento del equipo antes de fijar un marcador preciso.</div>', unsafe_allow_html=True)
    import pandas as pd
    locations = pd.DataFrame([
        {"Lugar":"Dique Cruz del Eje / Arturo Illia", "Latitud":-30.76194, "Longitud":-64.75248, "Tipo":"Agua y generación", "Detalle":"Embalse asociado al riego y a la generación hidroeléctrica."},
        {"Lugar":"IPEA N.º 211 Presidente Arturo Illia", "Latitud":-30.74969, "Longitud":-64.73899, "Tipo":"Biomasa y educación", "Detalle":"Caso escolar de compost, bokashi y lombricompuesto."},
    ])
    figmap = go.Figure()
    figmap.add_trace(go.Scattermapbox(
        lat=locations["Latitud"], lon=locations["Longitud"], mode="markers+text",
        text=["Dique Arturo Illia", "IPEA N.º 211"], textposition="top right",
        marker=dict(size=[18,15], color=["#167d72", "#d6a73b"]),
        customdata=locations[["Tipo", "Detalle"]].values,
        hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
    ))
    figmap.update_layout(mapbox=dict(style="open-street-map", center=dict(lat=-30.756, lon=-64.746), zoom=12),
                         height=510, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)",
                         legend=dict(orientation="h"))
    st.plotly_chart(figmap, use_container_width=True)
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="card"><div class="kicker">Agua</div><h3>Dique Arturo Illia</h3><p>Un sistema donde el agua cumple funciones de regulación, riego y generación. Es el punto de partida para conversar sobre altura, caudal y potencia.</p><a href="https://www.diquesdecordoba.com.ar/dique-cruz-del-eje/" target="_blank">Consultar ficha del dique ↗</a></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><div class="kicker">Biomasa</div><h3>IPEA N.º 211</h3><p>La investigación incorpora las prácticas de compostaje como oportunidad para estudiar procesos exotérmicos y recuperación de calor.</p><a href="https://mapa.educacion.gob.ar/legajo/140256100" target="_blank">Consultar ficha educativa ↗</a></div>', unsafe_allow_html=True)
    st.markdown("### Central hidroeléctrica Ferroviario")
    st.write("La central es el caso de anclaje del relevamiento físico descrito en el trabajo. Para no presentar una ubicación aproximada como si fuera exacta, el marcador se incorpora cuando el equipo confirme las coordenadas de su visita técnica.")
    st.link_button("Buscar Central Ferroviario en el mapa", "https://www.google.com/maps/search/?api=1&query=Central+Hidroel%C3%A9ctrica+Ferroviario+Cruz+del+Eje")
    st.caption("Fuentes de coordenadas: Mapa Educativo Nacional para IPEA N.º 211 y ficha de Dique Cruz del Eje. La ubicación precisa de la central debe validarse. El mapa es orientativo.")

elif page == "Registro de campo":
    heading("02 · Evidencias del territorio", "Registro de campo", "Fotografías aportadas para documentar la visita a la central hidroeléctrica y al IPEA N.º 211.")
    st.markdown('<div class="callout"><b>Procedencia</b><br>Las imágenes de esta galería provienen del PDF compartido en esta conversación. Se agrupan por el contenido visual observado; los lugares y detalles técnicos deben confirmarse con el equipo antes de la publicación definitiva.</div>', unsafe_allow_html=True)
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
    st.caption("Se incorpora el video enviado como registro audiovisual complementario. Conviene revisar el montaje y recortar los segmentos ajenos al relevamiento antes de usarlo en una exposición académica.")
    st.video("assets/registro_visita.mp4")
    st.markdown("### Para la defensa")
    st.markdown("- Explicar qué se observó directamente durante la visita.\n- Distinguir los datos medidos o informados por personal técnico de los valores usados en las simulaciones.\n- Vincular cada imagen con una pregunta física o didáctica concreta.")

elif page == "Cruz del Eje":
    heading("02 · Anclaje territorial", "Un caso energético real", "El contexto local permite conectar conceptos físicos, infraestructura y decisiones ambientales con lugares cercanos a la comunidad educativa.")
    st.image("https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=1600&q=85", use_container_width=True, caption="Imagen ilustrativa de energía solar; no corresponde necesariamente al parque mencionado en el informe.")
    cols=st.columns(3)
    with cols[0]:
        st.markdown('<div class="card"><div class="kicker">Agua</div><h3>Dique Arturo Illia</h3><p>Recurso vinculado al riego y a la generación hidroeléctrica.</p></div>',unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="card"><div class="kicker">Electricidad</div><h3>Central Ferroviario</h3><p>Caída neta relevada de 28 m y potencia informada de 0,5 MW. Elevación de tensión de 380 V a 13.200 V.</p></div>',unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div class="card"><div class="kicker">Sol</div><h3>Parque solar</h3><p>En construcción al momento descrito en la investigación, cerca de la escuela agrotécnica IPEA N.° 211.</p></div>',unsafe_allow_html=True)
    st.write("")
    st.markdown("### ¿Por qué importa el contexto local?")
    st.write("En el análisis documental, ningún documento menciona explícitamente Cruz del Eje, el dique o EPEC. Sin embargo, cinco de los seis docentes entrevistados usan o mencionan el contexto local. Esto muestra una distancia entre lo prescripto y lo enseñado.")
    st.markdown("### Marco normativo citado en el trabajo")
    st.markdown("- Constitución Nacional, artículo 41.\n- Ley 25.675, General del Ambiente.\n- Ley 27.621, Educación Ambiental Integral.\n- Ley provincial 10.823.\n- Ley 5.589, Código de Aguas de Córdoba.")
    st.caption("Las descripciones de los lugares y sus datos se presentan según el material de la investigación. Conviene verificarlos con fuentes técnicas antes de una publicación institucional.")

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
        # A stylized 3D schematic: water channel, penstock and turbine wheel.
        theta=np.linspace(0,2*np.pi,80)
        z=np.linspace(0,1,14)
        T,Z=np.meshgrid(theta,z)
        R=0.8
        X=R*np.cos(T); Y=R*np.sin(T); ZZ=Z*1.3
        fig=go.Figure()
        fig.add_trace(go.Surface(x=X,y=Y,z=ZZ,opacity=.75,showscale=False,colorscale=[[0,"#b6e3d4"],[1,"#176b59"]],name="Turbina esquemática"))
        # central shaft
        fig.add_trace(go.Scatter3d(x=[0,0],y=[0,0],z=[-0.2,1.7],mode="lines",line=dict(color="#f1bd4b",width=8),name="Eje"))
        # water pipe line to turbine
        fig.add_trace(go.Scatter3d(x=[-2.8,-2.1,-1.2,-.8],y=[0,0,0,0],z=[2.4,2.0,1.3,.8],mode="lines",line=dict(color="#58a9e0",width=12),name="Conducto de agua"))
        for ang in np.linspace(0,2*np.pi,7)[:-1]:
            fig.add_trace(go.Scatter3d(x=[0,0.78*np.cos(ang)],y=[0,0.78*np.sin(ang)],z=[.65,.65],mode="lines",line=dict(color="#f1bd4b",width=5),showlegend=False,hoverinfo="skip"))
        fig.update_layout(height=430,margin=dict(l=0,r=0,t=5,b=0),paper_bgcolor="rgba(0,0,0,0)",scene=dict(xaxis=dict(visible=False),yaxis=dict(visible=False),zaxis=dict(visible=False),aspectmode="data",camera=dict(eye=dict(x=1.8,y=1.7,z=1.25))),legend=dict(orientation="h",y=-.04))
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("#### Explorá el resultado")
    xs=np.linspace(.1,4,50)
    ys=rho*g*xs*h*eff/100/1e6
    f2=go.Figure(go.Scatter(x=xs,y=ys,mode="lines",line=dict(width=3,color="#16836a"),name="Potencia eléctrica estimada"))
    f2.add_trace(go.Scatter(x=[q],y=[p_e],mode="markers",marker=dict(size=12,color="#f1bd4b"),name="Escenario actual"))
    f2.update_layout(height=300,margin=dict(l=10,r=10,t=20,b=10),xaxis_title="Caudal Q (m³/s)",yaxis_title="Potencia (MW)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="white")
    st.plotly_chart(f2,use_container_width=True)
    st.info("Pregunta para el aula: si se duplica el caudal y se mantienen la altura y la eficiencia, ¿qué sucede con la potencia estimada?")

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
    st.markdown("### Recursos digitales para ampliar")
    st.write("La versión publicada puede incorporar enlaces a simuladores, mapas, documentos curriculares, guías de visita y actividades de evaluación. Los enlaces concretos deben revisarse antes de publicar para asegurar que sean pertinentes y estén vigentes.")

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
st.markdown("<div style='display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#60756d;font-size:.85rem'><span>La energía renovable como contenido escolar</span><span>Profesorado Universitario de Física · UPC · 2026</span></div>",unsafe_allow_html=True)
