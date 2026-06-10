import streamlit as st
import math
import time

# --- MATHEMATICAL FUNCTIONS ---
def es_primo(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def mcd(a, b):
    while b: a, b = b, a % b
    return a

def inverso_modular(e, phi):
    d_old, d_new = 0, 1
    r_old, r_new = phi, e
    while r_new != 0:
        cociente = r_old // r_new
        r_old, r_new = r_new, r_old - cociente * r_new
        d_old, d_new = d_new, d_old - cociente * d_new
    return d_old % phi

# --- CONFIGURATION ---
st.set_page_config(page_title="RSA Academic Simulator", layout="centered")

# Initialize session state
if 'paso' not in st.session_state:
    st.session_state.paso = 0
if 'mis_llaves' not in st.session_state:
    st.session_state.mis_llaves = {}
if 'd_busqueda_completa' not in st.session_state:
    st.session_state.d_busqueda_completa = False
if 'mostrar_llave_privada_paso1' not in st.session_state:
    st.session_state.mostrar_llave_privada_paso1 = False
if 'mostrar_llave_privada_paso3' not in st.session_state:
    st.session_state.mostrar_llave_privada_paso3 = False
if 'mostrar_formula_sustituida_paso3' not in st.session_state:
    st.session_state.mostrar_formula_sustituida_paso3 = False
if 'resultado_descifrado' not in st.session_state:
    st.session_state.resultado_descifrado = None

# --- GLOBAL CSS STYLES ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Sora:wght@400;600;700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, .stText, p, span, li, h1, h2, h3, h4 {
    font-family: 'Sora', sans-serif !important;
}

/* === FORMULA BLOCKS — YELLOW pastel (My Laptop) === */
.formula-block {
    background: linear-gradient(135deg, #fffde7 0%, #fff9c4 100%);
    border-radius: 12px;
    padding: 18px 24px;
    margin: 10px 0 18px 0;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px;
    color: #5a4200;
    border-left: 4px solid #f9a825;
    box-shadow: 0 2px 10px rgba(249,168,37,0.15);
}
.formula-block .formula-label {
    font-family: 'Sora', sans-serif !important;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #e65100;
    margin-bottom: 8px;
    font-weight: 700;
}
.formula-block .formula-general {
    font-size: 18px;
    font-weight: 700;
    color: #bf360c;
    margin-bottom: 6px;
}
.formula-block .formula-substituted {
    font-size: 15px;
    color: #2e7d32;
}
.formula-block .formula-note {
    font-family: 'Sora', sans-serif !important;
    font-size: 12px;
    color: #795548;
    margin-top: 8px;
    font-style: italic;
}

/* === FORMULA BLOCKS — BLUE pastel (Friend's Laptop) === */
.formula-block-blue {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    border-radius: 12px;
    padding: 18px 24px;
    margin: 10px 0 18px 0;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px;
    color: #0d2d4e;
    border-left: 4px solid #1976D2;
    box-shadow: 0 2px 10px rgba(25,118,210,0.15);
}
.formula-block-blue .formula-label {
    font-family: 'Sora', sans-serif !important;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #1565C0;
    margin-bottom: 8px;
    font-weight: 700;
}
.formula-block-blue .formula-general {
    font-size: 18px;
    font-weight: 700;
    color: #0d47a1;
    margin-bottom: 6px;
}
.formula-block-blue .formula-substituted {
    font-size: 15px;
    color: #1b5e20;
}
.formula-block-blue .formula-note {
    font-family: 'Sora', sans-serif !important;
    font-size: 12px;
    color: #37474f;
    margin-top: 8px;
    font-style: italic;
}

/* === HOVER REVEAL — wrapper genérico === */
.hover-reveal-wrapper {
    position: relative;
    cursor: pointer;
    margin: 6px 0 14px 0;
}
/* Estado bloqueado */
.hover-reveal-locked {
    background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%);
    border: 2px dashed #bdbdbd;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    color: #757575;
    font-family: 'Sora', sans-serif !important;
    transition: border-color 0.2s;
}
.hover-reveal-locked:hover { border-color: #9e9e9e; }
/* Estado revelado — variante amarilla (My Laptop) */
.hover-reveal-content-yellow {
    display: none;
    background: linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%);
    border: 2px solid #f9a825;
    border-radius: 12px;
    padding: 16px 22px;
    box-shadow: 0 4px 16px rgba(249,168,37,0.2);
    animation: fadeReveal 0.35s ease;
    color: #4a3000;
    font-family: 'JetBrains Mono', monospace;
}
/* Estado revelado — variante azul (Friend's Laptop) */
.hover-reveal-content-blue {
    display: none;
    background: linear-gradient(135deg, #e8f4fd 0%, #d6eaf8 100%);
    border: 2px solid #1976D2;
    border-radius: 12px;
    padding: 16px 22px;
    box-shadow: 0 4px 16px rgba(25,118,210,0.18);
    animation: fadeReveal 0.35s ease;
    color: #0d2d4e;
    font-family: 'JetBrains Mono', monospace;
}
/* Estado revelado — variante roja (Private key Step 3) */
.hover-reveal-content-red {
    display: none;
    background: linear-gradient(135deg, #fce4ec 0%, #f8d7da 100%);
    border: 2px solid #e53935;
    border-radius: 12px;
    padding: 18px 24px;
    box-shadow: 0 4px 20px rgba(229,57,53,0.2);
    animation: fadeReveal 0.35s ease;
    color: #4a0010;
    font-family: 'JetBrains Mono', monospace;
    text-align: center;
}
.hover-reveal-wrapper:hover .hover-reveal-locked              { display: none; }
.hover-reveal-wrapper:hover .hover-reveal-content-yellow      { display: block; }
.hover-reveal-wrapper:hover .hover-reveal-content-blue        { display: block; }
.hover-reveal-wrapper:hover .hover-reveal-content-red         { display: block; }

/* ---- PANEL SECRETO ---- */
.secret-panel-locked {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 2px dashed #555;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    color: #888;
    font-family: 'Sora', sans-serif !important;
    margin: 10px 0 18px 0;
}
.secret-panel-locked .lock-icon { font-size: 36px; margin-bottom: 8px; }
.secret-panel-locked .lock-text { font-size: 14px; color: #666; }

/* Panel revelado — amarillo (mi laptop) */
.secret-panel-revealed-yellow {
    background: linear-gradient(135deg, #2a1f00 0%, #3d2e00 100%);
    border: 2px solid #FBC02D;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 10px 0 18px 0;
    box-shadow: 0 0 25px rgba(251,192,45,0.35);
    animation: fadeReveal 0.5s ease;
}
/* Panel revelado — azul (laptop del amigo, no se usa pero por completitud) */
.secret-panel-revealed-blue {
    background: linear-gradient(135deg, #001a2e 0%, #002d4a 100%);
    border: 2px solid #4299E1;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 10px 0 18px 0;
    box-shadow: 0 0 25px rgba(66,153,225,0.35);
    animation: fadeReveal 0.5s ease;
}

@keyframes fadeReveal {
    from { opacity: 0; transform: translateY(-8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---- TABLA MI LAPTOP (amarilla) ---- */
.tabla-yellow { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
.tabla-yellow thead tr { background-color: #FBC02D; color: #1a1200; }
.tabla-yellow thead th { padding: 10px 14px; text-align: center; font-family: 'Sora', sans-serif; font-weight: 700; letter-spacing: 0.5px; }
.tabla-yellow tbody tr:nth-child(odd)  { background-color: #fffde7; color: #3d2e00; }
.tabla-yellow tbody tr:nth-child(even) { background-color: #fff9c4; color: #3d2e00; }
.tabla-yellow tbody td { padding: 9px 14px; text-align: center; border-bottom: 1px solid #f9e2a0; }
.tabla-yellow tbody tr:hover { background-color: #fff176; }

/* ---- TABLA LAPTOP AMIGO (azul) ---- */
.tabla-blue { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
.tabla-blue thead tr { background-color: #2B6CB0; color: #e8f4ff; }
.tabla-blue thead th { padding: 10px 14px; text-align: center; font-family: 'Sora', sans-serif; font-weight: 700; letter-spacing: 0.5px; }
.tabla-blue tbody tr:nth-child(odd)  { background-color: #ebf4ff; color: #1A365D; }
.tabla-blue tbody tr:nth-child(even) { background-color: #dbeafe; color: #1A365D; }
.tabla-blue tbody td { padding: 9px 14px; text-align: center; border-bottom: 1px solid #bee3f8; }
.tabla-blue tbody tr:hover { background-color: #bfdbfe; }

/* Glows */
.glow-n {
    color: #f0c27f; font-weight: 900;
    font-family: 'JetBrains Mono', monospace !important;
    text-shadow: 0 0 8px #f0c27f, 0 0 20px #f0a500, 0 0 40px #f07000;
    animation: pulse-n 1.8s ease-in-out infinite;
}
.glow-e {
    color: #7dd6f4; font-weight: 900;
    font-family: 'JetBrains Mono', monospace !important;
    text-shadow: 0 0 8px #7dd6f4, 0 0 20px #4ab8f0, 0 0 40px #2090d0;
    animation: pulse-e 1.8s ease-in-out infinite;
}
.glow-d {
    color: #f87171; font-weight: 900;
    font-family: 'JetBrains Mono', monospace !important;
    text-shadow: 0 0 8px #f87171, 0 0 20px #ef4444, 0 0 40px #cc0000;
    animation: pulse-d 1.8s ease-in-out infinite;
}
.glow-n-private {
    color: #f0c27f; font-weight: 900;
    font-family: 'JetBrains Mono', monospace !important;
    text-shadow: 0 0 8px #f0c27f, 0 0 20px #f0a500, 0 0 40px #f07000;
    animation: pulse-n 1.8s ease-in-out infinite;
}
@keyframes pulse-n {
    0%,100% { text-shadow: 0 0 8px #f0c27f,0 0 20px #f0a500,0 0 30px #f07000; }
    50% { text-shadow: 0 0 15px #f0c27f,0 0 35px #f0a500,0 0 60px #f07000; }
}
@keyframes pulse-e {
    0%,100% { text-shadow: 0 0 8px #7dd6f4,0 0 20px #4ab8f0,0 0 30px #2090d0; }
    50% { text-shadow: 0 0 15px #7dd6f4,0 0 35px #4ab8f0,0 0 60px #2090d0; }
}
@keyframes pulse-d {
    0%,100% { text-shadow: 0 0 8px #f87171,0 0 20px #ef4444,0 0 30px #cc0000; }
    50% { text-shadow: 0 0 15px #f87171,0 0 35px #ef4444,0 0 60px #cc0000; }
}

.key-box { padding:30px; border-radius:15px; color:white; min-height:200px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; margin-bottom:20px; box-shadow:2px 2px 10px rgba(0,0,0,0.1); }
.public-box { background-color:#4299E1; border:3px solid #2B6CB0; }
.private-box { background-color:#F87171; border:3px solid #EF4444; }
.key-box-glow-public { padding:15px; border-radius:12px; color:white; min-height:120px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; margin-bottom:10px; background-color:#1a2a4a; border:2px solid #4299E1; box-shadow:0 0 20px rgba(66,153,225,0.4); }
.key-box-glow-private { padding:15px; border-radius:12px; color:white; min-height:120px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; margin-bottom:10px; background-color:#2a1a1a; border:2px solid #F87171; box-shadow:0 0 20px rgba(248,113,113,0.4); }
.theory-box { background-color:#FFFDE7; border:1px solid #FBC02D; padding:20px; border-radius:10px; color:#333; margin-top:10px; margin-bottom:20px; font-family:'Sora',sans-serif !important; }
.warning-box { background-color:#FFF3CD; border:2px solid #FF8C00; padding:15px; border-radius:10px; color:#7a4100; margin-top:10px; margin-bottom:10px; font-family:'Sora',sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# --- Helper: render tabla coloreada ---
def render_tabla_yellow(filas, columnas):
    html = f'<table class="tabla-yellow"><thead><tr>'
    for col in columnas:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    for fila in filas:
        html += '<tr>'
        for col in columnas:
            html += f'<td>{fila.get(col,"")}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)

def render_tabla_blue(filas, columnas):
    html = f'<table class="tabla-blue"><thead><tr>'
    for col in columnas:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    for fila in filas:
        html += '<tr>'
        for col in columnas:
            html += f'<td>{fila.get(col,"")}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)

# --- Inline glow spans (funcionan dentro de hover panels) ---
GLOW_N_STYLE  = "color:#b45309;font-weight:900;font-family:'JetBrains Mono',monospace;text-shadow:0 0 6px #f0c27f,0 0 14px #f0a500,0 0 28px #f07000;"
GLOW_E_STYLE  = "color:#1d6fa4;font-weight:900;font-family:'JetBrains Mono',monospace;text-shadow:0 0 6px #7dd6f4,0 0 14px #4ab8f0,0 0 28px #2090d0;"
GLOW_D_STYLE  = "color:#b91c1c;font-weight:900;font-family:'JetBrains Mono',monospace;text-shadow:0 0 6px #f87171,0 0 14px #ef4444,0 0 28px #cc0000;"

def gn(v):  return f'<span style="{GLOW_N_STYLE}">{v}</span>'
def ge(v):  return f'<span style="{GLOW_E_STYLE}">{v}</span>'
def gd(v):  return f'<span style="{GLOW_D_STYLE}">{v}</span>'

def estilo_mi_laptop():
    st.markdown("""
    <style>
    .stApp { background-color:#FFFFFF; color:#4A4A4A; border:15px solid #FFEB3B; border-radius:20px; }
    .laptop-header { background-color:#FFEB3B; padding:10px; border-radius:10px 10px 0 0; border-bottom:2px solid #FBC02D; text-align:center; color:#7F6D00; font-weight:bold; }
    .stButton>button { background-color:#FBC02D; color:black; border-radius:10px; font-weight:bold; }
    </style>
    <div class="laptop-header">💻 MY LAPTOP (PRIVATE — YELLOW)</div>
    """, unsafe_allow_html=True)

def estilo_laptop_amigo():
    st.markdown("""
    <style>
    .stApp { background-color:#F0F8FF; color:#1A365D; border:15px solid #4299E1; border-radius:20px; }
    .laptop-header { background-color:#4299E1; padding:10px; border-radius:10px 10px 0 0; border-bottom:2px solid #2B6CB0; text-align:center; color:white; font-weight:bold; }
    </style>
    <div class="laptop-header">💻 FRIEND'S LAPTOP (PUBLIC — BLUE)</div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STEP 0: Introduction
# ─────────────────────────────────────────────
if st.session_state.paso == 0:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');
    
    .intro-header { 
        background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); 
        color:white; 
        padding:50px; 
        border-radius:20px; 
        text-align:center; 
        margin-bottom:30px; 
        box-shadow:0 8px 32px rgba(102,126,234,0.4);
        animation: slideDown 0.6s ease;
        font-family:'Sora',sans-serif; 
    }
    .intro-title { 
        font-size:56px; 
        font-weight:bold; 
        margin-bottom:10px;
        letter-spacing:2px;
    }
    .intro-subtitle { 
        font-size:24px; 
        opacity:0.95;
        font-weight:500;
    }
    
    .features-grid {
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        gap:20px;
        margin:30px 0;
    }
    .feature-card {
        background:linear-gradient(135deg,#f5f7fa 0%,#c3cfe2 100%);
        padding:30px;
        border-radius:15px;
        text-align:center;
        transition:transform 0.3s, box-shadow 0.3s;
        border:2px solid transparent;
        animation: fadeInUp 0.6s ease backwards;
    }
    .feature-card:hover {
        transform:translateY(-8px);
        box-shadow:0 12px 24px rgba(0,0,0,0.15);
        border-color:#667eea;
    }
    .feature-card:nth-child(1) { animation-delay:0.1s; }
    .feature-card:nth-child(2) { animation-delay:0.2s; }
    .feature-card:nth-child(3) { animation-delay:0.3s; }
    
    .feature-icon {
        font-size:48px;
        margin-bottom:15px;
    }
    .feature-title {
        font-size:20px;
        font-weight:700;
        color:#333;
        margin-bottom:10px;
        font-family:'Sora',sans-serif;
    }
    .feature-text {
        font-size:14px;
        color:#555;
        font-family:'Sora',sans-serif;
        line-height:1.6;
    }
    
    .intro-content { 
        background:linear-gradient(135deg,#f0f8ff 0%,#fff0f5 100%);
        padding:35px; 
        border-left:6px solid #667eea; 
        border-radius:12px; 
        margin-bottom:20px; 
        font-family:'Sora',sans-serif;
        box-shadow:0 4px 15px rgba(102,126,234,0.1);
        animation: fadeInUp 0.6s ease 0.4s backwards;
    }
    
    .intro-content h3 {
        color:#667eea;
        margin-top:0;
        font-size:24px;
    }
    
    .intro-content p {
        color:#444;
        line-height:1.8;
    }
    
    .intro-content ul {
        color:#555;
    }
    
    .intro-content li {
        margin:8px 0;
        line-height:1.8;
    }
    
    .key-comparison {
        display:flex;
        gap:20px;
        margin:20px 0;
        justify-content:center;
    }
    
    .key-type {
        flex:1;
        padding:20px;
        border-radius:10px;
        text-align:center;
        font-family:'JetBrains Mono',monospace;
        transition:transform 0.3s;
    }
    
    .key-type:hover {
        transform:scale(1.05);
    }
    
    .key-public {
        background:linear-gradient(135deg,#e3f2fd 0%,#bbdefb 100%);
        border:2px solid #1976D2;
        color:#0d2d4e;
    }
    
    .key-private{
        background:linear-gradient(135deg,#fce4ec 0%,#f8d7da 100%);
        border:2px solid #e53935;
        color:#4a0010;
    }
    
    .key-label {
        font-size:12px;
        text-transform:uppercase;
        letter-spacing:1.5px;
        font-weight:700;
        margin-bottom:8px;
        font-family:'Sora',sans-serif;
    }
    
    .key-content {
        font-size:16px;
        font-weight:700;
    }
    
    .start-button-wrapper {
        display:flex;
        justify-content:center;
        margin-top:40px;
        animation: fadeInUp 0.6s ease 0.6s backwards;
    }
    
    @keyframes slideDown {
        from { opacity:0; transform:translateY(-30px); }
        to { opacity:1; transform:translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity:0; transform:translateY(20px); }
        to { opacity:1; transform:translateY(0); }
    }
    </style>
    
    <div class="intro-header">
        <div class="intro-title">🔐 RSA Cryptography</div>
        <div class="intro-subtitle">Rivest, Shamir, Adleman — Since 1977</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="intro-content">
    <h3>🎯 What is RSA?</h3>
    <p><b>RSA</b> is an asymmetric cryptography algorithm that revolutionized digital security. 
    Unlike symmetric cryptography, where the same key encrypts and decrypts, RSA uses two mathematically linked keys 
    that work together but cannot be derived from each other.</p>
    
    <div class="key-comparison">
        <div class="key-type key-public">
            <div class="key-label">🌎 Public Key</div>
            <div class="key-content">Shared with everyone<br>Used to encrypt</div>
        </div>
        <div class="key-type key-private">
            <div class="key-label">🛑 Private Key</div>
            <div class="key-content">Kept secret<br>Used to decrypt</div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🔑</div>
            <div class="feature-title">Key Generation</div>
            <div class="feature-text">Generate your public/private key pair by selecting two prime numbers.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">✉️</div>
            <div class="feature-title">Encryption</div>
            <div class="feature-text">Your friend uses your public key to encrypt a secret message.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔓</div>
            <div class="feature-title">Decryption</div>
            <div class="feature-text">Use your private key to recover the original message.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="intro-content">
    <h3>📦 How RSA Works in Practice</h3>
    <p>In real-world applications, RSA encrypts <b>blocks of text</b> — large chunks of data processed together for efficiency and security.</p>
    <ul>
    </ul>
    
    <p style="background:#e8f5e9; padding:16px; border-radius:8px; border-left:4px solid #4caf50; margin-top:20px;">
        <b>💡 Why this simulator encrypts letter-by-letter:</b><br>
        To help you understand the <b>mathematical process step-by-step</b>, we encrypt one letter at a time. 
        This makes it easier to see exactly how the formula works: taking each ASCII value, raising it to power <b>e</b>, 
        and reducing modulo <b>n</b>. Once you master this, you'll understand how real block encryption operates!
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Start Simulator", key="start_button", use_container_width=True):
            st.session_state.paso = 1
            st.rerun()

# ─────────────────────────────────────────────
# STEP 1: Key Generation (My Laptop — yellow)
# ─────────────────────────────────────────────
elif st.session_state.paso == 1:
    estilo_mi_laptop()
    st.header("Step 1: Key Generation")

    col_p, col_q = st.columns(2)
    with col_p: p = st.number_input("Choose prime p:", value=61)
    with col_q: q = st.number_input("Choose prime q:", value=53)

    if es_primo(p) and es_primo(q) and p != q:
        n   = p * q
        phi = (p-1) * (q-1)

        st.markdown(f"""
        <div class="formula-block">
            <div class="formula-label">Step 1 — Compute the modulus n</div>
            <div class="formula-general">n = p × q</div>
            <div class="formula-note">n is the public modulus used in both encryption and decryption.</div>
        </div>
        <div class="hover-reveal-wrapper">
            <div class="hover-reveal-locked">
                <span style="font-size:20px;">🔢</span>&nbsp; <b>Substituted formula</b>
            </div>
            <div class="hover-reveal-content-yellow">
                <span style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#e65100;font-family:'Sora',sans-serif;font-weight:700;">With your values</span><br><br>
                <span style="font-family:'JetBrains Mono',monospace;font-size:17px;">n = {p} × {q} = <b>{n}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="formula-block">
            <div class="formula-label">Step 2 — Calculate the Euler function value</div>
            <div class="formula-general">φ(n) = (p − 1) × (q − 1)</div>
            <div class="formula-note">φ(n) counts how many integers less than n are coprime to n. It is kept secret.</div>
        </div>
        <div class="hover-reveal-wrapper">
            <div class="hover-reveal-locked">
                <span style="font-size:20px;">🔢</span>&nbsp; <b>Substituted formula</b>
            </div>
            <div class="hover-reveal-content-yellow">
                <span style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#e65100;font-family:'Sora',sans-serif;font-weight:700;">With your values</span><br><br>
                <span style="font-family:'JetBrains Mono',monospace;font-size:17px;">φ(n) = ({p} − 1) × ({q} − 1) = <b>{phi}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🎯 Choosing the Public Exponent 'e'")
        limite_inf = max(p+1, q+1)

        st.markdown(f"""
        <div class="formula-block">
            <div class="formula-label">Step 3 — Choose e satisfying two rules</div>
            <div class="formula-general">e ∈ (max(p+1,q+1) ; φ(n))  AND  gcd(e, φ(n)) = 1</div>
            <div class="formula-note">
                Rule 1: e must lie strictly between max(p,q) and φ(n).<br>
                Rule 2: e must be <b>coprime</b> with φ(n) — i.e. they share no common factor other than 1.<br>
                ⚠️ If the resulting d is smaller than log²(n) = {round(math.log(n)**2,2):.2f}, choose a different e.
            </div>
        </div>
        <div class="hover-reveal-wrapper">
            <div class="hover-reveal-locked">
                <span style="font-size:20px;">🔢</span>&nbsp; <b>Substituted formula</b>
            </div>
            <div class="hover-reveal-content-yellow">
                <span style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#e65100;font-family:'Sora',sans-serif;font-weight:700;">With your values</span><br><br>
                <span style="font-family:'JetBrains Mono',monospace;font-size:17px;">e ∈ ({limite_inf} ; {phi}) &nbsp;&nbsp; AND &nbsp;&nbsp; gcd(e, {phi}) = 1</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        e = st.number_input(f"Enter e (> {limite_inf}, coprime with φ(n)={phi}):", value=max(limite_inf+1, 17))
        log2n = math.log(n) ** 2

        if mcd(e, phi) == 1 and limite_inf < e < phi:
            d_real = inverso_modular(e, phi)

            if d_real < log2n:
                st.markdown(f"""
                <div class="warning-box">
                ⚠️ <b>Security Warning (Wiener's Attack):</b> The computed d = {d_real} is smaller than 
                log²(n) ≈ {log2n:.2f}. This makes the private key vulnerable. 
                Please choose a different value of e.
                </div>
                """, unsafe_allow_html=True)
            else:
                # Formula d — bloque pastel amarillo igual que el resto
                st.markdown(f"""
                <div class="formula-block">
                    <div class="formula-label">Step 4 — Compute the private exponent d (modular inverse)</div>
                    <div class="formula-general">d × e ≡ 1 (mod φ(n))</div>
                    <div class="formula-note">d is the unique modular inverse of e with respect to φ(n), found using the Extended Euclidean Algorithm. Calculate d first to reveal it.</div>
                </div>
                """, unsafe_allow_html=True)

                col_pub, col_priv = st.columns(2)

                with col_pub:
                    st.markdown(f"""<div class="key-box public-box">
                        <h3 style="margin:0;color:white;">🌎 PUBLIC KEY</h3>
                        <p style="font-family:'JetBrains Mono',monospace;font-size:22px;margin:15px 0;">(n={n}, e={e})</p>
                        <p style="font-size:14px;margin:0;">📢 Ready to share with anyone.</p>
                    </div>""", unsafe_allow_html=True)

                with col_priv:
                    if not st.session_state.d_busqueda_completa:
                        st.markdown("""
                        <div class="secret-panel-locked">
                            <div class="lock-icon">🔒</div>
                            <b style="color:#aaa;">PRIVATE KEY</b>
                            <div class="lock-text">d not calculated yet.<br>Press the button to search.</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("🔍 Calculate d"):
                            placeholder = st.empty()
                            for i in range(0, d_real, max(1, d_real // 10)):
                                placeholder.warning(f"Searching for d... {i}")
                                time.sleep(0.05)
                            placeholder.empty()
                            st.session_state.d_busqueda_completa = True
                            st.rerun()
                    else:
                        # Fórmula sustituida — pastel amarillo sin glows
                        st.markdown(f"""
                        <div class="formula-block">
                            <div class="formula-label">Step 4 — d found ✓</div>
                            <div class="formula-general">d × {e} ≡ 1 (mod {phi})</div>
                            <div class="formula-substituted">→ d = {d_real}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Panel de llave privada — hover para revelar
                        st.markdown(f"""
                        <div class="hover-reveal-wrapper">
                            <div class="hover-reveal-locked">
                                <div style="font-size:32px;margin-bottom:6px;">🛡️</div>
                                <b>PRIVATE KEY</b>
                            </div>
                            <div class="hover-reveal-content-red">
                                <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#c62828;font-family:'Sora',sans-serif;font-weight:700;margin-bottom:10px;">🛑 PRIVATE KEY</div>
                                <div style="font-size:22px;font-weight:700;font-family:'JetBrains Mono',monospace;">(n = {n}, d = {d_real})</div>
                                <div style="font-size:12px;color:#b71c1c;margin-top:8px;font-family:'Sora',sans-serif;">⚠️ Never share this.</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if st.session_state.d_busqueda_completa:
                    if st.button("Send Public Key over the Network ➡️"):
                        st.session_state.mis_llaves = {'n':n,'e':e,'d':d_real}
                        st.session_state.paso = 1.5
                        st.rerun()
        else:
            st.error("⚠️ 'e' does not meet the requirements: check the range and that gcd(e, φ(n)) = 1.")
    else:
        st.warning("Please enter two different prime numbers.")

# ─────────────────────────────────────────────
# STEP 1.5: Transition
# ─────────────────────────────────────────────
elif st.session_state.paso == 1.5:
    st.header("🌐 Transmitting public key over the network...")
    st.progress(100)
    time.sleep(0.5)
    if st.button("Open Friend's Laptop ➡️"):
        st.session_state.paso = 2
        st.rerun()

# ─────────────────────────────────────────────
# STEP 2: Encryption (Friend's Laptop — blue)
# ─────────────────────────────────────────────
elif st.session_state.paso == 2:
    estilo_laptop_amigo()
    llaves  = st.session_state.mis_llaves
    n_val   = llaves['n']
    e_val   = llaves['e']
    st.header("Step 2: Friend's Perspective — Encryption")

    st.markdown(f"""
    <div class="key-box-glow-public">
        <h4 style="margin:0;color:#89b4fa;font-family:'Sora',sans-serif;">🔑 Received Public Key</h4>
        <p style="font-family:'JetBrains Mono',monospace;font-size:22px;margin:10px 0;">
            <span class="glow-n">n = {n_val}</span> &nbsp;&nbsp; <span class="glow-e">e = {e_val}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Fórmula general visible — azul (Friend's Laptop)
    st.markdown(f"""
    <div class="formula-block-blue">
        <div class="formula-label">Encryption Formula</div>
        <div class="formula-general">c = m<sup>{ge('e')}</sup> mod {gn('n')}</div>
        <div class="formula-note">
            Each letter is converted to its ASCII value <b>m</b>, then raised to the public exponent 
            <span class="glow-e">e</span> and reduced modulo <span class="glow-n">n</span> to produce 
            the ciphertext <b>c</b>. Without knowing the private key, reversing this is computationally infeasible.
        </div>
    </div>
    <div class="hover-reveal-wrapper">
        <div class="hover-reveal-locked">
            <span style="font-size:20px;">🔢</span>&nbsp; <b>Substituted formula</b>
        </div>
        <div class="hover-reveal-content-blue">
            <span style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#1565C0;font-family:'Sora',sans-serif;font-weight:700;">With public key values</span><br><br>
            <span style="font-family:'JetBrains Mono',monospace;font-size:17px;">c = m<sup>{ge(e_val)}</sup> mod {gn(n_val)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    mensaje = st.text_input("Enter the secret message (M):", "RSA")

    if mensaje:
        st.markdown("---")
        st.subheader("🚀 Step-by-Step Encoding Process")

        datos = []
        for l in mensaje:
            m = ord(l)
            c = pow(m, e_val, n_val)
            datos.append({"Letter": l, "ASCII (m)": m, "Encrypted (c)": c})

        # Animated cards for each letter
        cards_html = ""
        colors = ["#3b82f6","#8b5cf6","#06b6d4","#10b981","#f59e0b","#ef4444","#ec4899"]
        for i, d in enumerate(datos):
            col = colors[i % len(colors)]
            delay = i * 0.12
            cards_html += f"""
            <div class="enc-card" style="border-color:{col};animation-delay:{delay}s;">
                <div class="enc-letter" style="color:{col};">{d['Letter']}</div>
                <div class="enc-step">
                    ASCII → <b style="color:{col};">{d['ASCII (m)']}</b>
                </div>
                <div class="enc-arrow">↓</div>
                <div class="enc-step">
                    <span style="font-family:'JetBrains Mono',monospace;">{d['ASCII (m)']}<sup>{e_val}</sup> mod {n_val}</span>
                </div>
                <div class="enc-arrow">↓</div>
                <div class="enc-result" style="border-color:{col};background:{col}15;">
                    🔒 <b style="color:{col};font-size:20px;">{d['Encrypted (c)']}</b>
                </div>
            </div>"""

        st.markdown(f"""
        <style>
        .enc-grid {{ display:flex; flex-wrap:wrap; gap:14px; margin:16px 0 24px 0; justify-content:center; }}
        .enc-card {{
            background:#001a35; border:2px solid #4299E1; border-radius:14px;
            padding:16px 20px; min-width:140px; flex:1; max-width:180px;
            text-align:center; font-family:'Sora',sans-serif;
            animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) both;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .enc-letter {{ font-size:36px; font-weight:900; margin-bottom:10px; font-family:'JetBrains Mono',monospace; }}
        .enc-step {{ font-size:12px; color:#94a3b8; margin:6px 0; }}
        .enc-badge {{ font-size:10px; padding:2px 7px; border-radius:20px; font-weight:700; margin-right:5px; display:inline-block; }}
        .enc-arrow {{ color:#475569; font-size:18px; margin:2px 0; }}
        .enc-result {{ border:2px solid; border-radius:10px; padding:10px; margin-top:8px; font-family:'JetBrains Mono',monospace; font-size:13px; color:#94a3b8; }}
        @keyframes cardPop {{
            from {{ opacity:0; transform:translateY(20px) scale(0.85); }}
            to   {{ opacity:1; transform:translateY(0) scale(1); }}
        }}
        .enc-summary {{ background:linear-gradient(135deg,#001a35,#002952); border:2px solid #4299E1;
            border-radius:12px; padding:16px 24px; margin:8px 0 16px 0; text-align:center;
            font-family:'JetBrains Mono',monospace; color:#90cdf4; font-size:14px; }}
        </style>
        <div class="enc-grid">{cards_html}</div>
        <div class="enc-summary">
            📨 Encrypted sequence: &nbsp;
            <b style="color:#63b3ed;">[ {' , '.join(str(d['Encrypted (c)']) for d in datos)} ]</b>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Send Encrypted Message 📤"):
            st.session_state.cifrado = [d['Encrypted (c)'] for d in datos]
            st.session_state.paso = 3
            st.rerun()

# ─────────────────────────────────────────────
# STEP 3: Decryption (My Laptop — yellow)
# ─────────────────────────────────────────────
elif st.session_state.paso == 3:
    estilo_mi_laptop()
    llaves = st.session_state.mis_llaves
    n_val  = llaves['n']
    d_val  = llaves['d']
    e_val  = llaves['e']
    st.header("Step 3: Final Decryption")

    # Private key — hover para revelar
    st.markdown(f"""
    <div class="hover-reveal-wrapper">
        <div class="hover-reveal-locked" style="min-height:80px;display:flex;align-items:center;justify-content:center;gap:10px;">
            <span style="font-size:28px;">🛑</span>
            <div><b>MY PRIVATE KEY</b></div>
        </div>
        <div class="hover-reveal-content-red">
            <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#c62828;font-family:'Sora',sans-serif;font-weight:700;margin-bottom:10px;">🛑 My Private Key</div>
            <div style="font-size:22px;font-weight:700;font-family:'JetBrains Mono',monospace;">
                n = {gn(n_val)} &nbsp;&nbsp; d = {gd(d_val)}
            </div>
            <div style="font-size:12px;color:#b71c1c;margin-top:10px;font-family:'Sora',sans-serif;">⚠️ Never share this value.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fórmula general visible
    st.markdown(f"""
    <div class="formula-block">
        <div class="formula-label">Decryption Formula</div>
        <div class="formula-general">m = c<sup>{gd('d')}</sup> mod {gn('n')}</div>
        <div class="formula-note">
            Each encrypted value <b>c</b> is raised to the private exponent 
            <b>d</b> and reduced modulo <b>n</b> to recover the original ASCII value <b>m</b>.
        </div>
    </div>
    <div class="hover-reveal-wrapper">
        <div class="hover-reveal-locked">
            <span style="font-size:20px;">🔢</span>&nbsp; <b>Substituted formula</b>
        </div>
        <div class="hover-reveal-content-yellow">
            <span style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#e65100;font-family:'Sora',sans-serif;font-weight:700;">With your private key values</span><br><br>
            <span style="font-family:'JetBrains Mono',monospace;font-size:17px;">m = c<sup>{gd(d_val)}</sup> mod {gn(n_val)}</span><br>
            <span style="font-size:12px;color:#795548;font-family:'Sora',sans-serif;margin-top:6px;display:block;">Replace c with each encrypted value to recover the original letter.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("**Encrypted codes received:**")
    st.code(st.session_state.cifrado)

    if st.button("🔓 Decrypt with my private key d"):
        res = []
        col_op = f"Operation: c^{d_val} mod {n_val}"
        for c in st.session_state.cifrado:
            m = pow(c, d_val, n_val)
            res.append({
                "Encrypted (c)": c,
                col_op: f"{c}^{d_val} mod {n_val}",
                "ASCII (m)": m,
                "Letter": chr(m)
            })
        st.session_state.resultado_descifrado = res
        st.rerun()

    if st.session_state.resultado_descifrado:
        res = st.session_state.resultado_descifrado
        st.subheader("📬 Decryption Results")

        # Animated decryption cards
        dcards_html = ""
        colors = ["#f87171","#fb923c","#facc15","#4ade80","#34d399","#60a5fa","#c084fc"]
        for i, r in enumerate(res):
            col = colors[i % len(colors)]
            delay = i * 0.15
            dcards_html += f"""
            <div class="dec-card" style="border-color:{col};animation-delay:{delay}s;">
                <div class="dec-cipher" style="margin-bottom:6px;">🔒 {r['Encrypted (c)']}</div>
                <div class="dec-arrow" style="color:{col};">↓</div>
                <div class="dec-op" style="font-size:11px;margin:4px 0;">
                    {r['Encrypted (c)']}<sup>{d_val}</sup> mod {n_val}
                </div>
                <div class="dec-arrow" style="color:{col};">↓</div>
                <div class="dec-ascii" style="font-size:12px;margin:4px 0;">ASCII: {r['ASCII (m)']}</div>
                <div class="dec-letter" style="color:{col};">{r['Letter']}</div>
            </div>"""

        mensaje_recuperado = ''.join([r['Letter'] for r in res])
        st.markdown(f"""
        <style>
        .dec-grid {{ display:flex; flex-wrap:wrap; gap:14px; margin:16px 0 20px 0; justify-content:center; }}
        .dec-card {{
            background:linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%); 
            border:2px solid #f9a825; 
            border-radius:14px;
            padding:14px 18px; 
            min-width:120px; 
            flex:1; 
            max-width:160px;
            text-align:center; 
            font-family:'JetBrains Mono',monospace;
            animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) both;
            box-shadow: 0 4px 20px rgba(249,168,37,0.2);
            color: #5a4200;
        }}
        .dec-arrow {{ font-size:16px; margin:2px 0; color: #f9a825; }}
        .dec-letter {{ font-size:38px; font-weight:900; margin-top:6px; font-family:'JetBrains Mono',monospace; color: #bf360c; }}
        .dec-cipher {{ color: #7a5d00 !important; font-size:12px; }}
        .dec-op {{ color: #7a5d00 !important; font-size:11px; }}
        .dec-ascii {{ color: #7a5d00 !important; font-size:12px; }}
        .dec-final-banner {{
            background: linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%);
            border: 3px solid #f9a825;
            border-radius: 14px;
            padding: 24px 32px;
            text-align: center;
            margin: 16px 0 16px 0;
            box-shadow: 0 6px 30px rgba(249,168,37,0.3);
            animation: fadeReveal 0.6s ease;
        }}
        </style>
        <div class="dec-grid">{dcards_html}</div>
        <div class="dec-final-banner">
            <div style="font-size:13px;color:#e65100;font-family:'Sora',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">✨ Message Recovered</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:36px;font-weight:900;color:#bf360c;letter-spacing:4px;">{mensaje_recuperado}</div>
        </div>
        """, unsafe_allow_html=True)

        st.balloons()

        if st.button("🔄 Restart Simulator"):
            st.session_state.paso = 1
            st.session_state.mis_llaves = {}
            st.session_state.d_busqueda_completa = False
            st.session_state.mostrar_llave_privada_paso1 = False
            st.session_state.mostrar_llave_privada_paso3 = False
            st.session_state.mostrar_formula_sustituida_paso3 = False
            st.session_state.resultado_descifrado = None
            if 'cifrado' in st.session_state:
                del st.session_state.cifrado
            st.rerun()