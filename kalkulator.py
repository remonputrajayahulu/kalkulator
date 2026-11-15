import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kalkulator Limit")
st.title("🧮 Kalkulator Limit")

x = sp.Symbol('x')

fungsi_input = st.text_input("Fungsi f(x):", "(x**2 - 9)/(x - 3)")
titik = st.text_input("Titik Limit (a):", "3")
arah = st.selectbox("Arah:", ["Dua Arah (+-)", "Kiri (-)", "Kanan (+)"])

if st.button("Hitung Sekarang!"):
    try:
        expr = sp.sympify(fungsi_input)
        a = sp.sympify(titik)
        if arah == "Dua Arah (+-)":
            hasil = sp.limit(expr, x, a)
        elif arah == "Kiri (-)":
            hasil = sp.limit(expr, x, a, dir='-')
        else:
            hasil = sp.limit(expr, x, a, dir='+')

        hasil = sp.simplify(hasil)
        st.success(f"Hasil: {hasil}")

        st.subheader("📝 Rincian Langkah:")
        st.latex(r"\lim_{x \to " + sp.latex(a) + r"} " + sp.latex(expr))
        st.write("1. Cek substitusi langsung: kalau hasilnya 0/0, pakai faktor / L'Hopital")
        st.latex(r"= " + sp.latex(sp.factor(expr)))
        st.latex(r"= " + sp.latex(hasil))

        # Grafik
        f = sp.lambdify(x, expr, 'numpy')
        xs = np.linspace(float(a)-4, float(a)+4, 400)
        xs = xs[np.abs(xs-float(a)) > 0.05]
        fig, ax = plt.subplots()
        ax.plot(xs, f(xs))
        ax.axvline(float(a), color='red', linestyle='--')
        ax.grid(True)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}") 
