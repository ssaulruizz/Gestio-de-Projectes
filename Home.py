import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup
st.set_page_config(page_title="Comparador EDV Incasòl", layout="wide")

st.title("📊 Comparador d'Estudis de Viabilitat (EDV) - Incasòl")
st.markdown("""
Aquesta eina permet comparar diferents **Estudis de Viabilitat (EDV)** de sectors d'Incasòl 
segons les seves variables econòmiques i físiques (p.ex. *Aprofitament privats*, *Obres d'urbanització*, etc.).
""")

# Sidebar
st.sidebar.header("📁 Dades")
uploaded_file = st.sidebar.file_uploader("Puja el fitxer Excel o CSV amb les dades EDV", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Try reading as Excel or CSV
    try:
        df = pd.read_excel(uploaded_file)
    except:
        df = pd.read_csv(uploaded_file)
    
    st.success("✅ Fitxer carregat correctament")
    st.subheader("Vista prèvia de les dades")
    st.dataframe(df.head())

    # Sidebar options
    st.sidebar.header("⚙️ Paràmetres de comparació")
    sector_col = st.sidebar.selectbox("Columna de sectors o actuacions", df.columns)
    numeric_cols = df.select_dtypes(include=["number", "float", "int"]).columns.tolist()
    variable_cols = st.sidebar.multiselect("Variables a comparar", numeric_cols)

    possible_year_cols = [c for c in df.columns if "any" in c.lower() or "year" in c.lower()]
    year_col = st.sidebar.selectbox("Columna d'anys (opcional, per gràfics temporals)", ["(Cap)"] + possible_year_cols)

    selected_sectors = st.sidebar.multiselect("Selecciona sectors per comparar", df[sector_col].unique())

    chart_library = st.sidebar.selectbox(
        "📚 Llibreria de gràfics",
        ["Plotly", "Matplotlib", "Seaborn", "Streamlit"]
    )

    chart_type = st.sidebar.selectbox(
        "Tipus de gràfic",
        ["Barres", "Línies", "Àrea", "Escampament (scatter)", "Caixa (boxplot)", "Histograma", "Mapa (si hi ha lat/lon)"]
    )

    if selected_sectors and variable_cols:
        filtered_df = df[df[sector_col].isin(selected_sectors)]
        st.subheader("📈 Resultats gràfics")
        tab1, tab2 = st.tabs(["Gràfic", "Taula de dades"])

        with tab1:
            for var in variable_cols:
                if chart_library == "Plotly":
                    # === Plotly charts ===
                    if year_col != "(Cap)" and year_col in df.columns:
                        if chart_type == "Línies":
                            fig = px.line(filtered_df, x=year_col, y=var, color=sector_col, markers=True,
                                          title=f"Evolució de {var} per anys")
                        elif chart_type == "Àrea":
                            fig = px.area(filtered_df, x=year_col, y=var, color=sector_col,
                                          title=f"Evolució de {var} per anys")
                        elif chart_type == "Barres":
                            fig = px.bar(filtered_df, x=year_col, y=var, color=sector_col,
                                         barmode="group", title=f"{var} per anys i sector")
                        elif chart_type == "Escampament (scatter)":
                            fig = px.scatter(filtered_df, x=year_col, y=var, color=sector_col,
                                             trendline="ols", title=f"{var} per anys i sector")
                        elif chart_type == "Caixa (boxplot)":
                            fig = px.box(filtered_df, x=sector_col, y=var, color=sector_col,
                                         title=f"Distribució de {var} per anys")
                        else:
                            fig = px.histogram(filtered_df, x=var, color=sector_col, nbins=20,
                                               title=f"Histograma de {var}")
                    else:
                        # Non-temporal
                        if chart_type == "Barres":
                            fig = px.bar(filtered_df, x=sector_col, y=var, color=sector_col,
                                         title=f"Comparació de {var}", text_auto=True)
                        elif chart_type == "Línies":
                            fig = px.line(filtered_df, x=sector_col, y=var, color=sector_col,
                                          title=f"Tendència de {var}", markers=True)
                        elif chart_type == "Àrea":
                            fig = px.area(filtered_df, x=sector_col, y=var, color=sector_col,
                                          title=f"Distribució de {var}")
                        elif chart_type == "Escampament (scatter)":
                            fig = px.scatter(filtered_df, x=sector_col, y=var, color=sector_col,
                                             title=f"Relació entre {sector_col} i {var}")
                        elif chart_type == "Caixa (boxplot)":
                            fig = px.box(filtered_df, x=sector_col, y=var, color=sector_col,
                                         title=f"Distribució de {var}")
                        else:
                            fig = px.histogram(filtered_df, x=var, color=sector_col, nbins=20,
                                               title=f"Histograma de {var}")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_library == "Matplotlib":
                    # === Matplotlib ===
                    fig, ax = plt.subplots(figsize=(8, 5))
                    if chart_type in ["Barres", "Histograma"]:
                        ax.hist(filtered_df[var], bins=20, color="skyblue", edgecolor="black")
                        ax.set_title(f"Histograma de {var}")
                    elif chart_type == "Línies":
                        for sector in selected_sectors:
                            subset = filtered_df[filtered_df[sector_col] == sector]
                            ax.plot(subset[year_col] if year_col != "(Cap)" else range(len(subset)), subset[var], label=sector)
                        ax.legend()
                        ax.set_title(f"Evolució de {var}")
                    st.pyplot(fig)

                elif chart_library == "Seaborn":
                    # === Seaborn ===
                    fig = plt.figure(figsize=(8, 5))
                    if chart_type == "Caixa (boxplot)":
                        sns.boxplot(data=filtered_df, x=sector_col, y=var, hue=sector_col)
                    elif chart_type == "Histograma":
                        sns.histplot(data=filtered_df, x=var, hue=sector_col, multiple="stack")
                    else:
                        sns.lineplot(data=filtered_df, x=year_col if year_col != "(Cap)" else sector_col, y=var, hue=sector_col)
                    st.pyplot(fig)

                elif chart_library == "Streamlit":
                    # === Streamlit native charts ===
                    if chart_type == "Barres":
                        st.bar_chart(filtered_df.set_index(sector_col)[var])
                    elif chart_type == "Línies":
                        st.line_chart(filtered_df.set_index(sector_col)[var])
                    elif chart_type == "Àrea":
                        st.area_chart(filtered_df.set_index(sector_col)[var])
                    elif chart_type == "Mapa (si hi ha lat/lon)" and {"lat", "lon"}.issubset(df.columns):
                        st.map(df[["lat", "lon"]])
                    else:
                        st.warning("Aquest tipus de gràfic no és compatible amb Streamlit natiu.")

        with tab2:
            st.dataframe(filtered_df[[sector_col] + variable_cols + ([year_col] if year_col != "(Cap)" else [])])

else:
    st.warning("Puja un fitxer per començar.")

st.markdown("---")
st.caption("Disseny desenvolupat per Saül Ruiz Cazáñez · Projecte EDV Incasòl · © 2025")
