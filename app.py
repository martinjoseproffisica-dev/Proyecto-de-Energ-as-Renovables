import json
from pathlib import Path
from string import Template

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Energía renovable · Cruz del Eje", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

BASE = Path(__file__).parent
ASSETS = BASE / "assets"

# ───────────────────────── Compatibilidad entre versiones de Streamlit ─────────────────────────
def _version():
    try:
        return tuple(int(x) for x in st.__version__.split(".")[:2])
    except Exception:
        return (1, 40)

STRETCH = {"width": "stretch"} if _version() >= (1, 50) else {"use_container_width": True}


def embed_html(html: str, height: int):
    """Muestra una página HTML con JavaScript (st.iframe en versiones nuevas, components.html en las anteriores)."""
    if hasattr(st, "iframe"):
        st.iframe(html, height=height)
    else:
        import streamlit.components.v1 as components
        components.html(html, height=height)


# ───────────────────────── Datos del equipo ─────────────────────────
TEAM = ["Martín José", "Moreno Florencia", "Saltos Sabrina", "Luna Lizeth", "Heredia Lucas"]
SUBJECTS = ["Metodología de la Investigación", "Educación Ambiental Integral", "Energías Renovables"]
PROFESSORS = ["Naserala Francisco", "Rodríguez Silvana", "Nieto Julieta"]

# ───────────────────────── Temas de color ─────────────────────────
THEMES = {
    "Bosque": dict(icon="🟢", bg="#F5F7F1", surface="#FFFFFF", surface2="#E8F0E9", ink="#142B2B", muted="#55706B", primary="#146B55",
                   primaryInk="#FFFFFF", border="#DCE6DA", accent="#C9F36B", sidebar="#102F2D", sidebarInk="#F4F7ED", calloutBg="#E8F3DD",
                   calloutBar="#78A943", link="#075F88", heroA="9,39,36", heroB="20,107,85", mapStyle="open-street-map", hue="0deg",
                   warn="#D9822B", sceneTop="#e9f1ec", sceneBottom="#b7c9c2", grid="#8fa79e", dark=False,
                   c1="#16836A", c2="#E1A52E", c3="#2864B4"),
    "Océano": dict(icon="🔵", bg="#F0F6FA", surface="#FFFFFF", surface2="#E2EEF6", ink="#0F2638", muted="#4F6A7D", primary="#0B5C8A",
                   primaryInk="#FFFFFF", border="#D3E2EC", accent="#9BE0FF", sidebar="#0B2A42", sidebarInk="#EAF4FB", calloutBg="#DCEBF6",
                   calloutBar="#2F86B8", link="#0B5C8A", heroA="6,32,54", heroB="11,92,138", mapStyle="open-street-map", hue="39deg",
                   warn="#D9822B", sceneTop="#e8f1f8", sceneBottom="#b4c9d8", grid="#8ba5b8", dark=False,
                   c1="#0B7DB5", c2="#E1A52E", c3="#1B4F9C"),
    "Atardecer": dict(icon="🟠", bg="#FBF5EC", surface="#FFFFFF", surface2="#F6E7D3", ink="#2E1B12", muted="#7A5C4A", primary="#B4541A",
                      primaryInk="#FFFFFF", border="#EADBC6", accent="#FFD18A", sidebar="#3A1F14", sidebarInk="#FBEFE2", calloutBg="#FBE6CF",
                      calloutBar="#E08A2E", link="#8A3B0E", heroA="58,24,12", heroB="180,84,26", mapStyle="open-street-map", hue="-141deg",
                      warn="#2A6FB0", sceneTop="#f6ebdc", sceneBottom="#d9bfa3", grid="#b99b80", dark=False,
                      c1="#C4571A", c2="#2A6FB0", c3="#7A3B12"),
    "Lavanda": dict(icon="🟣", bg="#F6F3FB", surface="#FFFFFF", surface2="#ECE6F7", ink="#251A3A", muted="#6B5E86", primary="#5B3FA3",
                    primaryInk="#FFFFFF", border="#E0D8F0", accent="#D8C8FF", sidebar="#2A1B4D", sidebarInk="#F3EEFF", calloutBg="#E9E0F8",
                    calloutBar="#8A63D2", link="#4B2E9A", heroA="34,20,72", heroB="91,63,163", mapStyle="open-street-map", hue="95deg",
                    warn="#D9822B", sceneTop="#efe9f8", sceneBottom="#c9bde0", grid="#a597c4", dark=False,
                    c1="#6B4BC0", c2="#E1A52E", c3="#2864B4"),
    "Coral": dict(icon="🔴", bg="#FFF4F2", surface="#FFFFFF", surface2="#FDE3DE", ink="#3A1A1A", muted="#845650", primary="#C8453A",
                  primaryInk="#FFFFFF", border="#F3D6D0", accent="#FFC1B5", sidebar="#4A1F1B", sidebarInk="#FFEFEA", calloutBg="#FCE0DA",
                  calloutBar="#E26A5A", link="#9B2C22", heroA="74,26,22", heroB="200,69,58", mapStyle="open-street-map", hue="-159deg",
                  warn="#2A6FB0", sceneTop="#fbeae6", sceneBottom="#e3bdb5", grid="#c69a92", dark=False,
                  c1="#C8453A", c2="#2A6FB0", c3="#7A2A22"),
    "Noche": dict(icon="⚫", bg="#0E1A1B", surface="#162A2C", surface2="#1C3436", ink="#E8F1EE", muted="#9DB5AF", primary="#4FD1A5",
                  primaryInk="#06231B", border="#2A4443", accent="#C9F36B", sidebar="#091112", sidebarInk="#E8F1EE", calloutBg="#1C3B37",
                  calloutBar="#4FD1A5", link="#7CC7F2", heroA="4,18,18", heroB="20,107,85", mapStyle="carto-darkmatter", hue="0deg",
                  warn="#F0B24A", sceneTop="#14282a", sceneBottom="#0a1516", grid="#35504f", dark=True,
                  c1="#4FD1A5", c2="#F0B24A", c3="#7CC7F2"),
    "Medianoche": dict(icon="🔷", bg="#0B1220", surface="#131D33", surface2="#1A2742", ink="#E6ECF8", muted="#93A3C2", primary="#5DA9FF",
                       primaryInk="#06142B", border="#24324F", accent="#9BD1FF", sidebar="#070C17", sidebarInk="#E6ECF8", calloutBg="#172A4A",
                       calloutBar="#5DA9FF", link="#8CC4FF", heroA="5,12,30", heroB="30,80,150", mapStyle="carto-darkmatter", hue="49deg",
                       warn="#F0B24A", sceneTop="#14213a", sceneBottom="#080e1b", grid="#2f4468", dark=True,
                       c1="#5DA9FF", c2="#F0B24A", c3="#A78BFA"),
    "Aurora": dict(icon="🟪", bg="#130E22", surface="#1E1634", surface2="#281D45", ink="#EDE8FA", muted="#A99CCB", primary="#B794F6",
                   primaryInk="#1A0F33", border="#33264F", accent="#7EF0D2", sidebar="#0D0817", sidebarInk="#EDE8FA", calloutBg="#2A1F4A",
                   calloutBar="#B794F6", link="#C9B2FF", heroA="19,10,40", heroB="90,50,160", mapStyle="carto-darkmatter", hue="102deg",
                   warn="#F0B24A", sceneTop="#1c1433", sceneBottom="#0c0716", grid="#44366b", dark=True,
                   c1="#B794F6", c2="#7EF0D2", c3="#F0B24A"),
}

PAGES = ["Presentación del equipo", "Inicio", "La investigación", "Documentos y docentes", "Mapa energético local", "Cruz del Eje",
         "Registro de campo", "Laboratorio hidráulico 3D", "Compostaje y calor", "Propuestas didácticas", "Resultados y conclusiones"]

# ───────────────────────── Estado y navegación ─────────────────────────
ss = st.session_state
ss.setdefault("theme", "Bosque")
ss.setdefault("page", PAGES[0])
ss.setdefault("nav_count", 0)
ss.setdefault("scroll_pending", False)
ss.setdefault("bg_level", 5)


def go_to(page):
    """Cambia de sección y pide volver al comienzo de la página."""
    ss["page"] = page
    ss["nav_count"] += 1
    ss["scroll_pending"] = True


def set_theme(name):
    ss["theme"] = name


T = THEMES[ss["theme"]]


def physics_bg(color, level):
    """Mosaico SVG de símbolos y fórmulas de Física, muy tenue, para el fondo de la página."""
    if level <= 0:
        return "none"
    from urllib.parse import quote
    o = level / 100
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='560' height='420' viewBox='0 0 560 420'>
<g fill='none' stroke='{color}' stroke-width='1.5' opacity='{o}'>
<g transform='translate(95,85)'><ellipse rx='46' ry='16'/><ellipse rx='46' ry='16' transform='rotate(60)'/><ellipse rx='46' ry='16' transform='rotate(120)'/><circle r='5' fill='{color}'/><circle cx='46' r='3.5' fill='{color}'/><circle cx='-23' cy='-40' r='3.5' fill='{color}'/></g>
<path d='M210 78 q20 -34 40 0 t40 0 t40 0 t40 0'/>
<path d='M30 205 h22 l8 -15 l14 30 l14 -30 l14 30 l8 -15 h22 M30 205 v-14 M144 205 v-14'/>
<path d='M455 140 L488 250'/><circle cx='490' cy='258' r='11'/><path d='M420 262 Q490 290 560 262' stroke-dasharray='4 6'/>
<rect x='215' y='300' width='84' height='28'/><path d='M257 300 v28'/><path d='M222 298 C165 230 350 230 292 298' stroke-dasharray='5 5'/><path d='M230 298 C190 255 325 255 285 298'/>
<path d='M30 400 Q120 300 215 400' stroke-dasharray='3 7'/>
<path d='M345 190 v50 M345 190 l-6 10 M345 190 l6 10 M335 215 h20'/>
</g>
<g fill='{color}' opacity='{o}' font-family='Georgia, Times, serif' font-style='italic'>
<text x='392' y='68' font-size='24' transform='rotate(-5 392 68)'>E = mc²</text>
<text x='170' y='168' font-size='20' transform='rotate(4 170 168)'>P = ρ·g·Q·H</text>
<text x='40' y='295' font-size='20' transform='rotate(-4 40 295)'>Q = m·c·ΔT</text>
<text x='360' y='345' font-size='20'>F = m·a</text>
<text x='400' y='398' font-size='18' transform='rotate(-3 400 398)'>V = I·R</text>
<text x='238' y='395' font-size='15'>p + ½ρv² + ρgh = cte</text>
<text x='40' y='140' font-size='17' transform='rotate(-8 40 140)'>ε = −ΔΦ/Δt</text>
<text x='380' y='290' font-size='17'>Ec = ½mv²</text>
<text x='455' y='195' font-size='17'>λ = v/f</text>
<text x='222' y='320' font-size='14' stroke='none'>N         S</text>
</g></svg>"""
    return "url(\"data:image/svg+xml;utf8," + quote(svg) + "\")"

# ───────────────────────── Estilos ─────────────────────────
CSS = Template("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --bg:$bg; --surface:$surface; --surface2:$surface2; --ink:$ink; --muted:$muted; --primary:$primary; --primaryInk:$primaryInk;
        --border:$border; --accent:$accent; --callout:$calloutBg; --calloutBar:$calloutBar; --link:$link; --warn:$warn; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background:var(--bg) !important; color:var(--ink) !important; }
[data-testid="stMain"] { background-image:$bgimg !important; background-size:560px 420px !important; background-repeat:repeat !important; }
[data-testid="stHeader"] { background:transparent !important; }
[data-testid="stHeader"] * { color:var(--ink) !important; }
[data-testid="stToolbar"] { opacity:.85; }
.block-container { padding-top:1.1rem !important; max-width:1280px; }
h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.03em; color:var(--ink) !important; }
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p { color:var(--ink) !important; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color:var(--muted) !important; }
[data-testid="stMarkdownContainer"] a, .stMarkdown a { color:var(--link) !important; text-decoration:underline; font-weight:600; }
hr { border-color:var(--border) !important; }

/* Barra lateral */
[data-testid="stSidebar"] { background:$sidebar !important; }
[data-testid="stSidebar"] * { color:$sidebarInk !important; }
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] { background:transparent !important; border:1px solid transparent !important;
    justify-content:flex-start !important; text-align:left; font-weight:500 !important; padding:.35rem .7rem !important; border-radius:10px !important; }
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover { background:rgba(255,255,255,.10) !important; border-color:rgba(255,255,255,.25) !important; }
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] { background:$accent !important; border:1px solid $accent !important;
    justify-content:flex-start !important; text-align:left; font-weight:700 !important; padding:.35rem .7rem !important; border-radius:10px !important; }
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"], [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] * { color:#102F2D !important; }
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.18) !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"], [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color:$sidebarInk !important; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { opacity:.78; }
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] [data-testid="stMarkdownContainer"] p { color:#102F2D !important; }
[data-testid="stSidebar"] button > div { width:100%; justify-content:flex-start !important; text-align:left; }
[data-testid="stSidebar"] button p { text-align:left; }

/* Botones */
.stButton button, .stLinkButton a, [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"] { border-radius:12px !important; font-weight:700 !important; }
[data-testid="stMain"] [data-testid="stBaseButton-secondary"], .stLinkButton a { background:var(--surface) !important; color:var(--ink) !important; border:1px solid var(--border) !important; }
[data-testid="stMain"] [data-testid="stBaseButton-secondary"] *, .stLinkButton a * { color:var(--ink) !important; }
[data-testid="stMain"] [data-testid="stBaseButton-secondary"]:hover, .stLinkButton a:hover { background:var(--surface2) !important; border-color:var(--primary) !important; }
[data-testid="stMain"] [data-testid="stBaseButton-primary"] { background:var(--primary) !important; border:1px solid var(--primary) !important; }
[data-testid="stMain"] [data-testid="stBaseButton-primary"], [data-testid="stMain"] [data-testid="stBaseButton-primary"] * { color:var(--primaryInk) !important; }
[data-testid="stMain"] [data-testid="stBaseButton-primary"]:hover { filter:brightness(1.08); }

/* Controles */
[data-testid="stSlider"] [data-baseweb="slider"] { filter:hue-rotate($hue); }
[data-testid="stSlider"] [data-testid="stTickBarMin"], [data-testid="stSlider"] [data-testid="stTickBarMax"], [data-testid="stSliderThumbValue"], [data-testid="stSlider"] div { color:var(--ink) !important; }
[data-testid="stNumberInput"] input, [data-testid="stTextInput"] input { color:var(--ink) !important; background:var(--surface) !important; }
[data-testid="stNumberInput"] > div > div { background:var(--surface) !important; border-color:var(--border) !important; }
[data-testid="stNumberInput"] button { background:var(--surface2) !important; color:var(--ink) !important; }
[data-testid="stMetricValue"] { color:var(--primary) !important; }
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * { color:var(--muted) !important; }
[data-testid="stAlert"] { background:var(--callout) !important; border:1px solid var(--border) !important; }
[data-testid="stAlert"] * { color:var(--ink) !important; }
[data-testid="stExpander"] { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:14px !important; }
[data-testid="stExpander"] * { color:var(--ink) !important; }
.stTabs [data-baseweb="tab-list"] { gap:.25rem; border-bottom:1px solid var(--border); }
.stTabs [data-baseweb="tab"] { color:var(--muted) !important; font-weight:600; }
.stTabs [aria-selected="true"] { color:var(--primary) !important; }
.stTabs [data-baseweb="tab-highlight"] { background:var(--primary) !important; }
.stTabs [data-baseweb="tab-border"] { background:var(--border) !important; }
[data-testid="stPlotlyChart"], [data-testid="stImage"] img { border-radius:14px; overflow:hidden; }
[data-testid="stIFrame"] iframe, iframe { border:0; border-radius:16px; color-scheme:normal; }
footer { visibility:hidden; }

/* Barra superior compacta con selector de tema */
.topbar-brand { font-size:.8rem; color:var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.topbar-brand b { color:var(--ink); font-family:'Space Grotesk',sans-serif; font-size:.9rem; }
.topline { border-bottom:1px solid var(--border); margin:.2rem 0 1.1rem; }
[data-testid="stPopover"] button { padding:.15rem .6rem !important; min-height:2rem !important; font-size:.82rem !important; background:var(--surface) !important; border:1px solid var(--border) !important; color:var(--ink) !important; border-radius:999px !important; }
[data-testid="stPopover"] button * { color:var(--ink) !important; }
[data-testid="stPopoverBody"] { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:16px !important; min-width:min(620px, 92vw); }
[data-testid="stPopoverBody"] * { color:var(--ink) !important; }
[data-testid="stPopoverBody"] [data-testid="stBaseButton-secondary"] { background:var(--surface2) !important; border:1px solid var(--border) !important; border-radius:10px !important; padding:.2rem .4rem !important; min-height:2rem !important; font-size:.82rem !important; }
[data-testid="stPopoverBody"] [data-testid="stBaseButton-primary"] { background:var(--primary) !important; border:1px solid var(--primary) !important; border-radius:10px !important; padding:.2rem .4rem !important; min-height:2rem !important; font-size:.82rem !important; }
[data-testid="stPopoverBody"] [data-testid="stBaseButton-primary"], [data-testid="stPopoverBody"] [data-testid="stBaseButton-primary"] * { color:var(--primaryInk) !important; }
/* Botón para abrir y cerrar el menú lateral, siempre visible */
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"] button { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:10px !important; }
[data-testid="stExpandSidebarButton"], [data-testid="stExpandSidebarButton"] * { color:var(--ink) !important; }
[data-testid="stSidebarCollapseButton"] button { background:rgba(255,255,255,.12) !important; border-color:rgba(255,255,255,.3) !important; }

/* Componentes propios */
.hero { padding:2.8rem 2.8rem 2.5rem; border-radius:24px; color:#fff; min-height:370px; display:flex; flex-direction:column; justify-content:flex-end;
  background:linear-gradient(110deg,rgba($heroA,.94),rgba($heroB,.65)),url('https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=1800&q=85');
  background-size:cover; background-position:center; }
.hero * { color:#fff !important; }
.hero .eyebrow { color:#d7f69a !important; }
.eyebrow { text-transform:uppercase; letter-spacing:.16em; font-size:.75rem; font-weight:700; color:var(--primary); }
.hero h1 { font-size:clamp(2.5rem,5vw,4.7rem); line-height:.98; max-width:850px; margin:.8rem 0 1rem; }
.hero p { color:#eef7ec !important; font-size:1.12rem; max-width:720px; }
.pill { display:inline-block; padding:.35rem .75rem; border:1px solid rgba(255,255,255,.45); border-radius:99px; font-size:.8rem; margin:.15rem .25rem .15rem 0; }
.card { background:var(--surface); padding:1.15rem 1.3rem; border:1px solid var(--border); border-radius:18px; height:100%; box-shadow:0 6px 24px rgba(0,0,0,.04); }
.card .kicker, .kicker { color:var(--primary); font-size:.74rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; }
.card h3 { margin:.35rem 0 .3rem; font-size:1.18rem; }
.card p { margin:.2rem 0 0; font-size:.95rem; color:var(--ink); }
.card .muted, .small-muted { color:var(--muted); font-size:.88rem; }
.big-number { font-family:'Space Grotesk',sans-serif; font-size:2.2rem; font-weight:700; color:var(--primary); line-height:1.1; }
.section-label { color:var(--primary); font-weight:700; text-transform:uppercase; letter-spacing:.14em; font-size:.75rem; }
.callout { background:var(--callout); border-left:4px solid var(--calloutBar); padding:1rem 1.2rem; border-radius:0 12px 12px 0; color:var(--ink); }
.callout * { color:var(--ink) !important; }
.nav-note { color:var(--muted); font-size:.9rem; }
.name-chip { display:flex; align-items:center; gap:.65rem; background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:.55rem .8rem; font-weight:600; }
.name-chip i { width:30px; height:30px; border-radius:50%; background:var(--primary); color:var(--primaryInk); display:flex; align-items:center; justify-content:center; font-style:normal; font-size:.8rem; flex:none; }
.ph { min-height:260px; border:2px dashed var(--border); border-radius:18px; background:var(--surface2); display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:1.4rem; color:var(--muted); }
.ph b { color:var(--ink); }
table.tbl { width:100%; border-collapse:separate; border-spacing:0; border:1px solid var(--border); border-radius:14px; overflow:hidden; background:var(--surface); font-size:.93rem; }
table.tbl th { background:var(--primary); color:var(--primaryInk); text-align:left; padding:.6rem .8rem; font-weight:700; }
table.tbl td { padding:.6rem .8rem; border-top:1px solid var(--border); color:var(--ink); vertical-align:top; }
table.tbl tr:nth-child(even) td { background:var(--surface2); }
table.tbl td.dim { color:var(--muted); }
.flow { display:flex; flex-wrap:wrap; gap:.6rem; align-items:stretch; }
.flow .step { flex:1 1 150px; background:var(--surface); border:1px solid var(--border); border-top:5px solid var(--primary); border-radius:14px; padding:.75rem .85rem; position:relative; }
.flow .step b { display:block; font-size:.95rem; }
.flow .step span { display:block; font-size:.82rem; color:var(--muted); margin-top:.15rem; }
.flow .step em { display:inline-block; font-style:normal; font-size:.74rem; font-weight:700; background:var(--callout); color:var(--ink); border-radius:99px; padding:.1rem .55rem; margin-top:.4rem; }
.flow .step:not(:last-child):after { content:"→"; position:absolute; right:-.62rem; top:42%; color:var(--primary); font-weight:700; background:var(--bg); border-radius:50%; width:1.1rem; text-align:center; z-index:2; }
.cgrid { display:grid; gap:1rem; margin:0 0 1rem; }
@media (max-width:900px){ .cgrid { grid-template-columns:1fr !important; } }
.badge { display:inline-block; font-size:.72rem; font-weight:700; padding:.12rem .55rem; border-radius:99px; background:var(--callout); color:var(--ink); border:1px solid var(--border); }
.phase { border-radius:16px; padding:1rem 1.2rem; border:1px solid var(--border); background:var(--surface); border-left:8px solid var(--primary); }
.phase h3 { margin:.1rem 0 .3rem; }
</style>
""")
st.markdown(CSS.substitute(bgimg=physics_bg(T["ink"], ss["bg_level"]), **T), unsafe_allow_html=True)

# Al cambiar de sección, la página vuelve al comienzo. El contador cambia el texto del script
# en cada navegación para que el navegador lo ejecute siempre (si el texto fuera idéntico, se reutilizaría).
if ss.pop("scroll_pending", False):
    embed_html(
        """<script>/* nav %d */
        (function(){
          function up(){
            try{
              var d = window.parent.document;
              ['[data-testid="stMain"]','section.main','[data-testid="stAppViewContainer"]','.main'].forEach(function(s){
                var e = d.querySelector(s); if(e){ e.scrollTop = 0; if(e.scrollTo){ e.scrollTo(0,0); } }
              });
              window.parent.scrollTo(0,0);
            }catch(err){}
          }
          up(); [30,120,300,700,1400].forEach(function(t){ setTimeout(up,t); });
        })();
        </script>""" % ss["nav_count"], height=1)

# ───────────────────────── Utilidades de interfaz ─────────────────────────
def heading(kicker, title, desc=None):
    # el número del encabezado es el mismo que el del menú lateral
    kicker = f"{PAGES.index(ss['page']):02d} · {kicker.split('·', 1)[-1].strip()}"
    st.markdown(f'<div class="section-label">{kicker}</div><h1 style="margin-top:.2rem">{title}</h1>', unsafe_allow_html=True)
    if desc:
        st.markdown(desc)


def card_html(kicker, title, body, extra=""):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    return f'<div class="card">{k}<h3>{title}</h3><p>{body}</p>{extra}</div>'


def metric_card(kicker, number, desc):
    return f'<div class="card"><div class="kicker">{kicker}</div><div class="big-number">{number}</div><div>{desc}</div></div>'


def cards(items, cols=None):
    """items: lista de HTML ya armado; se reparten en filas de una grilla de alto parejo."""
    cols = cols or len(items)
    for start in range(0, len(items), cols):
        row = items[start:start + cols]
        st.markdown(f'<div class="cgrid" style="grid-template-columns:repeat({len(row)},minmax(0,1fr))">{"".join(row)}</div>', unsafe_allow_html=True)


def table_html(headers, rows, widths=None):
    ths = "".join(f'<th style="width:{w}%">{h}</th>' if widths else f"<th>{h}</th>" for h, w in zip(headers, widths or headers))
    trs = ""
    for r in rows:
        trs += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return f'<table class="tbl"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>'


def callout(html):
    st.markdown(f'<div class="callout">{html}</div>', unsafe_allow_html=True)


def find_asset(*stems):
    for stem in stems:
        for ext in (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"):
            p = ASSETS / f"{stem}{ext}"
            if p.exists():
                return p
    return None


def photo(stems, caption, missing_title, height=260):
    p = find_asset(*stems)
    if p:
        st.image(str(p), caption=caption, **STRETCH)
    else:
        st.markdown(f'<div class="ph" style="min-height:{height}px"><div style="font-size:2.4rem">🖼️</div><b>{missing_title}</b>'
                    f'<span>Guardá la foto en <b>assets/{stems[0]}.jpg</b></span></div>', unsafe_allow_html=True)


def plot(fig, **kw):
    st.plotly_chart(fig, **STRETCH, **kw)


def base_layout(fig, height=330, **kw):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color=T["ink"], family="DM Sans, sans-serif"), **kw)
    fig.update_layout(title_font_color=T["ink"])
    return fig


# ───────────────────────── Barra lateral y barra superior ─────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Energía renovable")
    st.caption("Investigación educativa · Cruz del Eje")
    for i, p in enumerate(PAGES):
        label = f"{i:02d} · {p}"
        st.button(label, key=f"nav_{i}", on_click=go_to, args=(p,), type="primary" if p == ss["page"] else "secondary", **STRETCH)
    st.divider()
    st.markdown("**Profesorado Universitario de Física**")
    st.caption("UPC · Sede Cruz del Eje · 2026")
    st.caption("Proyecto académico interactivo")

tb_l, tb_r = st.columns([5, 1.25], vertical_alignment="center")
with tb_l:
    st.markdown('<div class="topbar-brand"><b>⚡ La energía renovable como contenido escolar</b><span> · Profesorado Universitario de Física · UPC · 2026</span></div>', unsafe_allow_html=True)
with tb_r:
    with st.popover(f"🎨 Tema · {ss['theme']}", **STRETCH):
        st.caption("Elegí una gama de colores")
        names = list(THEMES.keys())
        for r in range(0, len(names), 4):
            cols = st.columns(4)
            for col, name in zip(cols, names[r:r + 4]):
                with col:
                    st.button(f"{THEMES[name]['icon']} {name}", key=f"theme_{name}", on_click=set_theme, args=(name,),
                              type="primary" if ss["theme"] == name else "secondary", **STRETCH)
        st.slider("Fondo de física (0 = sin fondo)", 0, 20, key="bg_level")
st.markdown('<div class="topline"></div>', unsafe_allow_html=True)

page = ss["page"]

# ═════════════════════════ PÁGINAS ═════════════════════════
def page_portada():
    st.markdown('<div class="eyebrow">00 · Presentación del equipo · Profesorado Universitario de Física · UPC · 4.° año · 2026</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size:clamp(2.2rem,4.6vw,3.9rem);line-height:1.02;margin:.35rem 0 .4rem">La energía renovable como contenido escolar</h1>', unsafe_allow_html=True)
    st.markdown("**Análisis curricular y propuestas de transposición didáctica en Cruz del Eje y Córdoba**")
    st.write("")
    left, right = st.columns([1.3, 1], gap="large")
    with left:
        photo(["equipo_estudiantes"], "Equipo de investigación", "Fotografía del equipo", height=420)
    with right:
        st.markdown('<div class="section-label">Quiénes somos</div>', unsafe_allow_html=True)
        st.markdown("### Equipo de investigación")
        chips = "".join(f'<div class="name-chip"><i>{"".join(w[0] for w in n.split()[:2])}</i>{n}</div>' for n in TEAM)
        st.markdown(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem">{chips}</div>', unsafe_allow_html=True)
        st.write("")
        subj = "".join(f"<li>{s}</li>" for s in SUBJECTS)
        prof = "".join(f"<li>{p}</li>" for p in PROFESSORS)
        st.markdown(f'<div class="card"><div class="kicker">Espacios curriculares</div><ul style="margin:.3rem 0 .6rem;padding-left:1.1rem">{subj}</ul>'
                    f'<div class="kicker">Profesores</div><ul style="margin:.3rem 0 .2rem;padding-left:1.1rem">{prof}</ul></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="callout"><b>Universidad Provincial de Córdoba</b><br>Profesorado Universitario de Física · Sede Cruz del Eje · 4.° año · 2026</div>', unsafe_allow_html=True)
    st.write("")
    st.button("Comenzar la presentación →", type="primary", on_click=go_to, args=("Inicio",), **STRETCH)


def page_inicio():
    st.markdown("""<div class="hero"><div class="eyebrow">01 · Inicio · Investigación · Educación · Territorio</div>
<h1>La energía renovable como contenido escolar</h1>
<p>Análisis curricular y propuestas de transposición didáctica en Cruz del Eje y Córdoba.</p>
<div><span class="pill">Inicial</span><span class="pill">Primario</span><span class="pill">Secundario</span><span class="pill">Superior</span></div></div>""", unsafe_allow_html=True)
    st.write("")
    st.markdown("### Una investigación que conecta el aula con el territorio")
    st.markdown("El proyecto analiza cómo se enseñan las energías renovables en los documentos curriculares y en las prácticas docentes, y qué brechas existen frente al conocimiento físico del potencial energético local.")
    cards([metric_card("Caso de estudio", "Cruz del Eje", "Dique, central hidroeléctrica y parque solar."),
           metric_card("Trabajo de campo", "6 docentes", "Entrevistas a docentes de cuatro niveles educativos."),
           metric_card("Producto", "4 propuestas", "Una propuesta didáctica para cada nivel educativo.")])
    callout("<b>Idea central</b><br>La ausencia del contexto local en los documentos curriculares no equivale a su ausencia en el aula: su incorporación depende, en gran medida, de la iniciativa docente y de los recursos disponibles.")
    st.write("")
    st.markdown("### Explorar el proyecto")
    cards([card_html("Explorar", "01 · Investigación", "Pregunta, objetivos, marco teórico, hipótesis y método."),
           card_html("Explorar", "02 · Territorio", "Mapa energético local, fotos y recursos del caso."),
           card_html("Explorar", "03 · Laboratorios", "Turbina 3D y compostaje: dos simulaciones para razonar con la Física.")])
    st.markdown("### Ir directamente a una sección")
    cols = st.columns(4)
    for col, label, target in zip(cols, ["Ver el mapa local", "Abrir el laboratorio hidráulico", "Explorar compostaje y calor", "Ver los resultados"],
                                  ["Mapa energético local", "Laboratorio hidráulico 3D", "Compostaje y calor", "Resultados y conclusiones"]):
        with col:
            st.button(label, key=f"jump_{target}", on_click=go_to, args=(target,), **STRETCH)


def page_investigacion():
    heading("01 · El proyecto", "¿Cómo se enseñan las energías renovables?",
            "La investigación compara lo que prescriben los documentos, lo que declaran los docentes y el conocimiento físico del potencial energético local.")
    tabs = st.tabs(["Pregunta y objetivos", "Marco teórico", "Antecedentes", "Hipótesis", "Método"])
    with tabs[0]:
        st.markdown("### Pregunta de investigación")
        callout("¿Cómo se enseñan las energías renovables en los documentos curriculares y en las prácticas docentes de los cuatro niveles, y qué brechas hay frente al conocimiento físico del potencial energético local?")
        st.caption("Inicial · Primario · Secundario · Superior/universitario, con Cruz del Eje como caso de anclaje.")
        st.write("")
        st.markdown("#### Objetivo general")
        st.write("Analizar cómo se enseñan las energías renovables en los documentos y en las percepciones docentes de los cuatro niveles, identificar brechas frente al conocimiento físico local y elaborar propuestas de transposición didáctica.")
        st.markdown("#### Objetivos específicos")
        objs = ["Analizar presencia, profundidad y continuidad en los documentos.", "Relevar concepciones, apoyos y dificultades de los docentes.",
                "Evaluar la presencia del contexto energético local.", "Analizar la coherencia vertical entre niveles.",
                "Diseñar propuestas de transposición didáctica por nivel."]
        cards([f'<div class="card"><div class="big-number" style="font-size:1.6rem">{i+1}</div><p>{o}</p></div>' for i, o in enumerate(objs)], cols=5)
    with tabs[1]:
        st.markdown("### Los tres saberes de Chevallard como estructura")
        cards([card_html("Saber sabio", "Visita técnica", "Visita a la central «Ferroviario» y pliego de EPEC."),
               card_html("Saber a enseñar", "Documentos curriculares", "Progresiones de Aprendizaje de Ciencias Naturales y Tecnología, y plan de la Licenciatura en HST."),
               card_html("Saber enseñado", "Prácticas docentes", "Entrevistas a seis docentes de los cuatro niveles.")])
        fig = find_asset("figura_saberes")
        if fig:
            st.image(str(fig), caption="Figura 1. Los tres saberes y los instrumentos con los que se los estudió.", **STRETCH)
        st.markdown("### Tres ejes completan el marco")
        cards([card_html("Eje 1", "Alfabetización científica y enfoque CTSA", "Enseñar energía con sus implicancias sociales, tecnológicas y ambientales."),
               card_html("Eje 2", "Enseñanza contextualizada y aprendizaje situado", "El contenido cobra sentido cuando parte del entorno cercano de los estudiantes."),
               card_html("Eje 3", "Articulación curricular vertical", "Progresión entre niveles, sin rupturas ni repeticiones sin articular.")])
    with tabs[2]:
        st.markdown("### Lo que ningún antecedente combina")
        items = ["Energía y energías renovables como contenido escolar", "Comparación de tres o más niveles educativos",
                 "Un caso energético local real, visitado y documentado", "El esquema de los tres saberes de Chevallard", "Articulación vertical entre niveles"]
        cards([f'<div class="card"><div class="big-number" style="font-size:1.6rem">{i+1}</div><p>{t}</p></div>' for i, t in enumerate(items)], cols=5)
        st.caption("De diez antecedentes (2018 a 2024) predominan las propuestas genéricas; escasean las ancladas en un caso local.")
    with tabs[3]:
        st.markdown("### Cuatro hipótesis específicas")
        cards([card_html("H1", "Profundidad y continuidad", "Las renovables aparecen de forma esporádica y poco profunda, sin progresión clara entre años."),
               card_html("H2", "Apoyos y demandas", "Los docentes se apoyan en contenidos generales y piden recursos y capacitación."),
               card_html("H3", "Contexto local", "El dique y el parque solar están casi ausentes de documentos y prácticas."),
               card_html("H4", "Articulación vertical", "Se repiten contenidos básicos sin profundización progresiva entre niveles.")], cols=2)
        st.button("Ver cómo se contrastaron →", key="to_res", on_click=go_to, args=("Resultados y conclusiones",))
    with tabs[4]:
        st.markdown("### Diseño: documentos, entrevistas y visitas")
        cards([card_html("Documentos", "Análisis documental", "Progresiones de Ciencias Naturales, Educación Tecnológica y Computación, y plan de la Lic. en HST. Matriz de cinco categorías."),
               card_html("Entrevistas", "Seis docentes", "Uno de inicial, uno de primario, tres de secundario y uno de superior. Semiestructuradas, de 15 a 20 minutos, anónimas y con código por docente."),
               card_html("Visitas", "Central e IPEA", "Central «Ferroviario», con entrevista a un técnico, e IPEA N.° 211, con entrevista a un docente.")])
        st.caption("Investigación cualitativa exploratoria, con muestra por conveniencia.")


def page_documentos():
    heading("02 · Evidencias", "Lo prescripto y lo enseñado", "Qué dicen los documentos y qué cuentan los docentes sobre la energía en cada nivel.")
    tabs = st.tabs(["Currículo", "Docentes", "Prescripto vs. enseñado"])
    with tabs[0]:
        st.markdown("### Qué dicen los documentos")
        st.markdown(table_html(["Categoría", "Hallazgo principal"], [
            ["<b>Presencia</b>", "Explícita desde 6.° grado y en el Ciclo Orientado; ausente en Inicial y casi ausente en el plan universitario."],
            ["<b>Profundidad</b>", "Crece con el nivel: se nombra, luego se cuantifica y se contextualiza."],
            ["<b>Enfoque</b>", "CTS en primaria y secundaria; seguridad e higiene laboral en el plan universitario."],
            ["<b>Contexto local</b>", "Ningún documento lo menciona de forma explícita."],
            ["<b>Articulación vertical</b>", "Progresión identificable pero fragmentada; sin vínculo entre Física y Tecnología."]], widths=[24, 76]), unsafe_allow_html=True)
        st.write("")
        st.markdown("### Dónde aparece la energía en el currículo")
        st.markdown(table_html(["Nivel", "Ciencias Naturales y Física", "Tecnología"], [
            ["<b>Inicial</b>", "Ausente; eje precursor sobre transformaciones", "Ausente"],
            ["<b>Primaria 6.°</b>", "Modos de generar energía eléctrica", "Tipos de energía y clasificación de fuentes"],
            ["<b>Secundaria 1.°</b>", "Problematización del uso de fuentes", "Energía como insumo o salida"],
            ["<b>Secundaria 2.°</b>", "—", "Lo más desarrollado: centrales hidroeléctricas y eólicas"],
            ["<b>Secundaria 5.°</b>", "Inducción en dínamos y generadores", "—"]], widths=[20, 40, 40]), unsafe_allow_html=True)
        st.write("")
        st.markdown("### En la Licenciatura en HST la energía casi no aparece")
        cards([card_html("1.° año · Física", "Hidrostática e Hidrodinámica", "La base de «Ferroviario», sin mención de energía ni de generación."),
               card_html("3.° año", "Inducción y balances", "Inducción de Faraday y Lenz sin aplicarla a la generación; balances de energía en sentido industrial."),
               card_html("4.° año y plan completo", "Sostenibilidad general", "Ningún espacio nombra Cruz del Eje ni el dique.")])
        callout("<b>Hallazgo transversal.</b> Ciencias Naturales y Tecnología clasifican las fuentes en el mismo grado, 6.° de primaria, pero desde ángulos distintos y sin coordinación visible.")
    with tabs[1]:
        st.markdown("### Voces docentes por nivel")
        lv = st.tabs(["Inicial y primario", "Secundario", "Superior"])
        with lv[0]:
            cards([card_html("Inicial", "Explorar antes de nombrar",
                             "Anticipar y comprobar con objetos cotidianos.<br><b>Contexto:</b> escuela rural y parques solares.<br><b>Dificultad:</b> concepciones previas y tiempo.<br><b>Pide:</b> materiales sencillos, recursos visuales y capacitación."),
                   card_html("Primario · 1.° grado", "Sol, agua y viento",
                             "Experimentos simples.<br><b>Contexto:</b> el dique y fotos auténticas del paisaje, sin visitas.<br><b>Dificultad:</b> abstracción y falta de kits.<br><b>Pide:</b> kits itinerantes con maquetas, guías regionales y talleres.")])
            st.caption("En ambos niveles lo enseñado excede o se adelanta a lo prescripto.")
        with lv[1]:
            cards([card_html("D-SEC · técnica, 6.° año", "Contenido central y cuantitativo", "Enfoque CTS. Sin visitas ni datos locales; quiere visitar.<br><b>Dificultad:</b> el tiempo."),
                   card_html("D-SEC2 · Física, 1.° y 5.°", "Teoría con énfasis ambiental", "Salida al dique y a la planta potabilizadora. Única docente de Física: sostiene la continuidad."),
                   card_html("D-SEC3 · técnica, 5.° y 6.°", "Eje propio en 6.°", "Solar con equipo real; visitas a la central y moto eléctrica en la feria.<br><b>Falta:</b> material para eólica y mareomotriz.")])
            st.caption("El contenido es sistemático; la brecha está en el anclaje local y en los recursos de modelización.")
        with lv[2]:
            cards([card_html("Lo que declara D-UNI", "Fuentes por separado",
                             "Trabaja energía solar, eólica, hidráulica y biomasa. Se apoya en imágenes, videos y simuladores. Menciona el dique y los parques solares, sin profundizar ni visitar. Los estudiantes llegan con conocimientos previos dispares. <b>Pide:</b> equipos didácticos, simuladores y visitas."),
                   card_html("Brecha", "Doble", "Experimental, por falta de equipos y mediciones directas, y de anclaje local.")])
        st.markdown("### Saber enseñado, nivel por nivel")
        st.markdown(table_html(["Nivel", "Energía en el aula", "Qué demandan"], [
            ["<b>Inicial</b>", "Idea emergente de los fenómenos; excede lo prescripto", "Materiales sencillos, recursos visuales y locales"],
            ["<b>Primario</b>", "Sol, agua y viento desde 1.° grado, antes que el currículo", "Kits itinerantes con maquetas y guías regionales"],
            ["<b>Secundario</b>", "Contenido sistemático; contexto local en dos de tres docentes", "Planos de maquetas, salidas y capacitación"],
            ["<b>Superior</b>", "Fuentes por separado, teórico y con simuladores", "Equipos didácticos, simuladores y visitas"]], widths=[16, 44, 40]), unsafe_allow_html=True)
    with tabs[2]:
        st.markdown("### Lo prescripto y lo enseñado no coinciden")
        cards([metric_card("Documentos", "0", "mencionan de forma explícita el contexto local."),
               metric_card("Docentes", "5 de 6", "usan o mencionan el contexto local en sus clases."),
               metric_card("Demanda", "5 de 6", "piden recursos o capacitación didáctica.")])
        callout("<b>La ausencia en el currículo no equivale a ausencia en el aula.</b>")


def page_mapa():
    heading("03 · Territorio", "Mapa energético local", "Un mapa de referencia para conectar la investigación con los lugares que la hacen concreta.")
    locations = pd.DataFrame([
        {"Lugar": "Dique Cruz del Eje / Arturo Illia", "Latitud": -30.76194, "Longitud": -64.75248, "Tipo": "Agua y generación", "Detalle": "Embalse asociado al riego y a la generación hidroeléctrica."},
        {"Lugar": "IPEA N.º 211 Presidente Arturo Illia", "Latitud": -30.74969, "Longitud": -64.73899, "Tipo": "Biomasa y educación", "Detalle": "Institución educativa vinculada al relevamiento sobre compostaje."},
        {"Lugar": "Central hidroeléctrica El Ferroviario (EPEC)", "Latitud": -30.74950, "Longitud": -64.79675, "Tipo": "Generación hidroeléctrica", "Detalle": "Ubicación identificada mediante el código de mapa 7623+68."},
        {"Lugar": "Parque Solar Fotovoltaico Cruz del Eje (expediente ambiental 2026)", "Latitud": -30.746833, "Longitud": -64.727333, "Tipo": "Energía solar fotovoltaica",
         "Detalle": "Coordenadas publicadas en el aviso de proyecto ambiental de 2026: Pedanía San Marcos, fuera del ejido urbano."},
    ])
    fig = go.Figure()
    fig.add_trace(go.Scattermap(
        lat=locations["Latitud"], lon=locations["Longitud"], mode="markers+text",
        text=["Dique Arturo Illia", "IPEA N.º 211", "Central El Ferroviario", "Parque solar · proyecto 2026"], textposition="top right",
        textfont=dict(size=13, color="#111111" if not T["dark"] else "#ffffff"),
        marker=dict(size=[19, 16, 18, 17], color=[T["c1"], T["c2"], T["c3"], "#E1A52E"]),
        customdata=locations[["Tipo", "Detalle"]].values,
        hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>%{customdata[1]}<extra></extra>"))
    fig.update_layout(map=dict(style=T["mapStyle"], center=dict(lat=-30.753, lon=-64.763), zoom=10.5), height=520, margin=dict(l=0, r=0, t=0, b=0),
                      paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
    plot(fig)
    a, b = st.columns(2, gap="large")
    with a:
        photo(["dique_cruz_del_eje", "dique"], "Dique Arturo Illia (Cruz del Eje)", "Foto del dique", height=240)
        st.markdown(card_html("Agua", "Dique Arturo Illia", "Un sistema donde el agua cumple funciones de regulación, riego y generación. Es el punto de partida para conversar sobre altura, caudal y potencia.",
                              '<a href="https://www.diquesdecordoba.com.ar/dique-cruz-del-eje/" target="_blank">Consultar ficha del dique ↗</a>'), unsafe_allow_html=True)
    with b:
        photo(["ipea_211", "ipea"], "IPEA N.º 211 «Presidente Arturo Illia»", "Foto del IPEA N.º 211", height=240)
        st.markdown(card_html("Biomasa", "IPEA N.º 211", "La investigación incorpora las prácticas de compostaje como oportunidad para estudiar procesos exotérmicos y recuperación de calor.",
                              '<a href="https://mapa.educacion.gob.ar/legajo/140256100" target="_blank">Consultar ficha educativa ↗</a>'), unsafe_allow_html=True)
    st.markdown("### Central hidroeléctrica El Ferroviario")
    st.write("El punto de El Ferroviario corresponde al código de ubicación 7623+68. Para el parque solar se prioriza la ubicación informada en el aviso de proyecto ambiental de 2026: Pedanía San Marcos, fuera del ejido urbano de Cruz del Eje.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("Abrir El Ferroviario en Google Maps", "https://www.google.com/maps/search/?api=1&query=7623%2B68%20Cruz%20del%20Eje%2C%20C%C3%B3rdoba", **STRETCH)
    with c2:
        st.link_button("Aviso ambiental 2026 del parque solar", "https://cadenacentro.com/ultimas/audiencia-publica-ambiental-digital-proyecto-parque-solar-fotovoltaico-cruz-del-eje-2/", **STRETCH)
    with c3:
        st.link_button("Antecedente técnico de EPEC (2022)", "https://www.epec.com.ar/docs/imagenes/comunidad/blog/88/ANEXO3_PROYECTOS_PROPUESTOS_POR_EPEC_Convocatoria2022.pdf", **STRETCH)
    st.caption("Hay una diferencia entre la ubicación consignada en el documento de EPEC de 2022 (frente a la central hidroeléctrica) y la ubicación del expediente ambiental difundido en 2026. El mapa muestra la ubicación más reciente publicada y conserva el antecedente como fuente de contexto.")


def page_cruz():
    heading("04 · Anclaje territorial", "Un caso energético real", "El contexto local permite conectar conceptos físicos, infraestructura y decisiones ambientales con lugares cercanos a la comunidad educativa.")
    a, b = st.columns(2, gap="large")
    with a:
        photo(["ingreso_cruz_del_eje", "ingreso"], "Ingreso a la ciudad de Cruz del Eje", "Foto del ingreso a Cruz del Eje", height=300)
    with b:
        photo(["dique_cruz_del_eje", "dique"], "Dique Arturo Illia", "Foto del dique", height=300)
    st.write("")
    cards([card_html("Agua", "Dique Arturo Illia", "Recurso vinculado al riego y a la generación hidroeléctrica."),
           card_html("Electricidad", "Central Ferroviario", "Caída neta relevada de 28 m y potencia informada de 0,5 MW. Elevación de tensión de 380 V a 13.200 V."),
           card_html("Sol", "Parque solar fotovoltaico",
                     "El aviso ambiental difundido en 2026 ubica el proyecto en Pedanía San Marcos, fuera del ejido urbano de Cruz del Eje. La documentación de EPEC de 2022 consignaba un emplazamiento distinto.",
                     '<a href="https://cadenacentro.com/ultimas/audiencia-publica-ambiental-digital-proyecto-parque-solar-fotovoltaico-cruz-del-eje-2/" target="_blank">Consultar aviso ambiental 2026 ↗</a>')])
    st.markdown("### De la toma de agua a la red: la central «Ferroviario»")
    st.markdown("""<div class="flow">
<div class="step"><b>Toma de agua</b><span>El agua del dique entra al sistema.</span><em>Energía potencial</em></div>
<div class="step"><b>Tubería de presión</b><span>Caída neta de 28 m.</span><em>Presión y velocidad</em></div>
<div class="step"><b>Turbina</b><span>El agua empuja el rodete.</span><em>Energía mecánica</em></div>
<div class="step"><b>Generador</b><span>0,5 MW a 380 V.</span><em>Inducción de Faraday</em></div>
<div class="step"><b>Transformador</b><span>380 V → 13.200 V, hacia la red de EPEC.</span><em>Menos pérdidas por efecto Joule</em></div></div>""", unsafe_allow_html=True)
    st.write("")
    st.button("Probar la turbina en el laboratorio 3D →", key="to_lab", on_click=go_to, args=("Laboratorio hidráulico 3D",))
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
    fig = find_asset("figura_normativa")
    if fig:
        st.image(str(fig), caption="Figura 2. Cadena normativa que respalda el proyecto.", **STRETCH)


def page_registro():
    heading("05 · Evidencias del territorio", "Registro de campo", "Fotografías aportadas para documentar la visita a la central hidroeléctrica y al IPEA N.º 211.")
    tabs = st.tabs(["Central Ferroviario", "IPEA N.º 211", "Video de la visita"])

    def gallery(rng, intro):
        st.write(intro)
        files = [(i, ASSETS / f"relevamiento_{i:02d}.jpg") for i in rng]
        files = [(i, p) for i, p in files if p.exists()]
        if not files:
            st.info("Todavía no hay fotos en la carpeta assets (relevamiento_XX.jpg).")
            return
        cols = st.columns(3)
        for n, (i, p) in enumerate(files):
            with cols[n % 3]:
                st.image(str(p), caption=f"Registro de campo · imagen {i}", **STRETCH)

    with tabs[0]:
        gallery(range(1, 11), "Equipamiento, turbinas, instrumentos y sectores de la instalación registrados durante el relevamiento.")
    with tabs[1]:
        gallery(range(11, 21), "Espacios de la institución educativa, invernadero y pilas de material orgánico incluidos en el registro fotográfico.")
    with tabs[2]:
        st.caption("Registro audiovisual de la visita técnica.")
        v = ASSETS / "registro_visita.mp4"
        if v.exists():
            st.video(str(v))
        else:
            st.info("El video todavía no está en la carpeta assets (registro_visita.mp4).")


@st.cache_data(show_spinner=False)
def _turbine_template():
    return (BASE / "componentes" / "turbina3d.html").read_text(encoding="utf-8")


def turbine_html():
    cfg = dict(css=dict(bg=T["bg"], surface=T["surface"], ink=T["ink"], muted=T["muted"], primary=T["primary"], primaryInk=T["primaryInk"],
                        border=T["border"], accent=T["accent"], warn=T["warn"]),
               scene=dict(top=T["sceneTop"], bottom=T["sceneBottom"], grid=T["grid"]), defaults=dict(H=28, Q=2.3, eff=80))
    return _turbine_template().replace("__CONFIG__", json.dumps(cfg))


def page_laboratorio():
    heading("06 · Simulación interactiva", "Laboratorio hidráulico",
            "Mové las variables y mirá cómo cambian el distribuidor, el recorrido del agua y la potencia. Arrastrá el modelo para girarlo y usá la rueda para acercarte.")
    callout("<b>Modelo idealizado.</b> La potencia hidráulica disponible se estima con P = ρ · g · Q · H. La potencia eléctrica depende además de la eficiencia del sistema. "
            "Con H = 28 m, Q = 2,3 m³/s y 80 % el modelo da cerca de 0,5 MW, la potencia informada para «El Ferroviario»; el caudal y la eficiencia son supuestos, no mediciones de la central.")
    st.write("")
    embed_html(turbine_html(), height=800)
    st.write("")
    st.markdown("### Qué mirar")
    cards([card_html("1 · Potencia y caudal", "Proporcionales", "Con H y eficiencia fijas, al duplicar el caudal se duplica la potencia: la recta del gráfico lo muestra."),
           card_html("2 · El distribuidor", "Regula el caudal", "Al subir Q, las palas directrices se abren. Cerradas, la máquina se detiene aunque haya altura."),
           card_html("3 · Giro constante", "Sincronismo", "En una central conectada a la red el rodete gira siempre a la misma velocidad: cambia la potencia, no las vueltas."),
           card_html("4 · Eficiencia", "Lo que no se aprovecha", "La barra naranja es potencia que se pierde por rozamiento, remolinos y calor en el generador.")], cols=4)
    with st.expander("Preguntas para explorar con la simulación"):
        st.markdown("1. ¿Qué pasa con la potencia si H pasa de 28 m a 14 m y el caudal no cambia? ¿Y si el caudal se reduce a la mitad?\n"
                    "2. ¿Qué caudal haría falta para obtener 1 MW con H = 28 m y una eficiencia del 80 %?\n"
                    "3. Si la eficiencia baja de 80 % a 60 %, ¿cuántos kWh se pierden cada hora?\n"
                    "4. ¿Por qué conviene transformar la tensión de 380 V a 13.200 V para transportar la energía?")
    st.caption("Modelo 3D realizado con three.js. Necesita conexión a internet y un navegador con WebGL.")


# ── Compostaje ──
_CURVE = np.array([[0, 20], [3, 38], [6, 52], [9, 60], [14, 62], [20, 58], [26, 50], [32, 42], [40, 32], [50, 26], [70, 22], [90, 20]], float)
_DAYS = np.arange(0, 91)
_RAW = np.interp(_DAYS, _CURVE[:, 0], _CURVE[:, 1])
_PAD = np.pad(_RAW, 4, mode="edge")
CURVE_T = np.convolve(_PAD, np.ones(7) / 7, mode="same")[4:-4]
CURVE_T[0] = 20.0
PEAK_DAY = int(np.argmax(CURVE_T))


def phase_of(day, temp):
    if day <= PEAK_DAY:
        if temp < 40:
            return 0
        return 1 if temp < 55 else 2
    if temp >= 55:
        return 2
    if temp >= 40:
        return 1
    return 3 if day < 50 else 4


PHASES = [
    ("Fase mesófila", "#3C8DBC", "Por debajo de 40 °C", "Los microorganismos consumen los materiales más fáciles de degradar y liberan calor: la pila empieza a entibiarse."),
    ("Fase termófila", "#E0B02E", "Entre 40 y 55 °C", "Dominan los microorganismos que toleran el calor. Es la etapa de mayor actividad y de mayor descomposición."),
    ("Higienización", "#E8833A", "Entre 55 y 65 °C", "Con estas temperaturas sostenidas se reducen patógenos y semillas de malezas. Hay que cuidar que no se seque la pila."),
    ("Enfriamiento", "#5BA7A0", "La temperatura baja", "Se agota el material fácil de degradar, disminuye la actividad y la pila se enfría."),
    ("Maduración", "#8A6D4B", "Cerca de la temperatura ambiente", "El material se estabiliza y se transforma en un abono maduro (humus)."),
]


def pile_figure(t_core, mass):
    s = (mass / 1000) ** (1 / 3)
    w, hp = 1.7 * s, 1.15 * s
    xs, ys = np.linspace(-2.5, 2.5, 120), np.linspace(0, 1.9, 70)
    X, Y = np.meshgrid(xs, ys)
    rho = ((np.abs(X) / w) ** 2.6 + (Y / hp) ** 2.6) ** (1 / 2.6)
    f = 0.06 + 0.94 * np.clip((1 - rho) / 0.5, 0, 1) ** 0.7
    Z = np.where(rho <= 1, 20 + (t_core - 20) * f, np.nan)
    colors = [[0, "#2B6CB0"], [0.2, "#38B2AC"], [0.4, "#9AD36A"], [0.55, "#ECC94B"], [0.75, "#ED8936"], [1, "#E53E3E"]]
    fig = go.Figure(go.Heatmap(x=xs, y=ys, z=Z, zmin=15, zmax=70, colorscale=colors, zsmooth="best", hovertemplate="%{z:.0f} °C<extra></extra>",
                               colorbar=dict(title=dict(text="°C", font=dict(color=T["ink"])), thickness=12, len=0.85, tickfont=dict(color=T["ink"]))))
    fig.add_shape(type="rect", x0=-2.5, x1=2.5, y0=-0.25, y1=0, fillcolor="#6B4F36", line=dict(width=0), layer="below")
    fig.add_annotation(x=0, y=hp * 0.5, text=f"<b>Núcleo: {t_core:.0f} °C</b>", showarrow=False, font=dict(color="#ffffff", size=15), bgcolor="rgba(0,0,0,.38)", borderpad=4)
    fig.add_annotation(x=-2.45, y=1.8, text="Aire: 20 °C", showarrow=False, xanchor="left", font=dict(color=T["muted"], size=12))
    base_layout(fig, height=380, title=dict(text="Corte de la pila (esquema)", font=dict(size=15)))
    fig.update_xaxes(visible=False, range=[-2.5, 2.5])
    fig.update_yaxes(visible=False, range=[-0.25, 1.9], scaleanchor="x", scaleratio=1)
    return fig


def curve_figure(day):
    fig = go.Figure()
    bands = [(15, 40, "#3C8DBC", "Mesófila"), (40, 55, "#E0B02E", "Termófila"), (55, 65, "#E8833A", "Higienización"), (65, 72, "#D64545", "Exceso")]
    for y0, y1, c, name in bands:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=c, opacity=0.14, line_width=0)
        fig.add_annotation(x=89, y=(y0 + y1) / 2, text=name, showarrow=False, xanchor="right", font=dict(size=11, color=T["muted"]))
    fig.add_trace(go.Scatter(x=_DAYS, y=CURVE_T, mode="lines", line=dict(width=4, color=T["c1"]), name="Temperatura del núcleo", hovertemplate="Día %{x}: %{y:.0f} °C<extra></extra>"))
    fig.add_vline(x=day, line_dash="dash", line_color=T["warn"])
    fig.add_trace(go.Scatter(x=[day], y=[CURVE_T[day]], mode="markers", marker=dict(size=14, color=T["warn"], line=dict(color="#fff", width=2)), showlegend=False, hoverinfo="skip"))
    base_layout(fig, height=360, showlegend=False, title=dict(text="Curva ilustrativa de temperatura (no son mediciones)", font=dict(size=15)))
    fig.update_xaxes(title="Día del proceso", range=[0, 90], gridcolor=T["border"], zeroline=False)
    fig.update_yaxes(title="Temperatura (°C)", range=[15, 72], gridcolor=T["border"], zeroline=False)
    return fig


def page_compost():
    heading("07 · Biomasa y energía térmica", "Compostaje y calor",
            "Explorá las fases de una pila de compost y diferenciá el calor que libera de la energía que realmente se podría recuperar.")
    st.markdown("La investigación describe que en la escuela se mide la temperatura de las pilas, pero no se registra directamente el calor liberado. Por eso las simulaciones de esta sección son ejercicios didácticos: **sirven para razonar con la Física, no son mediciones del IPEA.**")
    st.markdown("### Tres procesos estudiados en el IPEA")
    cards([card_html("Entre 3 y 6 meses", "Compost", "Estiércol, paja y restos vegetales."),
           card_html("Alrededor de 20 días", "Bokashi", "Materiales similares, con levadura, azúcar y polvillo de maíz."),
           card_html("Etapa final", "Lombricompuesto", "Material que ya pasó la fase termófila, procesado con lombrices.")])
    st.caption("Los tiempos son los consignados en el material de investigación y pueden variar según las condiciones del proceso.")
    st.link_button("Abrir la aplicación de compostaje del IPEA", "https://manejo-de-variables-compost-upc-fisica.streamlit.app/", **STRETCH)
    st.caption("La aplicación enlazada es un recurso complementario independiente; se abre en otra pestaña o ventana según el navegador.")
    st.divider()

    st.markdown("### Simulador: ¿qué pasa dentro de la pila?")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        day = st.slider("Día del proceso", 0, 90, 14, key="comp_day")
    with c2:
        mass = st.slider("Masa de la pila (kg)", 200, 2500, 1000, 100, key="comp_mass")
    t_core = float(CURVE_T[day])
    ph = PHASES[phase_of(day, t_core)]
    left, right = st.columns([1, 1], gap="large")
    with left:
        plot(pile_figure(t_core, mass))
    with right:
        plot(curve_figure(day))
    st.markdown(f'<div class="phase" style="border-left-color:{ph[1]}"><div class="kicker">Día {day} · {ph[2]}</div><h3>{ph[0]}</h3><p>{ph[3]}</p></div>', unsafe_allow_html=True)
    st.caption("La curva es un esquema didáctico. Las fases reales se identifican con mediciones de la pila y criterios técnicos, no solo con el día del proceso. En el interior la temperatura es mayor que en la superficie porque la pila se enfría hacia el aire y el suelo.")

    st.divider()
    st.markdown("### ¿Cuánto calor se podría recuperar?")
    st.write("Para calentar agua con una pila hace falta un intercambiador de calor. Con estos controles podés comparar el calor que aporta la pila con el que pide un invernadero. Los valores iniciales son un **ejemplo simulado** (1.000 kg, 18 días, agua de 20 °C a 40 °C).")
    k1, k2, k3 = st.columns(3, gap="large")
    with k1:
        m_pila = st.slider("Masa de la pila (kg)", 200, 3000, 1000, 100, key="rec_mass")
        q_util = st.slider("Calor útil recuperable (kJ por kg de pila y por día)", 5.0, 40.0, 17.9, 0.5, key="rec_q",
                           help="Supuesto del ejemplo: parte del calor que libera la pila y que el intercambiador logra pasar al agua.")
    with k2:
        t0 = st.slider("Temperatura inicial del agua (°C)", 5, 30, 20, key="rec_t0")
        t1 = st.slider("Temperatura final del agua (°C)", 30, 70, 40, key="rec_t1")
        dias = st.slider("Días de suministro", 1, 60, 18, key="rec_days")
    with k3:
        area = st.slider("Superficie del invernadero (m²)", 4, 100, 24, key="rec_area")
        dT = st.slider("Diferencia de temperatura interior−exterior (°C)", 2, 25, 10, key="rec_dT")
    c_agua = 4186
    delta = max(1, t1 - t0)
    litros = m_pila * q_util * 1000 / (c_agua * delta)
    kwh_dia = m_pila * q_util / 3600
    kwh_total = kwh_dia * dias
    demanda = 6.0 * (3 * area) * dT * 24 / 1000
    cobertura = 100 * kwh_dia / demanda if demanda else 0
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Agua calentada por día", f"{litros:,.0f} L".replace(",", "."))
    m2.metric("Calor aportado por día", f"{kwh_dia:.1f} kWh".replace(".", ","))
    m3.metric(f"Calor en {dias} días", f"{kwh_total:.0f} kWh")
    m4.metric("Cobertura del invernadero", f"{cobertura:.0f} %")
    fig = go.Figure(go.Bar(x=[kwh_dia, demanda], y=["Calor que aporta la pila", f"Calor que pide el invernadero ({area} m²)"], orientation="h",
                           marker=dict(color=[T["c1"], T["warn"]]), text=[f"{kwh_dia:.1f} kWh/día".replace(".", ","), f"{demanda:.0f} kWh/día"], textposition="auto",
                           hoverinfo="skip"))
    base_layout(fig, height=200, title=dict(text="Aporte frente a demanda (kWh por día)", font=dict(size=15)))
    fig.update_xaxes(gridcolor=T["border"], zeroline=False)
    plot(fig)
    m_txt = f"{m_pila:,}".replace(",", ".")
    callout(f"<b>Lectura.</b> Con estos supuestos, una pila de {m_txt} kg aporta cerca del {cobertura:.0f} % de lo que pide un invernadero de {area} m²: haría falta del orden de {max(1, round(demanda / kwh_dia))} pilas como esa. "
            "Es el tipo de razonamiento de escala que buscamos con los estudiantes.")
    st.caption("Supuestos del invernadero: cubierta de polietileno con transmitancia de 6 W/(m²·K) y superficie de envolvente igual a 3 veces la superficie del piso. Son valores de ejemplo, no mediciones.")

    st.markdown("### El cálculo que hacen los estudiantes")
    a, b = st.columns(2, gap="large")
    with a:
        masa = st.number_input("Masa de agua (kg)", min_value=1.0, max_value=10000.0, value=100.0, step=10.0, key="q_m")
        ta = st.slider("Temperatura inicial (°C)", 0, 40, 20, key="q_t0")
        tb = st.slider("Temperatura final (°C)", 20, 90, 40, key="q_t1")
        q = masa * c_agua * max(0, tb - ta)
        mm1, mm2 = st.columns(2)
        mm1.metric("Calor transferido al agua", f"{q:,.0f} J".replace(",", "."))
        mm2.metric("Equivalencia", f"{q / 3.6e6:.2f} kWh".replace(".", ","))
    with b:
        st.markdown(f'<div class="card"><div class="kicker">Modelo físico</div><h3>Q = m · c · ΔT</h3><p><b>m</b>: masa de agua (kg)<br><b>c</b>: calor específico del agua (aprox. 4186 J/kg·°C)<br><b>ΔT</b>: variación de temperatura</p><hr>'
                    f'<div class="kicker">Escenario elegido</div><div class="big-number">{max(0, tb - ta):.1f} °C</div><p>Incremento de temperatura del agua durante el cálculo.</p>'
                    '<p class="small-muted">Este cálculo no predice el calor real disponible en una pila de compost. Para eso se necesitan mediciones y un modelo de pérdidas, duración y recuperación térmica.</p></div>', unsafe_allow_html=True)
    st.markdown("### Del modelo a una pregunta de investigación")
    st.write("¿Qué mediciones harían falta para estimar el calor que una pila podría transferir? Considerá masa, variación de temperatura, duración, pérdidas térmicas y eficiencia del sistema de intercambio.")


def page_propuestas():
    heading("08 · Transposición didáctica", "Cuatro niveles, un territorio",
            "Las propuestas responden a brechas y demandas identificadas en el análisis. Son diseños a validar: todavía no se aplicaron en el aula.")
    tabs = st.tabs(["Inicial", "Primario", "Secundario", "Superior"])
    with tabs[0]:
        st.markdown("### Descubriendo la fuerza del Sol, el viento y el agua")
        cards([card_html("1", "Calor y luz del Sol", "Agua al Sol y a la sombra: anticipan y comprueban con las manos."),
               card_html("2", "Fuerza del viento", "Molinillos de papel: ¿se mueven si corremos o si sopla el viento?"),
               card_html("3", "Agua que empuja", "Mesa de agua con canaletas y ruedas de paleta."),
               card_html("4 · Optativa", "Salida al IPEA N.° 211", "¿Una pila de compost está tibia o fría? Sujeta a acuerdo institucional.")], cols=4)
        callout("<b>Evaluación:</b> registro de observaciones, portafolio de dibujos y rúbrica cualitativa.")
    with tabs[1]:
        st.markdown("### El circuito energético regional de Cruz del Eje")
        cards([card_html("1", "Paisaje energético", "Mapa y fotografías auténticas del dique y de la central."),
               card_html("2", "Maquetas y kits", "Depósito, manguera, turbina y LED; versión de bajo costo."),
               card_html("3", "Eficiencia energética", "Relevar artefactos en watts y armar una campaña familiar."),
               card_html("4 · Optativa", "Visita a Ferroviario", "Comparar la maqueta con la central real.")], cols=4)
        callout("Primer ciclo: identificar fuentes. Segundo ciclo: explicar cómo funciona una central.")
    with tabs[2]:
        st.markdown("### Un puente entre Tecnología y Física")
        cards([card_html("Fase 1 · Tecnología", "Diagrama de bloques", "De la toma de agua al transformador."),
               card_html("Fase 2 · Física", "Potencia hidráulica", "P = ρ·g·Q·H con H = 28 m y ensayo de Faraday-Lenz. Podés usar el laboratorio 3D."),
               card_html("Fase 3 · Caso IPEA", "Procesos exotérmicos", "Compost, bokashi y lombricompuesto."),
               card_html("Fase 4 · Página web", "Calor y recuperación", "Cargar temperaturas, calcular el calor y simular su recuperación.")], cols=4)
        callout("<b>Evaluación:</b> rúbrica del producto, indicadores de logro y cierre con Padlet o Mentimeter.")
    with tabs[3]:
        st.markdown("### Hidrodinámica, riesgos laborales y gestión ambiental")
        cards([card_html("A", "Modelización hidrodinámica", "Bernoulli con pérdidas y número de Reynolds en la tubería de la central. ¿El efecto Venturi optimiza la salida de la turbina?"),
               card_html("B", "Riesgos laborales", "Matriz IPERC para la central y el IPEA: riesgo eléctrico, alturas y espacios confinados, y procedimiento LOTO."),
               card_html("C", "Balance de calor", "¿Alcanza el calor del compost para calentar agua o un invernadero? Usá el simulador de compostaje.")])
        callout("<b>Producto:</b> proyecto de práctica profesionalizante, con manual de seguridad y auditoría ambiental.")
    st.divider()
    st.markdown("### Recursos digitales")
    st.markdown("- [Aviso ambiental 2026 · Parque Solar Fotovoltaico Cruz del Eje](https://cadenacentro.com/ultimas/audiencia-publica-ambiental-digital-proyecto-parque-solar-fotovoltaico-cruz-del-eje-2/)\n"
                "- [Antecedente técnico 2022 · EPEC](https://www.epec.com.ar/docs/imagenes/comunidad/blog/88/ANEXO3_PROYECTOS_PROPUESTOS_POR_EPEC_Convocatoria2022.pdf)\n"
                "- [Mapa educativo nacional · IPEA N.º 211](https://mapa.educacion.gob.ar/legajo/140256100)\n"
                "- [Central hidroeléctrica Cruz del Eje · EPEC](https://web.epec.com.ar/generacion_central_h_cruz-eje.html)\n"
                "- [Ley de Educación Ambiental Integral · Argentina.gob.ar](https://www.argentina.gob.ar/normativa/nacional/ley-27621-350594/texto)")


def page_resultados():
    heading("09 · Hallazgos", "¿Qué nos dice la investigación?", "Los resultados son exploratorios: la muestra por conveniencia no permite generalizar a todos los docentes o instituciones.")
    cards([metric_card("Contexto local en documentos", "0", "Documentos que lo mencionan de forma explícita, según el análisis."),
           metric_card("Contexto local en docentes", "5 de 6", "Docentes que lo usan o lo mencionan en sus clases."),
           metric_card("Demanda de apoyos", "5 de 6", "Docentes que piden recursos o capacitación didáctica.")])
    st.markdown("### Contraste provisorio de las hipótesis")
    st.markdown(table_html(["Hipótesis", "Estado", "Por qué"], [
        ["<b>H1</b> Profundidad", "<span class='badge'>Confirmada parcialmente</span>", "La presencia real supera a la prescripta."],
        ["<b>H2</b> Apoyos", "<span class='badge'>Parcialmente sostenida</span>", "La demanda de recursos es mayoritaria; el apoyo en manuales no."],
        ["<b>H3</b> Contexto local", "<span class='badge'>Confirmada en documentos; no en prácticas</span>", "Depende de la iniciativa docente."],
        ["<b>H4</b> Articulación", "<span class='badge'>Confirmada parcialmente</span>", "Existe donde la institución la sostiene."]], widths=[24, 30, 46]), unsafe_allow_html=True)
    st.write("")
    st.markdown("### Conclusiones")
    cards([f'<div class="card"><div class="big-number" style="font-size:1.6rem">{i}</div><p>{t}</p></div>' for i, t in enumerate([
        "La ausencia en el currículo no equivale a ausencia en el aula: lo enseñado puede exceder lo prescripto.",
        "El anclaje local depende de la iniciativa docente y de la institución, no del currículo.",
        "La articulación entre niveles existe donde hay un dispositivo que la sostiene.",
        "Hace falta un recurso con rigor físico: visitas, maquetas y herramientas digitales, no convencer de usar el contexto."], 1)], cols=4)
    st.markdown("### Limitaciones y próximos pasos")
    cards([card_html("Limitaciones", "Lo que hay que tener presente", "• Muestra por conveniencia: no permite generalizar.<br>• Prácticas declaradas, no observadas.<br>• Un solo docente de nivel superior.<br>• Entrevista de primario respondida por escrito.<br>• Documento del 6.° año técnico no disponible."),
           card_html("Próximos pasos", "Hacia adelante", "• Validar las propuestas con los docentes entrevistados.<br>• Probar la página web en una escuela.<br>• Armar las guías de actividades por nivel.<br>• Ampliar la muestra a más docentes por nivel.")], cols=2)
    st.write("")
    st.markdown(f"""<div class="hero" style="min-height:230px;text-align:center;align-items:center"><div class="eyebrow">Muchas gracias</div>
<h1 style="font-size:clamp(2rem,4vw,3.2rem)">¿Preguntas?</h1><p style="margin:0 auto">{' · '.join(TEAM)}</p>
<p style="margin:.4rem auto 0;font-size:.95rem">Profesorado Universitario de Física · UPC · Sede Cruz del Eje · 2026</p></div>""", unsafe_allow_html=True)


ROUTES = {
    "Presentación del equipo": page_portada, "Inicio": page_inicio, "La investigación": page_investigacion, "Documentos y docentes": page_documentos,
    "Mapa energético local": page_mapa, "Cruz del Eje": page_cruz, "Registro de campo": page_registro, "Laboratorio hidráulico 3D": page_laboratorio,
    "Compostaje y calor": page_compost, "Propuestas didácticas": page_propuestas, "Resultados y conclusiones": page_resultados,
}
ROUTES[page]()

# ───────────────────────── Navegación secuencial ─────────────────────────
st.divider()
idx = PAGES.index(page)
nl, nm, nr = st.columns([1, 2, 1])
with nl:
    if idx > 0:
        st.button("← Anterior", key="prev", on_click=go_to, args=(PAGES[idx - 1],), **STRETCH)
with nm:
    st.markdown(f'<div class="nav-note" style="text-align:center;padding-top:.55rem">Sección {idx:02d} de {len(PAGES) - 1:02d} · {page}</div>', unsafe_allow_html=True)
with nr:
    if idx < len(PAGES) - 1:
        st.button("Siguiente →", key="next", type="primary", on_click=go_to, args=(PAGES[idx + 1],), **STRETCH)
st.markdown("<div style='display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:var(--muted);font-size:.85rem'><span>La energía renovable como contenido escolar</span><span>Profesorado Universitario de Física · UPC · 2026</span></div>", unsafe_allow_html=True)
