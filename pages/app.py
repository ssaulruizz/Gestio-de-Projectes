import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Comparador EDV Camps", layout="wide")
st.title("📊 Comparador de sectors - EDV Camps")

uploaded_file = st.file_uploader("📂 Carrega el fitxer Excel", type=["xlsx"])
if uploaded_file:
    df_raw = pd.read_excel(uploaded_file, header=None)

    # Buscar la fila donde está “Informació sector” (columna C)
    info_row_idx = df_raw[df_raw.iloc[:, 2].astype(str).str.contains("Informació sector", case=False, na=False)].index

    if len(info_row_idx) == 0:
        st.error("❌ No s'ha trobat 'Informació sector' al fitxer.")
    else:
        start_row = info_row_idx[0] + 1  # fila siguiente a “Informació sector”

        # --- Extraer variables y valores ---
        variables = df_raw.iloc[start_row:, 3].dropna().tolist()
        df_data = df_raw.iloc[start_row:, 4:]
        sector_names = df_raw.iloc[start_row - 1, 4:].dropna().astype(str).tolist()

        # Asegurar longitudes compatibles
        min_len = min(len(variables), len(df_data))
        df_data = df_data.iloc[:min_len, :len(sector_names)]

        # --- Evitar nombres duplicados ---
        from collections import Counter

        counts = Counter()
        unique_sector_names = []
        for s in sector_names:
            counts[s] += 1
            if counts[s] > 1:
                unique_sector_names.append(f"{s}_{counts[s]}")
            else:
                unique_sector_names.append(s)

        df_data.columns = unique_sector_names
        df_data.index = variables[:min_len]
        df_data.index.name = "Variable"

        # --- Limpieza numérica ---
        def clean_value(x):
            if isinstance(x, str):
                x = x.replace("m²s", "").replace("m²st", "").replace("%", "").replace(",", ".").strip()
                try:
                    return float(x)
                except ValueError:
                    return np.nan
            return x

        df_numeric = df_data.applymap(clean_value)
        df_numeric = df_numeric.apply(pd.to_numeric, errors="coerce")

        st.success("✅ Fitxer carregat correctament.")
        st.subheader("Vista prèvia de les dades")
        st.dataframe(df_data.head(10))

        # --- Selector ---
        st.sidebar.header("⚙️ Opcions de visualització")
        vista = st.sidebar.radio("Tria el tipus de vista", ["Taula", "Gràfic"])

        if vista == "Taula":
            st.subheader("📋 Taula de dades")
            st.dataframe(df_data)

            st.markdown("#### 📊 Estadístiques:")
            mean_sector = df_numeric.mean().round(2)
            st.write("**Mitjana per sector:**")
            st.dataframe(mean_sector)

            overall_mean = df_numeric.stack().mean().round(2)
            st.write(f"**Mitjana global:** {overall_mean:,}")

        else:
            
            st.subheader("📈 Gràfic comparatiu")

            # Convertir el índice a lista explícitamente
            variable_list = df_data.index.tolist()

            selected_vars = st.multiselect(
                "Selecciona variables per comparar:",
                options=variable_list,
                default=variable_list[:5] if len(variable_list) >= 5 else variable_list
            )

            if len(selected_vars) > 0:
                df_plot = df_numeric.loc[selected_vars].T

                # Verificar que haya valores numéricos
                if df_plot.dropna(how="all").shape[0] == 0:
                    st.warning("⚠️ No hi ha valors numèrics per a aquestes variables.")
                else:
                    df_plot.plot(kind="bar", figsize=(10, 6))
                    plt.title("Comparació entre sectors")
                    plt.xlabel("Sector")
                    plt.ylabel("Valor numèric")
                    plt.xticks(rotation=45)
                    st.pyplot(plt)
            else:
                st.info("Selecciona almenys una variable per mostrar el gràfic.")

else:
    st.info("⬆️ Carrega un fitxer Excel per començar.")
