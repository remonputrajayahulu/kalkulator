import streamlit as st
import sympy as sp
import plotly.graph_objects as go
import numpy as np

# Konfigurasi Tampilan Wide Mode
st.set_page_config(
    page_title="Kalkulator-limit 🤓",
    page_icon="📔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Fira+Code:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Quicksand', sans-serif;
    color: #1e293b;
    background-color: #f8fafc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 4rem;
    max-width: 1450px;
}

.book-header {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    padding: 2rem 2.5rem;
    border-radius: 24px;
    color: #ffffff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    box-shadow: 0 15px 35px rgba(56, 189, 248, 0.25);
}

.book-title {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
}

.book-subtitle {
    font-size: 1rem;
    font-weight: 700;
    margin: 0;
}

.bright-card {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.5rem;
}

.result-bright-success {
    background: #f0fdf4;
    border: 2px solid #bbf7d0;
    border-left: 6px solid #10b981;
    padding: 1.2rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}

.result-bright-error {
    background: #fef2f2;
    border: 2px solid #fecaca;
    border-left: 6px solid #ef4444;
    padding: 1.2rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}

div.stButton > button:first-child {
    background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    color: #ffffff;
    font-weight: 700;
    border: none;
    border-radius: 14px;
    padding: 0.7rem 1rem;
    width: 100%;
    box-shadow: 0 10px 20px rgba(249, 115, 22, 0.3);
    font-family: 'Quicksand', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="book-header">
  <div>
    <h1 class="book-title">📔 Kalkulus-limit</h1>
    <p class="book-subtitle">🌠 Eksplorasi limit fungsi, Aturan L'Hôpital, dan kurva interaktif</p>
  </div>
</div>
""", unsafe_allow_html=True)

if "expr_input" not in st.session_state:
    st.session_state.expr_input = "(sin(x) - x) / x**3"
if "point_input" not in st.session_state:
    st.session_state.point_input = "0"

st.markdown('<div class="bright-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2.8, 1, 1.2, 1], vertical_alignment="bottom")

with c1:
    expr_str = st.text_input("💡 Fungsi Matematka f(x):", value=st.session_state.expr_input)

with c2:
    point_str = st.text_input("📖 Titik Limit (x -> a):", value=st.session_state.point_input)

with c3:
    direction_str = st.selectbox("🧭 Arah Pendekatan:", ["Dua Arah (+-)","Dari Kanan (+)","Dari Kiri (-)"])

with c4:
    submit_btn = st.button("🚀 Hitung Sekarang!", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

def solve_limit(expr, x, point, dir_val):
    steps = []
    steps.append({
        "title": "💡 Langkah 1 - Formulasi Awal", 
        "latex": f"\\lim_{{x\\to{sp.latex(point)}}} \\left({sp.latex(expr)} \\right)"
    })
    
    # Penanganan arah pendekatan spesifik
    if dir_val in ['+', '-']:
        res = sp.limit(expr, x, point, dir=dir_val)
        return res, steps

    # Dua arah (+-)
    lim_l = sp.limit(expr, x, point, dir='-')
    lim_r = sp.limit(expr, x, point, dir='+')
    if lim_l != lim_r:
        return sp.nan, steps

    # Cek Aturan L'Hôpital jika bentuk tak tentu (0/0 atau inf/inf)
    num, den = expr.as_numer_denom()
    if den != 1 and point.is_finite:
        it = 1
        while it <= 3:
            try:
                nv = num.subs(x, point)
                dv = den.subs(x, point)
                if (nv == 0 and dv == 0) or (sp.oo in (sp.Abs(nv), sp.Abs(dv))):
                    num_d = sp.diff(num, x)
                    den_d = sp.diff(den, x)
                    steps.append({
                        "title": f"🌠 Langkah L'Hôpital (iterasi {it})",
                        "latex": f"\\lim_{{x\\to{sp.latex(point)}}} \\frac{{{sp.latex(num)}}}{{{sp.latex(den)}}} = \\lim_{{x \\to {sp.latex(point)}}} \\frac{{{sp.latex(num_d)}}}{{{sp.latex(den_d)}}}"
                    })
                    num, den = num_d, den_d
                    it += 1
                else:
                    break
            except Exception:
                break
                
    return sp.limit(expr, x, point), steps

try:
    x = sp.Symbol('x', real=True)
    expr = sp.sympify(expr_str.replace("^", "**"))
    
    if point_str.strip().lower() in ['oo', 'inf', 'infinity']:
        point = sp.oo
    elif '-oo' in point_str or '-inf' in point_str:
        point = -sp.oo
    else:
        point = sp.sympify(point_str)
        
    dir_val = '+' if "Kanan" in direction_str else ('-' if "Kiri" in direction_str else '+-')
    
    limit_res, steps = solve_limit(expr, x, point, dir_val)
    
    col_left, col_right = st.columns([1, 1.1], gap="large")
    
    with col_left:
        st.markdown('<div class="bright-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Hasil Kalkulasi Eksak")
        
        if limit_res is sp.nan:
            st.markdown('<div class="result-bright-error"><b>🎈 DNE:</b> Limit kiri & kanan berbeda.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-bright-success"><b>🌟 Berhasil Dievaluasi</b></div>', unsafe_allow_html=True)
            st.latex(f"\\lim_{{x \\to {sp.latex(point)}}} \\left({sp.latex(expr)}\\right) = {sp.latex(limit_res)}")
            
        # Tampilkan Langkah-langkah penyelesaian
        st.markdown("---")
        st.markdown("#### 📝 Rincian Langkah:")
        for s in steps:
            st.markdown(f"**{s['title']}**")
            st.latex(s['latex'])
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown('<div class="bright-card">', unsafe_allow_html=True)
        st.markdown("### 🎨 Grafik Interaktif")
        fig = go.Figure()
        f_num = sp.lambdify(x, expr, modules=['numpy'])
        
        pt_val = float(point) if point.is_finite else 0.0
        x_v = np.linspace(pt_val - 5, pt_val + 5, 500)
        
        with np.errstate(all='ignore'):
            y_v = f_num(x_v)
            
        fig.add_trace(go.Scatter(x=x_v, y=y_v, mode='lines', line=dict(color='#0284c7', width=3.5)))
        fig.update_layout(template="plotly_white", height=350, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Terjadi Kesalahan: {e}")