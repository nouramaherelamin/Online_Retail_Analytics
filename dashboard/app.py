"""
Online Retail Analytics - Streamlit dashboard (dark theme, filters + search in the sidebar)

Requirements : streamlit>=1.40, plotly, pandas, numpy
Run          : streamlit run app.py

Project layout:
    data/raw/Online Retail.csv                (if missing, a built-in DEMO dataset is generated)
    data/processed/clean_transactions.csv     (optional)
    data/processed/customer_rfm.csv           (optional - otherwise RFM is computed from the sales data)
    assets/hero.png                           (hero banner)
    assets/icons/*.png                        (optional - falls back to built-in SVG icons)
"""
import base64
import html as _html
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from pathlib import Path

ICON = Path(__file__).parent / "assets" / "icons" / "orders.png"

st.set_page_config(
    page_title="Online Retail Analytics",
    page_icon=str(ICON),
    layout="wide"
)

# ----------------------------------------------------------------------------- paths
HERE = Path(__file__).resolve().parent
BASE = next((p for p in (HERE, HERE.parent) if (p / "data").exists()), HERE)
DATA = BASE / "data" / "processed"
RAW = BASE / "data" / "raw" / "Online Retail.csv"
ASSETS = next((p / "assets" for p in (HERE, HERE.parent) if (p / "assets").exists()), BASE / "assets")
ICONS = ASSETS / "icons"
IS_DEMO = not RAW.exists() and not (DATA / "clean_transactions.csv").exists()

# ----------------------------------------------------------------------------- palette
ORANGE = "#F97316"
INK = "#F3F4F6"
SLATE = "#9CA3AF"
CARD = "#111722"
GREEN = "#22C55E"
RED = "#EF4444"
GRID = "#1E2735"

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root{--bg:#0A0E15;--card:#111722;--line:#1F2836;--ink:#F3F4F6;--muted:#9CA3AF;--orange:#F97316;--orange2:#FB923C}
html,body,.stApp{font-family:'DM Sans',sans-serif}
[data-testid="stIconMaterial"]{font-family:'Material Symbols Rounded'!important}
.stApp{background:radial-gradient(1100px 480px at 75% -8%,rgba(249,115,22,.11),transparent 60%),var(--bg);color:var(--ink)}
header[data-testid="stHeader"]{background:transparent!important}
[data-testid="stAppDeployButton"],.stDeployButton,#MainMenu,footer{display:none!important}
:root{--gap:24px}
.block-container{max-width:none!important;margin:0;padding:2rem 2.5rem 2.5rem!important}
.block-container>div[data-testid="stVerticalBlock"]{gap:var(--gap)!important}
div[data-testid="stHorizontalBlock"]{gap:var(--gap)!important}

/* ---------- keyframes ---------- */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes drift{from{transform:scale(1.03) translateX(0)}to{transform:scale(1.1) translateX(-22px)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}
@keyframes glow{0%,100%{box-shadow:0 0 0 0 rgba(249,115,22,.0)}50%{box-shadow:0 0 18px 2px rgba(249,115,22,.35)}}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D121B 0%,#0A0E15 100%)!important;border-right:1px solid var(--line)!important}
section[data-testid="stSidebar"][aria-expanded="true"]{min-width:340px!important;max-width:340px!important;width:340px!important}
section[data-testid="stSidebar"][aria-expanded="false"]{min-width:0!important;max-width:0!important;width:0!important;margin-left:0!important;transform:none!important;border:0!important;overflow:hidden!important}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"]{height:auto;min-height:2.25rem;padding:.5rem .75rem 0}
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]{gap:.4rem}
.brand{display:flex;align-items:center;gap:12px;padding:4px 6px 20px;animation:slideIn .6s ease both}
.brand-name{font-weight:700;font-size:17px;letter-spacing:.6px;line-height:1.15;color:#fff}
.brand-name small{display:block;font-weight:500;font-size:14px;letter-spacing:1.4px;color:#D1D5DB}
section[data-testid="stSidebar"] div[data-testid="stButton"],[class*="st-key-nav_"],.st-key-btn_reset{width:100%!important}
[class*="st-key-nav_"] button,.st-key-btn_reset button{width:100%!important}
section[data-testid="stSidebar"] div[data-testid="stButton"] button{width:100%;justify-content:flex-start!important;gap:6px;background:transparent!important;border:0!important;box-shadow:none!important;color:#E5E7EB!important;border-radius:10px!important;min-height:42px;padding:0 14px!important;transition:background .2s,transform .2s,color .2s}
section[data-testid="stSidebar"] div[data-testid="stButton"] button p{color:inherit!important;font-size:15px;font-weight:500}
section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover{background:rgba(255,255,255,.07)!important;color:#fff!important;transform:translateX(4px)}
section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]{background:var(--orange)!important;color:#fff!important;transform:none}
section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] p{color:#fff!important;font-weight:700}
.side-sep{height:1px;background:rgba(255,255,255,.1);margin:16px 6px}
.side-h{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:#fff;margin:4px 4px 6px}
section[data-testid="stSidebar"] label p{color:#D1D5DB!important;font-size:13px!important;font-weight:500}
div[data-baseweb="input"],div[data-baseweb="select"]>div{background:#151C29!important;border:1px solid #263041!important;border-radius:10px!important;min-height:40px;transition:border-color .2s,box-shadow .2s}
div[data-baseweb="input"]:focus-within,div[data-baseweb="select"]>div:hover{border-color:var(--orange)!important;box-shadow:0 0 0 1px rgba(249,115,22,.4)}
.st-key-f_search input{padding-left:38px!important;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23F97316' stroke-width='2' stroke-linecap='round'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cpath d='M20 20l-3.5-3.5'/%3E%3C/svg%3E") no-repeat 12px center}
.st-key-btn_reset button{justify-content:center!important;margin-top:6px;animation:glow 3s ease-in-out infinite}
.st-key-btn_reset button:hover{transform:none!important;filter:brightness(1.1)}
.demo-note{font-size:11.5px;color:#FDBA74;background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.3);border-radius:8px;padding:6px 10px;margin:6px 2px}

/* ---------- hero ---------- */
.hero{position:relative;height:300px;margin-top:0;border-radius:16px;overflow:hidden;border:1px solid var(--line);animation:fadeIn .7s ease both}
.hero-bg{position:absolute;inset:0;background-size:cover;background-position:right center;animation:drift 22s ease-in-out infinite alternate}
.hero:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,#0A0E15 0%,rgba(10,14,21,.88) 34%,rgba(10,14,21,.2) 70%,rgba(10,14,21,0) 100%)}
.hero-content{position:absolute;left:52px;top:38px;max-width:680px;z-index:2;color:#fff;animation:fadeUp .8s .15s ease both}
.hero-title{font-family:'Playfair Display',serif;font-size:46px;line-height:1.07;font-weight:700}
.hero-title span{color:var(--orange)}
.hero-copy{font-size:15px;color:#D1D5DB;margin-top:14px;line-height:1.6;max-width:610px}

/* ---------- KPI cards ---------- */
.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--gap)}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px 22px;display:flex;flex-wrap:nowrap;align-items:center;gap:16px;min-height:116px;container-type:inline-size;animation:fadeUp .6s ease both;transition:transform .25s,border-color .25s,box-shadow .25s}
.kpi:nth-child(1){animation-delay:.05s}.kpi:nth-child(2){animation-delay:.14s}.kpi:nth-child(3){animation-delay:.23s}.kpi:nth-child(4){animation-delay:.32s}
.kpi:hover{transform:translateY(-4px);border-color:rgba(249,115,22,.55);box-shadow:0 10px 28px rgba(249,115,22,.14)}
.kpi-icon{width:58px;height:58px;flex:none;border-radius:14px;background:#2A1A10;border:1px solid #3A2414;display:flex;align-items:center;justify-content:center}
.kpi-mid{min-width:0;flex:1 1 auto}
.kpi-label{font-size:14px;color:#D1D5DB;font-weight:500}
.kpi-value{font-size:30px;font-weight:700;color:#fff;line-height:1.15;margin-top:2px}
.kpi-delta{font-size:13.5px;font-weight:700;margin-top:3px}
.kpi-spark{margin-left:auto;align-self:center;flex:0 0 auto}.kpi-spark svg{display:block}
@container (max-width:300px){.kpi-spark{display:none}}
.kpi-spark polyline{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.6s .35s ease forwards}
.kpi-spark polygon{animation:fadeIn 1.6s .6s ease both}

/* ---------- cards ---------- */
[class*="st-key-card_"]{
  background:linear-gradient(180deg,rgba(17,23,34,.98),rgba(14,20,30,.98));
  border:1px solid var(--line);
  border-radius:18px;
  padding:24px 26px;
  gap:1rem;
  animation:fadeUp .7s cubic-bezier(.2,.75,.2,1) both;
  transition:transform .28s ease,border-color .28s ease,box-shadow .28s ease;
  overflow:hidden;
}
[class*="st-key-card_"]:hover{
  transform:translateY(-3px);
  border-color:rgba(249,115,22,.48);
  box-shadow:0 14px 34px rgba(0,0,0,.28),0 0 0 1px rgba(249,115,22,.06);
}
[class*="st-key-card_"] div[data-testid="stHorizontalBlock"]{gap:18px!important}
[data-testid="stPlotlyChart"]{
  animation:fadeUp .8s .12s cubic-bezier(.2,.75,.2,1) both;
  transition:transform .25s ease;
}
[data-testid="stPlotlyChart"]:hover{transform:translateY(-2px)}
.ptitle{display:flex;align-items:center;gap:11px;font-size:17.5px;font-weight:700;color:#fff;margin-bottom:2px}
.ptitle img{width:26px;height:26px;object-fit:contain}
.section-heading{font-size:24px;font-weight:700;color:#fff;margin:2px 0 0;animation:slideIn .5s ease both}
.bar{height:6px;border-radius:6px;background:#1C2433;overflow:hidden}
.bar span{display:block;height:100%;border-radius:6px;background:linear-gradient(90deg,#EA580C,#FB923C);transform-origin:left;animation:grow 1.1s .3s cubic-bezier(.2,.8,.2,1) both}

.cty-scroll,.prod-scroll{overflow-y:auto;padding-right:6px}
.cty-scroll{max-height:300px}.prod-scroll{max-height:400px}
.cty-scroll::-webkit-scrollbar,.prod-scroll::-webkit-scrollbar{width:5px}
.cty-scroll::-webkit-scrollbar-thumb,.prod-scroll::-webkit-scrollbar-thumb{background:#2A3446;border-radius:5px}
.cty-row{display:grid;grid-template-columns:30px 1fr auto;gap:3px 10px;align-items:center;margin-bottom:11px;font-size:13.5px}
.cty-row .flag{width:28px;height:19px;border-radius:3px;object-fit:cover}
.cty-name{color:#E5E7EB;font-weight:500}.cty-val{font-weight:600;color:#fff}
.prod-row{display:grid;grid-template-columns:22px 44px 1fr auto;gap:2px 12px;align-items:center;margin-bottom:10px;transition:transform .2s}
.prod-row:hover{transform:translateX(4px)}
.prod-rank{grid-row:1/3;font-size:20px;color:#E5E7EB;text-align:center}
.prod-thumb{grid-row:1/3;width:44px;height:40px;border-radius:8px;background:#1C2433;display:flex;align-items:center;justify-content:center;font-size:21px}
.prod-name{font-size:12.5px;font-weight:600;color:#E5E7EB;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.prod-val{font-size:13px;font-weight:700;color:#fff;text-align:right}
.prod-row .bar{grid-column:3/5}
.lg-row{display:flex;align-items:center;gap:10px;font-size:13.5px;margin:0;padding:10px 0;border-bottom:1px solid var(--line);color:#E5E7EB}
.lg-row:last-child{border-bottom:0}
.lg-row .dot{width:14px;height:14px;border-radius:50%;flex:none}
.lg-row .lg-val{margin-left:auto;color:#9CA3AF}
.ins-title{display:flex;align-items:center;gap:10px;color:var(--orange);font-weight:700;font-size:21px}
.ins-text{font-size:14px;color:#D1D5DB}.ins-text b{color:#fff}

.block-container button[data-testid="stBaseButton-primary"]{background:var(--orange)!important;border:0!important;color:#fff!important;border-radius:10px!important;font-weight:700;min-height:46px;width:100%;transition:transform .2s,filter .2s}
.block-container button[data-testid="stBaseButton-primary"]:hover{transform:translateY(-2px);filter:brightness(1.1)}
.block-container button[data-testid="stBaseButton-primary"] p{color:#fff!important;font-weight:700}
.st-key-btn_viewall{display:flex;justify-content:flex-end}
.st-key-btn_viewall button{background:transparent!important;border:0!important;box-shadow:none!important;color:#E5E7EB!important;font-size:13px;padding:0!important;min-height:0!important}
.st-key-btn_viewall button:hover{color:var(--orange)!important}
/* ---------- polished spacing + motion ---------- */
div[data-testid="stHorizontalBlock"]:has([class*="st-key-card_"]){align-items:stretch!important}
div[data-testid="stColumn"]:has([class*="st-key-card_"]){display:flex;flex-direction:column}
div[data-testid="stColumn"]:has([class*="st-key-card_"])>div[data-testid="stVerticalBlock"]{flex:1}
div[data-testid="stColumn"]>div[data-testid="stVerticalBlock"]>[class*="st-key-card_"],
div[data-testid="stColumn"]>div[data-testid="stVerticalBlock"]>div:has(>[class*="st-key-card_"]){flex:1}
div:has(>[class*="st-key-card_"])>[class*="st-key-card_"]{height:100%}
.section-heading{padding:6px 2px 2px;margin:4px 0 2px;letter-spacing:-.3px}
[data-testid="stDataFrame"]{
  border:1px solid var(--line)!important;
  border-radius:14px!important;
  overflow:hidden;
  animation:fadeUp .7s ease both;
}
[data-testid="stMetric"]{
  background:rgba(255,255,255,.025);
  border:1px solid var(--line);
  border-radius:14px;
  padding:12px 14px;
  transition:transform .25s ease,border-color .25s ease;
}
[data-testid="stMetric"]:hover{transform:translateY(-2px);border-color:rgba(249,115,22,.45)}
.stButton button{transition:transform .22s ease,box-shadow .22s ease,filter .22s ease!important}
.stButton button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 20px rgba(249,115,22,.14)!important}
.st-key-btn_explore button{animation:glow 3.5s ease-in-out infinite}
.footer-wrap{
  margin-top:28px;
  padding:18px 8px 5px;
  border-top:1px solid var(--line);
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:18px;
  color:#9CA3AF;
  font-size:11.5px;
  animation:fadeIn .9s ease both;
}
.footer-brand{color:#F3F4F6;font-weight:700;letter-spacing:.5px}
.footer-links{display:flex;gap:16px;align-items:center}
.footer-links a{
  color:#CBD5E1!important;
  text-decoration:none!important;
  transition:color .2s ease,transform .2s ease;
  display:inline-block;
}
.footer-links a:hover{color:#F97316!important;transform:translateY(-1px)}
.footer-copy{text-align:right}
@media(max-width:1100px){.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.block-container{padding:1.5rem 1.25rem 2rem!important}}
@media(max-width:760px){
  .block-container{padding:1.5rem 12px 18px!important}
  div[data-testid="stHorizontalBlock"]{gap:12px!important}
  .hero-title{font-size:34px}
  .footer-wrap{flex-direction:column;align-items:flex-start}
  .footer-copy{text-align:left}
}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.kpi-spark polyline{stroke-dashoffset:0}}
""" + "".join(f".st-key-card_{i}{{animation-delay:{0.05 * i:.2f}s}}" for i in range(1, 13)) + '/* ---------- wide sidebar + full hero ---------- */\nsection[data-testid="stSidebar"] input,\nsection[data-testid="stSidebar"] [data-baseweb="select"],\nsection[data-testid="stSidebar"] [data-baseweb="select"] > div{\n  width:100%!important;\n}\nsection[data-testid="stSidebar"] .st-key-f_search input{font-size:13px!important;}\nsection[data-testid="stSidebar"] .side-h{white-space:nowrap!important;}\n.hero-content .hero-title{max-width:690px;}\ndiv[data-baseweb="popover"] li{white-space:normal!important;line-height:1.35!important;height:auto!important;min-height:36px}\nsection[data-testid="stSidebar"] [data-baseweb="select"] div{font-size:13.5px}\n' + "</style>"
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------- icons
ICON_PATHS = {
    "bar": '<rect x="4" y="11" width="4" height="9" rx="1"/><rect x="10" y="4" width="4" height="16" rx="1"/><rect x="16" y="8" width="4" height="12" rx="1"/>',
    "box": '<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17" cy="9" r="2.6"/><path d="M17 14c2.6 0 4.5 1.8 4.5 4.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a2 2 0 002 1.6h8.2a2 2 0 002-1.5L21.5 8H6"/>',
    "trophy": '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 01-10 0V4z"/><path d="M17 5h3v2a3 3 0 01-3 3M7 5H4v2a3 3 0 003 3"/>',
    "refresh": '<path d="M3 12a9 9 0 109-9 9 9 0 00-6.4 2.6L3 8"/><path d="M3 3v5h5"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.7.6 1 1.3 1 2.1h5c0-.8.3-1.5 1-2.1A6 6 0 0012 3z"/>',
    "filter": '<path d="M3 5h18l-7 8v6l-4-2v-4L3 5z"/>',
}


def svg(name, size=22, color=ORANGE, sw=1.9):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[name]}</svg>')


@st.cache_data
def _b64(path_str):
    p = Path(path_str)
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""


def asset_uri(p):
    s = _b64(str(p))
    if not s:
        return ""
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "webp": "webp"}.get(p.suffix.lower().lstrip("."), "png")
    return f"data:image/{mime};base64,{s}"


def find_asset(*names):
    for n in names:
        p = ASSETS / n
        if p.exists():
            return p
    return None


def icon_html(png, name, size=26, color=ORANGE):
    p = ICONS / png if png else None
    if p is not None and p.exists():
        return f'<img src="{asset_uri(p)}" style="width:{size}px;height:{size}px;object-fit:contain">'
    return svg(name, size, color)


def esc(x):
    return _html.escape(str(x))


def money(x):
    x = float(x)
    if abs(x) >= 1e6:
        return f"£{x / 1e6:.2f}M"
    if abs(x) >= 1e3:
        return f"£{x / 1e3:.2f}K"
    return f"£{x:,.0f}"


def compact(x):
    x = float(x)
    if abs(x) >= 1e6:
        return f"{x / 1e6:.2f}M"
    if abs(x) >= 1e3:
        return f"{x / 1e3:.2f}K"
    return f"{x:,.0f}"


# ----------------------------------------------------------------------------- data
def _clean(df):
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"]).copy()
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["StockCode"] = df["StockCode"].astype(str)
    if "CustomerID" not in df.columns:
        df["CustomerID"] = np.nan
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["Description"] = df["Description"].fillna("Unknown Product").astype(str)
    df["Country"] = df["Country"].fillna("Unknown").astype(str)
    return df


def _time_cols(df):
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["DayName"] = df["InvoiceDate"].dt.day_name()
    return df


def make_demo():
    """Synthetic dataset with the same columns as 'Online Retail.csv' (used only when no CSV exists)."""
    rng = np.random.default_rng(7)
    prods = [("WHITE HANGING HEART T-LIGHT HOLDER", 2.95), ("REGENCY CAKESTAND 3 TIER", 12.75),
             ("JUMBO BAG RED RETROSPOT", 2.08), ("PARTY BUNTING", 4.95), ("LUNCH BAG RED RETROSPOT", 1.65),
             ("ASSORTED COLOUR BIRD ORNAMENT", 1.69), ("PAPER CHAIN KIT 50'S CHRISTMAS", 2.55),
             ("SET OF 3 CAKE TINS PANTRY DESIGN", 4.95), ("HEART OF WICKER SMALL", 1.65),
             ("NATURAL SLATE HEART CHALKBOARD", 3.75), ("RABBIT NIGHT LIGHT", 2.08), ("POPCORN HOLDER", 0.85),
             ("VICTORIAN GLASS HANGING T-LIGHT", 1.25), ("WOODEN PICTURE FRAME WHITE FINISH", 2.55),
             ("SPOTTY BUNTING", 4.95), ("RED HARMONICA IN BOX", 1.25), ("JAM MAKING SET WITH JARS", 4.25),
             ("HOT WATER BOTTLE KEEP CALM", 4.95), ("CHOCOLATE HOT WATER BOTTLE", 4.65),
             ("GLASS STAR FROSTED T-LIGHT HOLDER", 3.75), ("BIRTHDAY CARD RETROSPOT", 0.42),
             ("LANTERN CANDLE HOLDER", 3.25), ("MUG KEEP CALM AND CARRY ON", 1.25), ("STORAGE BOX VINTAGE", 6.35)]
    countries = ["United Kingdom", "Netherlands", "Germany", "France", "Australia", "EIRE", "Spain",
                 "Switzerland", "Belgium", "Norway", "Japan", "USA"]
    cw = np.array([.80, .035, .03, .03, .02, .02, .01, .01, .01, .01, .005, .005])
    cw = cw / cw.sum()
    n_cust = 700
    cust_ids = 12346 + np.arange(n_cust)
    cust_country = rng.choice(countries, n_cust, p=cw)
    cust_p = rng.pareto(1.4, n_cust) + 1
    cust_p = cust_p / cust_p.sum()
    pp = rng.pareto(1.1, len(prods)) + 1
    pp = pp / pp.sum()
    n_inv = 3500
    days = rng.beta(1.7, 1.0, n_inv) * 373
    dates = pd.to_datetime("2010-12-01") + pd.to_timedelta(days * 86400 + rng.integers(8 * 3600, 19 * 3600, n_inv), unit="s")
    rows = []
    for i in range(n_inv):
        c = rng.choice(n_cust, p=cust_p)
        cancelled = rng.random() < .08
        inv = ("C" if cancelled else "") + str(536365 + i)
        for _ in range(rng.integers(1, 9)):
            k = rng.choice(len(prods), p=pp)
            q = int(rng.integers(1, 25))
            rows.append((inv, f"P{k:04d}", prods[k][0], -q if cancelled else q, dates[i], prods[k][1],
                         float(cust_ids[c]), cust_country[c]))
    return pd.DataFrame(rows, columns=["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
                                       "UnitPrice", "CustomerID", "Country"])


@st.cache_data(show_spinner="Loading raw data...")
def load_raw():
    if RAW.exists():
        return _clean(pd.read_csv(RAW, encoding="ISO-8859-1"))
    if IS_DEMO:
        return _clean(make_demo())
    return None


@st.cache_data(show_spinner="Loading sales data...")
def load_sales():
    p = DATA / "clean_transactions.csv"
    if p.exists():
        df = _clean(pd.read_csv(p))
    else:
        raw = load_raw()
        if raw is None:
            return None
        df = raw[(raw.Quantity > 0) & (raw.UnitPrice > 0)].copy()
    return _time_cols(df)


@st.cache_data
def load_cancelled():
    raw = load_raw()
    if raw is None:
        return None
    c = raw[raw.InvoiceNo.str.startswith("C")].copy()
    c["Quantity"] = c.Quantity.abs()
    c["Revenue"] = c.Revenue.abs()
    return _time_cols(c)


def compute_rfm(df):
    d = df.dropna(subset=["CustomerID"])
    if d.empty or d.CustomerID.nunique() < 5:
        return pd.DataFrame()
    snap = d.InvoiceDate.max() + pd.Timedelta(days=1)
    g = d.groupby("CustomerID").agg(Last=("InvoiceDate", "max"), Frequency=("InvoiceNo", "nunique"),
                                    Monetary=("Revenue", "sum")).reset_index()
    g["Recency"] = (snap - g.Last).dt.days
    g = g.drop(columns="Last")
    g["CustomerID"] = g.CustomerID.astype(int)

    def score(s, rev=False):
        q = pd.qcut(s.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        return 6 - q if rev else q
    g["RFM_Score"] = score(g.Recency, True) + score(g.Frequency) + score(g.Monetary)
    g["Segment"] = pd.cut(g.RFM_Score, [-np.inf, 5, 8, 11, 13, np.inf],
                          labels=["Lost", "At Risk", "Potential Loyalists", "Loyal Customers", "Champions"]).astype(str)
    return g


@st.cache_data
def load_rfm(_sales):
    p = DATA / "customer_rfm.csv"
    if not p.exists():
        return compute_rfm(_sales)
    r = pd.read_csv(p)
    if "CustomerID" not in r.columns:
        return compute_rfm(_sales)
    if "RFM_Score" not in r.columns:
        cols = [c for c in ["R_Score", "FrequencyScore", "MonetaryScore"] if c in r.columns]
        if len(cols) == 3:
            r["RFM_Score"] = r[cols].sum(axis=1)
    if "Segment" not in r.columns:
        if "RFM_Score" in r.columns:
            r["Segment"] = pd.cut(r["RFM_Score"], [-np.inf, 5, 8, 11, 13, np.inf],
                                  labels=["Lost", "At Risk", "Potential Loyalists", "Loyal Customers",
                                          "Champions"]).astype(str)
        else:
            r["Segment"] = "Unclassified"
    return r


@st.cache_data
def customer_list(_df):
    ids = pd.to_numeric(_df["CustomerID"], errors="coerce").dropna().astype(int).unique()
    return [str(i) for i in sorted(ids)]


@st.cache_data
def product_list(_df):
    return sorted(_df.Description.unique())


sales = load_sales()
if sales is None or sales.empty:
    st.error(f"No data found. Put 'Online Retail.csv' in:  {RAW}\n\nor the cleaned file in:  {DATA / 'clean_transactions.csv'}")
    st.stop()
raw_all = load_raw()
rfm = load_rfm(sales)
d_min, d_max = sales.InvoiceDate.min().date(), sales.InvoiceDate.max().date()

# ----------------------------------------------------------------------------- navigation + filters (sidebar)
PAGES = [("Overview", ":material/dashboard:"), ("Sales Analytics", ":material/bar_chart:"),
         ("Product Analysis", ":material/inventory_2:"), ("Customer Analysis", ":material/group:"),
         ("Geographic Analysis", ":material/location_on:"), ("Returns & Cancellations", ":material/refresh:")]
EXTRA = []
ALL_C, ALL_CU, ALL_P, ALL_S = "All Countries", "All Customers", "All Products", "All Orders"

if "page" not in st.session_state:
    st.session_state.page = "Overview"


def goto(p):
    st.session_state.page = p


def reset_filters():
    st.session_state.f_search = ""
    st.session_state.f_date = (d_min, d_max)
    st.session_state.f_country = ALL_C
    st.session_state.f_status = ALL_S
    st.session_state.f_product = ALL_P
    st.session_state.f_customer = ALL_CU


bag = ('<svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M5 8h14l-1 12H6L5 8z" fill="#F97316"/>'
       '<path d="M9 8V6.5a3 3 0 016 0V8" stroke="#F97316" stroke-width="1.8" stroke-linecap="round"/></svg>')
with st.sidebar:
    st.markdown(f'<div class="brand">{bag}<div class="brand-name">ONLINE RETAIL<small>ANALYTICS</small></div></div>',
                unsafe_allow_html=True)
    for label, ic in PAGES:
        st.button(label, key="nav_" + label, icon=ic, on_click=goto, args=(label,),
                  type="primary" if st.session_state.page == label else "secondary")
    st.markdown('<div class="side-sep"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="side-h">{svg("filter", 18)}<span>Search &amp; Filters</span></div>', unsafe_allow_html=True)
    search = st.text_input("Search", placeholder="Search products, customers, countries...",
                           label_visibility="collapsed", key="f_search")
    date_range = st.date_input("Date range", value=(d_min, d_max), min_value=d_min, max_value=d_max, key="f_date")
    country = st.selectbox("Country", [ALL_C] + sorted(sales.Country.unique()), key="f_country")
    status = st.selectbox("Order status", [ALL_S, "Completed", "Cancelled"], key="f_status")
    product = st.selectbox("Product", [ALL_P] + product_list(sales), key="f_product")
    customer = st.selectbox("Customer", [ALL_CU] + customer_list(sales), key="f_customer")
    st.button("Reset filters", key="btn_reset", icon=":material/restart_alt:", type="primary", on_click=reset_filters)
    if IS_DEMO:
        st.markdown('<div class="demo-note">Demo data in use. Put <b>Online Retail.csv</b> in <b>data/raw/</b> '
                    'to see the real numbers.</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="margin-top:14px;padding-top:12px;border-top:1px solid rgba(255,255,255,.08);'
        'font-size:10.5px;color:#6B7280;line-height:1.6">'
        '<b style="color:#D1D5DB">NOURA MAHER</b><br>'
        '© 2026 • All Rights Reserved<br>'
        '<a href="https://www.linkedin.com/in/nouramaherelamin/" target="_blank" '
        'style="color:#9CA3AF;text-decoration:none">LinkedIn</a> · '
        '<a href="https://github.com/nouramaherelamin" target="_blank" '
        'style="color:#9CA3AF;text-decoration:none">GitHub</a>'
        '</div>',
        unsafe_allow_html=True
    )

page = st.session_state.page


def apply_filters(df, use_status=True):
    out = df
    if search:
        q = search.strip().lower()
        cid = pd.to_numeric(out.CustomerID, errors="coerce").fillna(0).astype("int64").astype(str)
        mask = (out.Description.str.lower().str.contains(q, na=False, regex=False)
                | out.Country.str.lower().str.contains(q, na=False, regex=False)
                | out.StockCode.str.lower().str.contains(q, na=False, regex=False)
                | out.InvoiceNo.str.lower().str.contains(q, na=False, regex=False)
                | cid.str.contains(q, na=False, regex=False))
        out = out[mask]
    if country != ALL_C:
        out = out[out.Country == country]
    if product != ALL_P:
        out = out[out.Description == product]
    if customer != ALL_CU:
        out = out[pd.to_numeric(out.CustomerID, errors="coerce") == float(customer)]
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        d1 = pd.Timestamp(date_range[0])
        d2 = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
        out = out[(out.InvoiceDate >= d1) & (out.InvoiceDate < d2)]
    return out


base = sales
if status == "Cancelled":
    canc = load_cancelled()
    base = canc if canc is not None else sales
filtered = apply_filters(base)
if filtered.empty:
    st.warning("No data matches the current filters. Clear the search box, widen the date range, or press Reset filters.")
    st.stop()

# ----------------------------------------------------------------------------- shared helpers
_card_n = [0]


def card():
    _card_n[0] += 1
    return st.container(key=f"card_{_card_n[0]}")


def ptitle(title, icon_name, png=None):
    return f'<div class="ptitle">{icon_html(png, icon_name, 26)}<span>{esc(title)}</span></div>'


def show(fig):
    cfg = {"displaylogo": False, "displayModeBar": False}
    try:
        st.plotly_chart(fig, width="stretch", config=cfg)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True, config=cfg)


def table(df):
    try:
        st.dataframe(df, width="stretch", hide_index=True)
    except TypeError:
        st.dataframe(df, use_container_width=True, hide_index=True)


def polish(fig, h=320):
    fig.update_layout(height=h, margin=dict(l=8, r=8, t=24, b=20), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color=INK, size=12),
                      legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11, color=INK)),
                      hoverlabel=dict(bgcolor="#1F2937", font=dict(color="#fff")))
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color=SLATE, size=11))
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SLATE, size=11))
    return fig


def chart_card(title, icon_name, fig, png=None):
    with card():
        st.markdown(ptitle(title, icon_name, png), unsafe_allow_html=True)
        show(fig)


def sparkline(vals, color, uid, w=112, h=48):
    v = [float(x) for x in vals]
    if len(v) < 2:
        return ""
    lo, hi = min(v), max(v)
    rng = (hi - lo) or 1.0
    pts = [(i * (w - 4) / (len(v) - 1) + 2, h - 5 - (x - lo) / rng * (h - 14)) for i, x in enumerate(v)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"2,{h} {line} {w - 2},{h}"
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>'
            f'<linearGradient id="sp{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{color}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>'
            f'<polygon points="{area}" fill="url(#sp{uid})"/>'
            f'<polyline pathLength="1" points="{line}" fill="none" stroke="{color}" stroke-width="2.2" '
            f'stroke-linejoin="round" stroke-linecap="round"/></svg>')


def growth(series):
    """Mean of the 2nd half of the period vs. the 1st half, in %."""
    v = series.to_numpy(dtype=float)
    if len(v) < 2:
        return None
    h = len(v) // 2
    a, b = v[:h].mean(), v[h:].mean()
    return (b / a - 1) * 100 if a else None


def kpi_card(label, value, icon, delta=None, spark=""):
    dh = ""
    if delta is not None:
        up = delta >= 0
        dh = (f'<div class="kpi-delta" style="color:{GREEN if up else RED}" '
              f'title="2nd half of the selected period vs. the 1st half">'
              f'{"↑" if up else "↓"} {delta:+.1f}%</div>')
    return (f'<div class="kpi"><div class="kpi-icon">{icon}</div><div class="kpi-mid">'
            f'<div class="kpi-label">{esc(label)}</div><div class="kpi-value">{value}</div>{dh}</div>'
            f'<div class="kpi-spark">{spark}</div></div>')


def section(title):
    st.markdown(f'<div class="section-heading">{esc(title)}</div>', unsafe_allow_html=True)


FLAGS = {"United Kingdom": "gb", "France": "fr", "Australia": "au", "Netherlands": "nl", "Germany": "de",
         "Norway": "no", "EIRE": "ie", "Switzerland": "ch", "Spain": "es", "Poland": "pl", "Portugal": "pt",
         "Italy": "it", "Belgium": "be", "Lithuania": "lt", "Japan": "jp", "Iceland": "is",
         "Channel Islands": "gg", "Denmark": "dk", "Cyprus": "cy", "Sweden": "se", "Finland": "fi",
         "Austria": "at", "Greece": "gr", "Singapore": "sg", "Lebanon": "lb", "United Arab Emirates": "ae",
         "Israel": "il", "Saudi Arabia": "sa", "Czech Republic": "cz", "Canada": "ca", "Brazil": "br",
         "USA": "us", "European Community": "eu", "Bahrain": "bh", "Malta": "mt", "RSA": "za"}
MAP_NAMES = {"EIRE": "Ireland", "RSA": "South Africa", "USA": "United States"}

SEG_LABEL = {"Champions": "Champions", "Loyal Customers": "Loyal Customers", "Loyal": "Loyal Customers",
             "Potential Loyalists": "Potential Loyal", "Potential Loyalist": "Potential Loyal",
             "Potential Loyal": "Potential Loyal", "At Risk": "At Risk", "Lost": "Lost Customers",
             "Lost Customers": "Lost Customers"}
SEG_ORDER = ["Champions", "Loyal Customers", "Potential Loyal", "At Risk", "Lost Customers"]
SEG_COLOR = {"Champions": "#F97316", "Loyal Customers": "#FB9F3C", "Potential Loyal": "#FFC88A",
             "At Risk": "#D9822B", "Lost Customers": "#7C4A2D"}


def donut(labels, values, colors, center_top, center_bottom, h=215):
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=.68, sort=False, textinfo="none",
                           marker=dict(colors=colors, line=dict(color=CARD, width=3)),
                           hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>"))
    fig.update_layout(height=h, margin=dict(l=0, r=0, t=0, b=0), showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      annotations=[dict(text=f"<b>{center_top}</b><br><span style='font-size:13px;color:#9CA3AF'>"
                                             f"{center_bottom}</span>", x=.5, y=.5, showarrow=False,
                                        font=dict(size=24, color="#FFFFFF", family="DM Sans"))])
    return fig


def legend_html(items):
    rows = "".join(f'<div class="lg-row"><span class="dot" style="background:{c}"></span><span>{esc(n)}</span>'
                   f'<span class="lg-val">{v}</span></div>' for n, c, v in items)
    return f'<div>{rows}</div>'


# ----------------------------------------------------------------------------- overview widgets
def revenue_fig(df, freq):
    rule = {"Monthly": "MS", "Weekly": "W-MON", "Daily": "D"}[freq]
    s = df.set_index("InvoiceDate").Revenue.resample(rule).sum().reset_index()
    monthly = freq == "Monthly"
    fig = go.Figure(go.Scatter(
        x=s.InvoiceDate, y=s.Revenue, mode="lines+markers" if monthly else "lines",
        line=dict(color=ORANGE, width=2.8, shape="spline" if monthly else "linear"),
        marker=dict(size=8, color=ORANGE, line=dict(color="#0A0E15", width=1.5)),
        fill="tozeroy", fillcolor="rgba(249,115,22,.18)",
        hovertemplate=("%{x|%b %Y}" if monthly else "%{x|%d %b %Y}") + "<br>£%{y:,.0f}<extra></extra>"))
    fig.update_layout(height=300, margin=dict(l=4, r=10, t=6, b=4), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color=SLATE, size=11),
                      hoverlabel=dict(bgcolor="#1F2937", font=dict(color="#fff")))
    fig.update_xaxes(showgrid=False, zeroline=False, tickformat="%b<br>%Y" if monthly else "%d %b",
                     dtick="M1" if monthly else None)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, tickprefix="£", tickformat="~s", rangemode="tozero")
    return fig


def map_fig(cc, h=300):
    d = cc.copy()
    d["Name"] = d.Country.replace(MAP_NAMES)
    d["Log"] = np.log10(d.Revenue.clip(lower=1))
    fig = go.Figure(go.Choropleth(
        locations=d.Name, locationmode="country names", z=d.Log, customdata=d.Revenue, text=d.Country,
        colorscale=[[0, "#7A4A22"], [.5, "#EA7A1A"], [1, "#FF9A3D"]], showscale=False,
        marker=dict(line=dict(color="#0A0E15", width=.4)),
        hovertemplate="%{text}<br>£%{customdata:,.0f}<extra></extra>"))
    fig.update_geos(showframe=False, showcoastlines=False, showland=True, landcolor="#3A332D",
                    showcountries=True, countrycolor="#0A0E15", bgcolor="rgba(0,0,0,0)",
                    projection_type="natural earth", lataxis_range=[-58, 84])
    fig.update_layout(height=h, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)",
                      geo=dict(bgcolor="rgba(0,0,0,0)"))
    return fig


def country_rows(cc, n=None):
    top = cc.head(n) if n else cc
    mx = float(cc.Revenue.max()) or 1.0
    rows = []
    for r in top.itertuples():
        iso = FLAGS.get(r.Country)
        flag = (f'<img class="flag" src="https://flagcdn.com/w40/{iso}.png" alt="">' if iso
                else '<span class="flag"></span>')
        pct = max(float(r.Revenue) / mx * 100, 2)
        rows.append(f'<div class="cty-row">{flag}<span class="cty-name">{esc(r.Country)}</span>'
                    f'<span class="cty-val">{money(r.Revenue)}</span>'
                    f'<div class="bar" style="grid-column:2/4"><span style="width:{pct:.0f}%"></span></div></div>')
    return f'<div class="cty-scroll">{"".join(rows)}</div>'


def product_emoji(name):
    n = name.upper()
    for key, e in (("HEART", "🤍"), ("CAKE", "🎂"), ("BAG", "🛍️"), ("BUNTING", "🎉"), ("CANDLE", "🕯️"),
                   ("LIGHT", "💡"), ("MUG", "☕"), ("CARD", "💌"), ("BOTTLE", "🍶"), ("BOX", "📦"),
                   ("CLOCK", "⏰"), ("LANTERN", "🏮")):
        if key in n:
            return e
    return "🎁"


def product_rows(prod):
    mx = float(prod.Revenue.max()) or 1.0
    rows = []
    for i, r in enumerate(prod.itertuples(), 1):
        pct = max(float(r.Revenue) / mx * 100, 2)
        rows.append(f'<div class="prod-row"><div class="prod-rank">{i}</div>'
                    f'<div class="prod-thumb">{product_emoji(r.Description)}</div>'
                    f'<div class="prod-name">{esc(r.Description.upper())}</div>'
                    f'<div class="prod-val">{money(r.Revenue)}</div>'
                    f'<div class="bar"><span style="width:{pct:.0f}%"></span></div></div>')
    return f'<div class="prod-scroll">{"".join(rows)}</div>'


def segment_data(df):
    if rfm.empty:
        return None
    ids = pd.to_numeric(df.CustomerID, errors="coerce").dropna().unique()
    r = rfm[pd.to_numeric(rfm.CustomerID, errors="coerce").isin(ids)]
    if r.empty:
        return None
    lab = r.Segment.astype(str).map(lambda s: SEG_LABEL.get(s, s)).value_counts()
    order = [s for s in SEG_ORDER if s in lab.index] + [s for s in lab.index if s not in SEG_ORDER]
    lab = lab.reindex(order)
    extra = ["#9CA3AF", "#6B7280", "#D1D5DB"]
    colors = [SEG_COLOR.get(s, extra[i % 3]) for i, s in enumerate(lab.index)]
    return lab, colors


def insight_text(df):
    by_c = df.groupby("Country").Revenue.sum().sort_values(ascending=False)
    total = float(df.Revenue.sum()) or 1.0
    name = by_c.index[0]
    shown = "The " + name if name.startswith("United") else name
    parts = [f"{esc(shown)} accounts for <b>{by_c.iloc[0] / total * 100:.0f}%</b> of total revenue"]
    q = df.groupby(df.InvoiceDate.dt.quarter).Revenue.sum()
    if len(q) > 1:
        parts[0] += f", with seasonal peaks in Q{int(q.idxmax())}"
    parts[0] += "."
    idf = df[df.CustomerID.notna()]
    if not idf.empty:
        inv = idf.groupby("CustomerID").InvoiceNo.nunique()
        rep = idf[idf.CustomerID.isin(inv[inv > 1].index)].Revenue.sum()
        parts.append(f"Repeat customers contribute <b>{rep / total * 100:.0f}%</b> of revenue.")
    return " ".join(parts)


# ============================================================================= PAGES
if page == "Overview":
    hero = find_asset("hero.png", "hero.jpg", "hero.jpeg", "hero.webp")
    hbg = (f"background-image:url({asset_uri(hero)})" if hero
           else "background-image:linear-gradient(100deg,#2B1D12 0%,#6B4423 55%,#C98B4A 100%)")
    st.markdown(
        f'<div class="hero"><div class="hero-bg" style="{hbg}"></div><div class="hero-content">'
        f'<div class="hero-title">Analyze Sales.<br>Understand Customers.<br>Drive <span>Growth.</span></div>'
        f'<div class="hero-copy">Explore real online retail data through interactive insights.<br>'
        f'Track performance, discover trends and make data-driven decisions.</div></div></div>',
        unsafe_allow_html=True)

    g = filtered.groupby(filtered.InvoiceDate.dt.to_period("M"))
    m_rev, m_ord = g.Revenue.sum(), g.InvoiceNo.nunique()
    m_cus, m_prd = g.CustomerID.nunique(), g.StockCode.nunique()
    kpis = [("Total Revenue", money(filtered.Revenue.sum()), icon_html("revenue_sales.png", "bar", 30), m_rev, "#F97316"),
            ("Total Orders", compact(filtered.InvoiceNo.nunique()), icon_html("orders.png", "cart", 30), m_ord, "#F97316"),
            ("Total Customers", compact(filtered.CustomerID.nunique()), icon_html("customer.png", "users", 30), m_cus, "#F97316"),
            ("Total Products", compact(filtered.StockCode.nunique()), icon_html("product_stock.png", "box", 30), m_prd, "#F97316")]
    cards = "".join(kpi_card(l, v, ic, growth(s), sparkline(s.to_numpy(), c, i)) for i, (l, v, ic, s, c) in enumerate(kpis))
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1, card():
        h, ctl = st.columns([3, 1.3], vertical_alignment="center")
        h.markdown(ptitle("Revenue Over Time", "bar", "analytics_dashboard.png"), unsafe_allow_html=True)
        freq = ctl.selectbox("Frequency", ["Monthly", "Weekly", "Daily"], label_visibility="collapsed", key="freq")
        show(revenue_fig(filtered, freq))
    with c2, card():
        cc = (filtered.groupby("Country", as_index=False).Revenue.sum().sort_values("Revenue", ascending=False))
        h, ctl = st.columns([1.5, 1.5], vertical_alignment="center")
        h.markdown(ptitle("Sales by Country", "globe", "country.png"), unsafe_allow_html=True)
        with ctl:
            if hasattr(st, "segmented_control"):
                tab = st.segmented_control("Countries", ["Top Countries", "All Countries"], default="Top Countries",
                                           label_visibility="collapsed", key="cty_tab") or "Top Countries"
            else:
                tab = st.radio("Countries", ["Top Countries", "All Countries"], horizontal=True,
                               label_visibility="collapsed", key="cty_tab")
        mcol, lcol = st.columns([1.3, 1])
        with mcol:
            show(map_fig(cc))
        lcol.markdown(country_rows(cc, 5 if tab == "Top Countries" else None), unsafe_allow_html=True)

    p1, p2, p3 = st.columns([1.2, 1, 1])
    with p1, card():
        h, b = st.columns([3, 1.2], vertical_alignment="center")
        h.markdown(ptitle("Top 10 Products by Revenue", "trophy", "top_products.png"), unsafe_allow_html=True)
        b.button("View All  →", key="btn_viewall", on_click=goto, args=("Product Analysis",))
        prod = (filtered.groupby("Description", as_index=False).Revenue.sum()
                .sort_values("Revenue", ascending=False).head(10))
        st.markdown(f'<div style="margin-top:6px">{product_rows(prod)}</div>', unsafe_allow_html=True)
    with p2, card():
        st.markdown(ptitle("Customer Segments (RFM)", "users", "customer.png"), unsafe_allow_html=True)
        seg = segment_data(filtered)
        if seg is None:
            st.info("RFM data is not available for the current selection.")
        else:
            lab, colors = seg
            show(donut(list(lab.index), lab.to_numpy(), colors, compact(lab.sum()), "Customers"))
            st.markdown(legend_html([(n, c, f"{v / lab.sum() * 100:.0f}%")
                                    for (n, v), c in zip(lab.items(), colors)]), unsafe_allow_html=True)
    with p3, card():
        st.markdown(ptitle("Order Status", "refresh", "returns_cancellations.png"), unsafe_allow_html=True)
        if raw_all is None:
            st.info("Raw data file not found - order status needs 'Online Retail.csv'.")
        else:
            rf = apply_filters(raw_all, use_status=False)
            canc_n = int(rf.InvoiceNo.str.startswith("C").sum())
            done = int(len(rf) - canc_n)
            tot = max(done + canc_n, 1)
            show(donut(["Completed", "Cancelled"], [done, canc_n], ["#C2410C", "#EF4444"],
                       compact(tot), "Transactions"))
            st.markdown(legend_html([("Completed", "#C2410C", f"{done / tot * 100:.1f}%"),
                                    ("Cancelled", "#EF4444", f"{canc_n / tot * 100:.1f}%")]), unsafe_allow_html=True)

    with card():
        a, b, c = st.columns([1.5, 6.4, 1.9], vertical_alignment="center")
        a.markdown(f'<div class="ins-title">{svg("bulb", 30, ORANGE)}<span>Key Insight</span></div>',
                   unsafe_allow_html=True)
        b.markdown(f'<div class="ins-text">{insight_text(filtered)}</div>', unsafe_allow_html=True)
        c.button("Explore Full Analysis  →", key="btn_explore", type="primary", on_click=goto,
                 args=("Sales Analytics",))

elif page == "Sales Analytics":
    section("Sales Analytics")
    m = filtered.groupby("YearMonth", as_index=False).agg(Revenue=("Revenue", "sum"), Orders=("InvoiceNo", "nunique"))
    m["MoM Growth %"] = m.Revenue.pct_change() * 100
    a, b = st.columns(2)
    with a:
        f = px.line(m, x="YearMonth", y="Revenue", markers=True)
        f.update_traces(line_color=ORANGE, marker_color=ORANGE)
        chart_card("Monthly Revenue", "bar", polish(f, 360), "analytics_dashboard.png")
    with b:
        f = px.bar(m, x="YearMonth", y="MoM Growth %")
        f.update_traces(marker_color=ORANGE)
        chart_card("Month-over-Month Growth", "bar", polish(f, 360), "revenue_sales.png")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat = filtered.pivot_table(index="DayName", columns="Hour", values="Revenue", aggfunc="sum",
                                fill_value=0).reindex(days)
    f = px.imshow(heat, aspect="auto", color_continuous_scale=["#1B2330", ORANGE])
    chart_card("Revenue Heatmap - Day x Hour", "bar", polish(f, 380), "invoice_date.png")

elif page == "Product Analysis":
    section("Product Analysis")
    p = (filtered.groupby(["StockCode", "Description"], as_index=False)
         .agg(Revenue=("Revenue", "sum"), Quantity=("Quantity", "sum"), Orders=("InvoiceNo", "nunique"))
         .sort_values("Revenue", ascending=False))
    a, b = st.columns(2)
    with a:
        f = px.bar(p.head(15).sort_values("Revenue"), x="Revenue", y="Description", orientation="h")
        f.update_traces(marker_color=ORANGE)
        chart_card("Top Products by Revenue", "trophy", polish(f, 480), "top_products.png")
    with b:
        f = px.scatter(p.head(100), x="Quantity", y="Revenue", size="Orders", hover_name="Description")
        f.update_traces(marker_color=ORANGE)
        chart_card("Quantity vs Revenue", "box", polish(f, 480), "quantity.png")
    with card():
        st.markdown(ptitle("Product Table (top 100)", "box", "product_stock.png"), unsafe_allow_html=True)
        table(p.head(100))

elif page == "Customer Analysis":
    section("Customer Analysis")
    if rfm.empty or not {"Frequency", "Monetary", "Recency"}.issubset(rfm.columns):
        st.warning("Not enough customer data to build RFM segments.")
    else:
        ids = pd.to_numeric(filtered.CustomerID, errors="coerce").dropna().unique()
        r = rfm[pd.to_numeric(rfm.CustomerID, errors="coerce").isin(ids)].copy()
        r["Segment"] = r.Segment.astype(str).map(lambda s: SEG_LABEL.get(s, s))
        a, b = st.columns(2)
        with a:
            f = px.scatter(r, x="Frequency", y="Monetary", size="Recency", color="Segment",
                           hover_data=["CustomerID"], log_x=True, log_y=True, color_discrete_map=SEG_COLOR)
            f.update_traces(marker=dict(opacity=.8))
            chart_card("RFM Customer Value Map", "users", polish(f, 420), "customer.png")
        with b:
            seg = r.groupby("Segment", as_index=False).agg(Customers=("CustomerID", "nunique"))
            f = px.bar(seg, x="Segment", y="Customers", color="Segment", color_discrete_map=SEG_COLOR)
            f.update_layout(showlegend=False)
            chart_card("Customer Segments", "users", polish(f, 420), "customer.png")
        with card():
            st.markdown(ptitle("Top Customers by Monetary Value", "users", "customer.png"), unsafe_allow_html=True)
            table(r.sort_values("Monetary", ascending=False).head(100))

elif page == "Geographic Analysis":
    section("Geographic Analysis")
    c = (filtered.groupby("Country", as_index=False)
         .agg(Revenue=("Revenue", "sum"), Orders=("InvoiceNo", "nunique"), Customers=("CustomerID", "nunique"))
         .sort_values("Revenue", ascending=False))
    chart_card("Revenue Map", "globe", map_fig(c[["Country", "Revenue"]], 460), "country.png")
    f = px.bar(c.head(20).sort_values("Revenue"), x="Revenue", y="Country", orientation="h")
    f.update_traces(marker_color=ORANGE)
    chart_card("Top Countries by Revenue", "globe", polish(f, 520), "country.png")
    with card():
        st.markdown(ptitle("Country Table", "globe", "country.png"), unsafe_allow_html=True)
        table(c)

elif page == "Returns & Cancellations":
    section("Returns & Cancellations")
    if raw_all is None:
        st.warning("This page needs 'Online Retail.csv' in data/raw/.")
    else:
        rf = apply_filters(raw_all, use_status=False)
        returns = rf[rf.Quantity < 0]
        cancels = rf[rf.InvoiceNo.str.startswith("C")]
        tiles = [("Return Lines", f"{len(returns):,}", icon_html("returns_cancellations.png", "refresh", 30)),
                 ("Cancelled Invoices", f"{cancels.InvoiceNo.nunique():,}", icon_html("invoice.png", "cart", 30)),
                 ("Return Value", money(abs(returns.Revenue.sum())), icon_html("revenue_sales.png", "bar", 30))]
        st.markdown('<div class="kpi-grid" style="grid-template-columns:repeat(3,minmax(0,1fr))">'
                    + "".join(kpi_card(l, v, i) for l, v, i in tiles) + '</div>', unsafe_allow_html=True)
        if returns.empty:
            st.info("No returns match the current filters.")
        else:
            a, b = st.columns(2)
            with a:
                x = returns.groupby("Description", as_index=False).Quantity.sum()
                x["ReturnQty"] = x.Quantity.abs()
                x = x.sort_values("ReturnQty", ascending=False).head(15)
                f = px.bar(x.sort_values("ReturnQty"), x="ReturnQty", y="Description", orientation="h")
                f.update_traces(marker_color=ORANGE)
                chart_card("Most Returned Products", "box", polish(f, 500), "product_stock.png")
            with b:
                x = returns.groupby("Country", as_index=False).Quantity.sum()
                x["ReturnQty"] = x.Quantity.abs()
                x = x.sort_values("ReturnQty", ascending=False).head(15)
                f = px.bar(x.sort_values("ReturnQty"), x="ReturnQty", y="Country", orientation="h")
                f.update_traces(marker_color=ORANGE)
                chart_card("Returns by Country", "globe", polish(f, 500), "country.png")

elif page == "Data Information":
    section("Data Information")
    tiles = [("Valid Sales Rows", f"{len(sales):,}", icon_html("database.png", "cart", 30)),
             ("Countries", f"{sales.Country.nunique():,}", icon_html("country.png", "globe", 30)),
             ("Products", f"{sales.StockCode.nunique():,}", icon_html("product_stock.png", "box", 30)),
             ("Customers", f"{sales.CustomerID.nunique():,}", icon_html("customer.png", "users", 30))]
    st.markdown('<div class="kpi-grid">' + "".join(kpi_card(l, v, i) for l, v, i in tiles) + '</div>',
                unsafe_allow_html=True)
    with card():
        st.markdown(ptitle(f"Dataset: {d_min:%d %b %Y} - {d_max:%d %b %Y}", "bar", "invoice_date.png"),
                    unsafe_allow_html=True)
        info = pd.DataFrame({"Column": sales.columns, "Type": [str(t) for t in sales.dtypes],
                             "Missing": sales.isna().sum().to_numpy()})
        table(info)
    with card():
        st.markdown(ptitle("Sample rows", "box", "database.png"), unsafe_allow_html=True)
        table(sales.head(50))

elif page == "Settings":
    section("Settings")
    with card():
        st.markdown(ptitle("Data cache", "refresh", "returns_cancellations.png"), unsafe_allow_html=True)
        st.caption("Data is cached for speed. Clear the cache after replacing the CSV files.")
        if st.button("Clear cache and reload", key="btn_clear"):
            st.cache_data.clear()
            st.rerun()



# ----------------------------------------------------------------------------- ownership footer
st.markdown(
    '''
    <div class="footer-wrap">
      <div>
        <div class="footer-brand">ONLINE RETAIL ANALYTICS</div>
        <div style="margin-top:4px">Designed &amp; developed by Noura Maher</div>
      </div>
      <div class="footer-links">
        <a href="https://www.linkedin.com/in/nouramaherelamin/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
        <a href="https://github.com/nouramaherelamin" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
      </div>
      <div class="footer-copy">© 2026 Noura Maher. All Rights Reserved.</div>
    </div>
    ''',
    unsafe_allow_html=True
)