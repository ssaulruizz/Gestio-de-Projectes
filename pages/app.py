# App_full_fixed.py
import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
from io import BytesIO
import json

# Plotly (opcional)
try:
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False

st.set_page_config(page_title="EDV Comparator (All features)", layout="wide")
st.title("📊 EDV Comparator — Full features")

# -------------------------
# Utilities
# -------------------------
def safe_show(df, height=300):
    """Mostrar DataFrame evitando errores de pyarrow: forzar string si falla."""
    try:
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.dataframe(df.astype(str), use_container_width=True)

def read_excel_safe(uploaded_file):
    """Intenta leer un excel con pandas y devuelve df_raw; capta error de openpyxl."""
    try:
        return pd.read_excel(uploaded_file, header=None)
    except Exception as e:
        st.error(f"Error reading Excel: {e}")
        st.info("Asegúrate de tener instalado: openpyxl (`pip install openpyxl`) y pandas actualizado.")
        return None

def parse_sheet_structure(df_raw):
    idxs = df_raw[df_raw.iloc[:, 2].astype(str).str.contains("Informació sector", case=False, na=False)].index
    if len(idxs) == 0:
        return None, None, None
    start_row = idxs[0] + 1

    raw_vars = df_raw.iloc[start_row:, 3]
    variables = raw_vars.dropna().astype(str)
    variables = variables[variables.str.strip() != ""]

    sector_names_raw = df_raw.iloc[start_row - 1, 4:].dropna().astype(str).tolist()
    counts = Counter()
    unique_sector_names = []
    for s in sector_names_raw:
        counts[s] += 1
        unique_sector_names.append(f"{s}_{counts[s]}" if counts[s] > 1 else s)

    df_data = df_raw.iloc[variables.index, 4:4 + len(unique_sector_names)].copy()
    df_data.columns = unique_sector_names
    df_data.index = variables.values
    df_data.index.name = "Variable"
    return df_data, unique_sector_names, start_row

def clean_value(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, str):
        x = x.replace("m²s", "").replace("m²st", "").replace("m²", "") \
             .replace("%", "").replace(" ", "").replace("‐", "-").strip()
        x = x.replace(",", ".")
        try:
            return float(x)
        except Exception:
            return np.nan
    try:
        return float(x)
    except Exception:
        return np.nan

def df_to_excel_bytes(df):
    towrite = BytesIO()
    with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
        df.to_excel(writer, index=True, sheet_name="data")
    towrite.seek(0)
    return towrite.getvalue()

def fig_to_png_bytes(fig):
    if not PLOTLY_AVAILABLE:
        return None
    try:
        return pio.to_image(fig, format="png")
    except Exception:
        return None

# -------------------------
# Session state
# -------------------------
if "presets" not in st.session_state:
    st.session_state.presets = {}

# -------------------------
# File upload
# -------------------------
uploaded_file = st.file_uploader("Upload Excel (.xlsx) with 'Informació sector' in column C", type=["xlsx"])

if uploaded_file:
    df_raw = read_excel_safe(uploaded_file)
    if df_raw is None:
        st.stop()

    df_data, sector_names, start_row = parse_sheet_structure(df_raw)
    if df_data is None:
        st.error("Could not find 'Informació sector' in column C. Check file structure.")
        st.stop()

    # --- Convertir y limpiar numéricos ---
    df_numeric = df_data.apply(lambda col: col.map(clean_value))
    # Forzar todas las columnas a string antes de mostrarlas para evitar error de pyarrow
    df_data = df_data.astype(str)

    st.success("File loaded and parsed successfully.")
    st.subheader("Preview: extracted variables & sectors (first 10 rows)")
    safe_show(df_data.head(10))

    # -------------------------
    # Sidebar: modes
    # -------------------------
    st.sidebar.header("View / Mode")
    mode = st.sidebar.radio("Choose view:", ["Compare EDVs", "Single EDV", "Statistics", "Export", "Presets"])
    all_variables = df_data.index.tolist()
    all_sectors = df_data.columns.tolist()

    # -------------------------
    # MODE: Compare EDVs
    # -------------------------
    if mode == "Compare EDVs":
        st.subheader("Compare multiple EDVs")
        with st.sidebar.expander("Comparison options", expanded=True):
            selected_sectors = st.multiselect("Select EDVs (sectors) to compare", all_sectors, default=all_sectors[:3])
            selected_vars = st.multiselect("Select variables", all_variables, default=all_variables[:6] if len(all_variables) >= 6 else all_variables)
            chart_type = st.selectbox("Chart type", ["Bar (grouped)", "Bar (stacked)", "Line", "Scatter", "Boxplot", "Radar"])
            normalize = st.checkbox("Normalize variables (0-1) per variable", value=False)
            show_table = st.checkbox("Show underlying numeric table", value=False)

        if not selected_sectors or not selected_vars:
            st.info("Choose at least one EDV and one variable.")
        else:
            df_plot = df_numeric.loc[selected_vars, selected_sectors]
            
            if df_plot.dropna(how="all").shape[0] == 0:
                st.warning("No numeric values available for the selection.")
            else:
                # Preparar datos para Plotly de forma correcta
                plot_df = df_plot.copy()
                if normalize:
                    plot_df = (plot_df - plot_df.min()) / (plot_df.max() - plot_df.min())

                if not PLOTLY_AVAILABLE:
                    st.warning("Plotly not installed. Showing table instead.")
                    safe_show(plot_df.T)  # Transponer para mejor visualización en tabla
                else:
                    # Crear DataFrame largo (tidy) para Plotly
                    df_long = plot_df.reset_index().melt(
                        id_vars=['Variable'], 
                        value_vars=selected_sectors,
                        var_name='Sector', 
                        value_name='Value'
                    )
                    
                    if chart_type.startswith("Bar"):
                        barmode = "group" if "grouped" in chart_type.lower() else "stack"
                        fig = px.bar(
                            df_long, 
                            x='Variable', 
                            y='Value', 
                            color='Sector',
                            barmode=barmode,
                            title="Comparison: Variables across EDVs",
                            labels={"Value": "Value", "Variable": "Variable"}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                    elif chart_type == "Line":
                        fig = px.line(
                            df_long, 
                            x='Variable', 
                            y='Value', 
                            color='Sector',
                            markers=True,
                            title="Line chart: Variables across EDVs",
                            labels={"Value": "Value", "Variable": "Variable"}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                    elif chart_type == "Scatter":
                        cols_for_scatter = selected_vars[:6] if len(selected_vars) > 6 else selected_vars
                        # Para scatter matrix, necesitamos los datos en formato ancho por sector
                        scatter_df = df_numeric.loc[cols_for_scatter, selected_sectors].T
                        fig = px.scatter_matrix(
                            scatter_df,
                            dimensions=cols_for_scatter, 
                            title="Scatter matrix by EDV"
                        )
                        fig.update_traces(diagonal_visible=False)
                        st.plotly_chart(fig, use_container_width=True)
                        
                    elif chart_type == "Boxplot":
                        fig = px.box(
                            df_long, 
                            x='Variable', 
                            y='Value', 
                            color='Sector',
                            title="Boxplot per variable across EDVs"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                    elif chart_type == "Radar":
                        fig = go.Figure()
                        for sector in selected_sectors:
                            sector_data = plot_df[sector].fillna(0)
                            fig.add_trace(go.Scatterpolar(
                                r=sector_data.values, 
                                theta=plot_df.index.tolist(), 
                                fill='toself', 
                                name=sector
                            ))
                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True)),
                            title="Radar chart: Variables comparison"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                if show_table:
                    st.markdown("### Numeric values used for the chart")
                    safe_show(plot_df)  
    # -------------------------
    # MODE: Single EDV
    # -------------------------
    elif mode == "Single EDV":
        st.subheader("Single EDV (detailed) view")
        with st.sidebar.expander("Single EDV options", expanded=True):
            selected_sector = st.selectbox("Choose EDV / Sector", all_sectors)
            top_n = st.number_input("Show top N variables by value (0 to show all)", min_value=0, max_value=len(all_variables), value=0)
            show_raw = st.checkbox("Show raw (string) table", value=False)
            chart_types = st.multiselect("Charts to show", ["Bar", "Line", "Radar", "Histogram"], default=["Bar", "Radar"])

        if selected_sector:
            df_single_raw = df_data[selected_sector]
            df_single_num = df_numeric[selected_sector].dropna()

            st.markdown(f"## {selected_sector}")
            
            cols = st.columns((1, 1))
                    
            with cols[0]:
                st.markdown("### Summary statistics")
                if df_single_num.empty:
                    st.warning("No numeric values available for this EDV.")
                else:
                    # Crear estadísticas de forma segura
                    try:
                        stats = df_single_num.describe().round(3)
                        stats_df = stats.to_frame(name="Value")
                        safe_show(stats_df)
                    except Exception as e:
                        st.error(f"Error calculating statistics: {e}")
                        st.info("Showing basic info instead")
                        st.write(f"Total variables: {len(df_single_num)}")
                        st.write(f"Non-null values: {df_single_num.count()}")
                        
            if top_n > 0 and not df_single_num.empty:
                st.markdown(f"### Top {top_n} variables by value")
                try:
                    top_df = df_single_num.sort_values(ascending=False).head(top_n).to_frame("Value")
                    top_df = top_df.fillna('N/A')
                    safe_show(top_df)
                except Exception as e:
                    st.error(f"Error displaying top variables: {e}")

            # GRÁFICOS - con manejo robusto de errores
            if PLOTLY_AVAILABLE and not df_single_num.empty:
                for ct in chart_types:
                    try:
                        if ct == "Bar":
                            # Preparar datos para bar chart
                            plot_data = df_single_num.sort_values(ascending=False)
                            # Limitar a los primeros 20 para mejor visualización
                            if len(plot_data) > 20:
                                plot_data = plot_data.head(20)
                                st.info(f"Showing top 20 of {len(df_single_num)} variables")
                                
                            fig = px.bar(
                                x=plot_data.index, 
                                y=plot_data.values,
                                title=f"{selected_sector} - Bar Chart",
                                labels={'x': 'Variable', 'y': 'Value'}
                            )
                            fig.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig, use_container_width=True)
                            
                        elif ct == "Line":
                            # Para line chart, usar valores ordenados por índice
                            plot_data = df_single_num.sort_index()
                            fig = px.line(
                                x=range(len(plot_data)), 
                                y=plot_data.values,
                                title=f"{selected_sector} - Line Chart",
                                labels={'x': 'Variable Index', 'y': 'Value'},
                                markers=True
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                        elif ct == "Radar":
                            vars_for_radar = df_single_num.index.tolist()
                            if len(vars_for_radar) < 3:
                                st.info("Radar chart needs at least 3 variables.")
                            else:
                                # Limitar a 10 variables para radar legible
                                if len(vars_for_radar) > 10:
                                    vars_for_radar = vars_for_radar[:10]
                                    st.info("Showing first 10 variables for radar chart")
                                    
                                fig = go.Figure()
                                fig.add_trace(go.Scatterpolar(
                                    r=df_single_num.loc[vars_for_radar].fillna(0).values, 
                                    theta=vars_for_radar, 
                                    fill="toself", 
                                    name=selected_sector
                                ))
                                fig.update_layout(
                                    title=f"{selected_sector} - Radar Chart", 
                                    polar=dict(radialaxis=dict(visible=True))
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                
                        elif ct == "Histogram":
                            # Filtrar valores infinitos o extremos
                            hist_data = df_single_num.replace([np.inf, -np.inf], np.nan).dropna()
                            if not hist_data.empty:
                                fig = px.histogram(
                                    x=hist_data.values, 
                                    nbins=20, 
                                    title=f"{selected_sector} - Value Distribution"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning("No valid data for histogram")
                                
                    except Exception as e:
                        st.error(f"Error creating {ct} chart: {str(e)}")
                        st.info("Try selecting different variables or check data quality")
                        
            elif not PLOTLY_AVAILABLE and not df_single_num.empty:
                st.info("Install plotly to view interactive charts (`pip install plotly`).")
    # -------------------------
    # MODE: Statistics
    # -------------------------
    elif mode == "Statistics":
        st.subheader("Statistics & Correlations")
        with st.sidebar.expander("Stats options", expanded=True):
            corr_method = st.selectbox("Correlation method", ["pearson", "kendall", "spearman"])
            show_heatmap = st.checkbox("Show correlation heatmap", value=True)
            show_describe = st.checkbox("Show describe() tables", value=True)

        if show_describe:
            st.markdown("### Mean per EDV")
            safe_show(df_numeric.mean().round(3).to_frame("mean"))
            st.markdown("### Mean per variable (top 30)")
            safe_show(df_numeric.mean(axis=1).round(3).sort_values(ascending=False).head(30).to_frame("mean"))

        if show_heatmap and PLOTLY_AVAILABLE:
            corr_df = df_numeric.corr(method=corr_method)
            st.markdown("### Correlation heatmap between EDVs")
            fig = px.imshow(corr_df, text_auto=True, aspect="auto", title=f"Correlation ({corr_method})")
            st.plotly_chart(fig, use_container_width=True)
        elif show_heatmap:
            st.info("Install plotly to view heatmap.")

    # -------------------------
    # MODE: Export
    # -------------------------
    elif mode == "Export":
        st.subheader("Export data and charts")
        with st.sidebar.expander("Export options", expanded=True):
            export_scope = st.selectbox("Export scope", ["All numeric data", "Selected EDVs/Vars (custom)"])
            if export_scope == "Selected EDVs/Vars (custom)":
                exp_sectors = st.multiselect("Select EDVs to export", all_sectors, default=all_sectors[:3])
                exp_vars = st.multiselect("Select variables to export", all_variables, default=all_variables[:10] if len(all_variables) >= 10 else all_variables)
            else:
                exp_sectors = all_sectors
                exp_vars = all_variables
            create_excel = st.checkbox("Create Excel file", value=True)
            chart_for_export = st.selectbox("Create PNG from chart", ["None", "Comparison Bar (first 10 vars)", "Single EDV Bar"])
            png_sector = None
            if chart_for_export == "Single EDV Bar":
                png_sector = st.selectbox("Choose EDV for PNG", all_sectors)

        export_df = df_numeric.loc[exp_vars, exp_sectors]
        if create_excel:
            try:
                excel_bytes = df_to_excel_bytes(export_df)
                st.download_button("Download Excel (.xlsx)", data=excel_bytes, file_name="edv_export.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            except Exception as e:
                st.error(f"Error creating Excel: {e}. Ensure openpyxl is installed.")

        if chart_for_export != "None" and PLOTLY_AVAILABLE:
            fig = None
            if chart_for_export == "Comparison Bar (first 10 vars)":
                vars_to_plot = exp_vars[:10] if len(exp_vars) > 0 else all_variables[:10]
                sectors_to_plot = exp_sectors[:8] if len(exp_sectors) > 0 else all_sectors[:8]
                df_plot = df_numeric.loc[vars_to_plot, sectors_to_plot].T
                fig = px.bar(df_plot, barmode="group", title="Export Chart: Comparison")
            elif chart_for_export == "Single EDV Bar" and png_sector:
                df_single = df_numeric[png_sector].dropna()
                fig = px.bar(df_single.sort_values(ascending=False), title=f"{png_sector} - Bar")
            if fig is not None:
                png_bytes = fig_to_png_bytes(fig)
                if png_bytes:
                    st.download_button("Download chart PNG", data=png_bytes, file_name="chart.png", mime="image/png")
                else:
                    st.warning("Automatic PNG generation failed. Install 'kaleido' for export.")

    # -------------------------
    # MODE: Presets
    # -------------------------
    elif mode == "Presets":
        st.subheader("Presets — save/load your selections")
        st.markdown("### Save a new preset")
        preset_name = st.text_input("Preset name")
        if st.button("Save current selection as preset") and preset_name.strip() != "":
            preset = {
                "variables": st.session_state.get("selected_vars", []),
                "sectors": st.session_state.get("selected_sectors", []),
                "mode": mode
            }
            st.session_state.presets[preset_name] = preset
            st.success(f"Preset '{preset_name}' saved.")

        st.markdown("### Manage presets")
        if st.session_state.presets:
            for name, data in st.session_state.presets.items():
                col1, col2, col3 = st.columns([3,1,1])
                col1.write(f"**{name}** — {json.dumps(data)}")
                if col2.button("Load", key=f"load_{name}"):
                    st.info(f"Loading preset '{name}' (session only).")
                if col3.button("Delete", key=f"del_{name}"):
                    del st.session_state.presets[name]
                    st.rerun()
            presets_json = json.dumps(st.session_state.presets, indent=2)
            st.download_button("Download presets JSON", data=presets_json.encode("utf-8"), file_name="edv_presets.json", mime="application/json")
        else:
            st.info("No presets saved yet.")

else:
    st.info("Upload an Excel file to start. Must contain 'Informació sector' in column C.")