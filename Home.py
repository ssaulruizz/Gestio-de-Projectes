import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Comparador EDV Incasòl", layout="wide")

st.title("📊 Comparador d'Estudis de Viabilitat (EDV) - Incasòl")

st.markdown("""
Aquesta eina permet comparar diferents **Estudis de Viabilitat (EDV)** de sectors d'Incasòl 
segons les seves variables econòmiques i físiques (p.ex. *Aprofitament privats*, *Obres d'urbanització*, etc.).
""")

# --- File upload ---
st.sidebar.header("📁 Dades")
uploaded_file = st.sidebar.file_uploader("Puja el fitxer Excel amb les dades EDV", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Try reading as Excel or CSV
    try:
        df = pd.read_excel(uploaded_file)
    except:
        df = pd.read_csv(uploaded_file)
    
    st.success("Fitxer carregat correctament ✅")
    
    # Show sample
    st.subheader("Vista prèvia de les dades")
    st.dataframe(df.head())

    # --- Column selection ---
    st.sidebar.header("⚙️ Paràmetres de comparació")
    sector_col = st.sidebar.selectbox("Selecciona la columna de sectors o actuacions", df.columns)
    variable_cols = st.sidebar.multiselect("Selecciona variables a comparar", df.select_dtypes(include=["number", "float", "int"]).columns)
    
    selected_sectors = st.sidebar.multiselect("Selecciona sectors per comparar", df[sector_col].unique())
    
    if selected_sectors and variable_cols:
        # Filter dataframe
        filtered_df = df[df[sector_col].isin(selected_sectors)]

        st.subheader("📈 Comparació gràfica")
        tab1, tab2 = st.tabs(["Gràfic", "Taula"])
        
        with tab1:
            for var in variable_cols:
                fig = px.bar(
                    filtered_df,
                    x=sector_col,
                    y=var,
                    color=sector_col,
                    title=f"Comparació de {var}",
                    text_auto=True
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.dataframe(filtered_df[[sector_col] + variable_cols])
    else:
        st.info("Selecciona almenys un sector i una variable per veure la comparació.")
else:
    st.warning("Puja un fitxer per començar.")

st.markdown("---")
st.caption("Disseny desenvolupat per Saül Ruiz Cazáñez · Projecte EDV Incasòl · © 2025")