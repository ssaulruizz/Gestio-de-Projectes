import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import mysql.connector
import hashlib

# ============================================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================================
st.set_page_config(
    page_title="EDV Comparator - Gestió de Projectes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS Y CONFIGURACIÓN
# ============================================================================
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .admin-badge {
        background-color: #ff9800;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.75rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SISTEMA DE AUTENTICACIÓN Y PERMISOS
# ============================================================================

# USUARIOS Y CONTRASEÑAS (EN PRODUCCIÓN, USAR BD O VARIABLES DE ENTORNO)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "usuario": {"password": "user123", "role": "user"},
    "viewer": {"password": "viewer123", "role": "viewer"}
}

def hash_password(password):
    """Hashea una contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    """Verifica credenciales del usuario"""
    if username in USERS:
        stored_password = USERS[username]["password"]
        if stored_password == password:
            return True, USERS[username]["role"]
    return False, None

def is_admin():
    """Comprueba si el usuario actual es admin"""
    return st.session_state.get("user_role") == "admin"

def is_logged_in():
    """Comprueba si el usuario está logueado"""
    return st.session_state.get("logged_in", False)

def login_page():
    """Página de login"""
    st.set_page_config(page_title="EDV Comparator - Login", page_icon="🔐", layout="centered")
    
    st.markdown('<div class="header-title">🔐 EDV Comparator - Login</div>', unsafe_allow_html=True)
    st.markdown("Sistema de Gestión de Estudios de Viabilidad")
    
    st.divider()
    
    with st.form("login_form"):
        st.subheader("Inicia Sesión")
        
        username = st.text_input("Usuario", placeholder="admin, usuario o viewer")
        password = st.text_input("Contraseña", type="password", placeholder="Introduce tu contraseña")
        
        submitted = st.form_submit_button("🔓 Iniciar Sesión", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.error("❌ Introduce usuario y contraseña")
            else:
                is_valid, role = check_credentials(username, password)
                if is_valid:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = role
                    st.success(f"✅ ¡Bienvenido {username}!")
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
    
    st.divider()
    st.info("""
    ### 🔑 Credenciales de Prueba:
    
    **Admin** (puede ver y crear registros):
    - Usuario: `admin`
    - Contraseña: `admin123`
    
    **Usuario** (solo puede ver):
    - Usuario: `usuario`
    - Contraseña: `user123`
    
    **Viewer** (solo lectura):
    - Usuario: `viewer`
    - Contraseña: `viewer123`
    """)

# ============================================================================
# CONEXIÓN A BASE DE DATOS
# ============================================================================

def get_db_connection():
    """Establece conexión con MySQL"""
    try:
        db_config = st.secrets["mysql"]
        
        connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        return connection
    except KeyError as e:
        st.error(f"❌ Error: Falta configuración en secrets.toml: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Error de conexión a BD: {e}")
        return None

@st.cache_data(ttl=300)
def load_data_from_db():
    """Carga todos los datos de la BD"""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        query = """
            SELECT 
                id, sector, codigo_actuacion, nom_actuacio, municipi, any,
                Codi_Actuacio, Tipus_actuacio, Sol_sistemes, Sol_zones, Total_ambit,
                Sol_viari, Sostre_zones, edificabilitat_bruta, Sostre_residencial,
                Nombre_dhabitatges, Hipotesis, E1__Programacio, E2__Adquisicio,
                E3__Planejament, E4__Projecte_durbanitzacio, E5__Projecte_de_reparcellacio,
                E6__Execucio_obres, E7__Comercialitzacio, E8__Compte_liquidacio_definitiva,
                E9__Tancament_darrera_venda, Incasol, Altres_propietaris, Sol_amb_drets,
                Sol_sense_drets, Titular_Adm__Act_, pct_drets_Adm__Act_, Total_Ingressos,
                Cessio_Administracio_actuant, despesa_comercialitzacio, Aprofitament_privats,
                Obres_durbanitzacio, Connexions_i_canons, Indemnitzacions, Gestio,
                Despesa_a_assumir_Adm__Act_, Despesa_total, Calcul_dinamic_Taxa_aplicada,
                Calcul_dinamic_Valor_residual_sol, Calcul_dinamic_Valor_unitari,
                Calcul_dinamic_Temps_mig_retorn, Calcul_estatic_Taxa_aplicada,
                Calcul_estatic_Valor_residual_sol, Calcul_estatic_Valor_unitari,
                Calcul_estatic_Temps_mig_retorn
            FROM edv_fitxes
            ORDER BY sector, any DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Eliminar columnas duplicadas
        df = df.loc[:, ~df.columns.duplicated()]
        
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return None

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_numeric_columns(df):
    """Obtiene las columnas numéricas"""
    return df.select_dtypes(include=[np.number]).columns.tolist()

def get_categorical_columns(df):
    """Obtiene las columnas categóricas"""
    return df.select_dtypes(include=['object']).columns.tolist()

def safe_show_dataframe(df, height=300):
    """Muestra DataFrame de forma segura"""
    try:
        st.dataframe(df, use_container_width=True, height=height)
    except Exception as e:
        st.warning(f"Error mostrando tabla: {e}")
        st.write(df)

def insert_new_record(data):
    """Inserta un nuevo registro en la BD"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return False, "❌ No se pudo conectar a la BD"
        
        cursor = conn.cursor()
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())
        
        query = f"INSERT INTO edv_fitxes ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "✅ Registro insertado correctamente"
    except Exception as e:
        if conn:
            conn.close()
        return False, f"❌ Error al insertar: {str(e)}"

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

# Inicializar estado de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Si no está logueado, mostrar página de login
if not is_logged_in():
    login_page()
    st.stop()

# ============================================================================
# INTERFAZ PRINCIPAL (USUARIO LOGUEADO)
# ============================================================================

st.markdown('<div class="header-title">📊 Comparador d\'EDV - Estudis de Viabilitat</div>', unsafe_allow_html=True)
st.markdown("Eina de comparació de **Estudis de Viabilitat (EDV)** de sectors urbanístics a Catalunya")

# Sidebar con info del usuario
with st.sidebar:
    st.divider()
    
    # Mostrar usuario actual
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text(f"👤 Usuario: **{st.session_state.username}**")
    with col2:
        if is_admin():
            st.markdown('<span class="admin-badge">ADMIN</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="admin-badge" style="background-color: #2196F3;">USER</span>', unsafe_allow_html=True)
    
    st.divider()
    
    # Botón cerrar sesión
    if st.button("🔓 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.rerun()

# Cargar datos
df = load_data_from_db()

if df is None or df.empty:
    st.error("❌ No s'han pogut caregar les dades de la base de dades")
else:
    # ========================================================================
    # SIDEBAR - CONFIGURACIÓ
    # ========================================================================
    with st.sidebar:
        st.header("⚙️ Paràmetres")
        
        # Opciones según rol
        if is_admin():
            view_options = ["🏠 Visió General", "📈 Comparar Sectors", "🔍 Análisi Individual", "📊 Estadístics", "📥 Exportar", "➕ Afegir Registre"]
        else:
            view_options = ["🏠 Visió General", "📈 Comparar Sectors", "🔍 Análisi Individual", "📊 Estadístics", "📥 Exportar"]
        
        view_mode = st.radio(
            "Mode de visualització:",
            view_options
        )
        
        st.divider()
        
        # Filtres comuns (no en modo "Afegir Registre")
        if view_mode != "➕ Afegir Registre":
            st.subheader("Filtres")
            
            all_sectors = sorted(df['sector'].unique().tolist())
            selected_sectors = st.multiselect(
                "Selecciona sectors:",
                all_sectors,
                default=all_sectors[:3] if len(all_sectors) >= 3 else all_sectors
            )
            
            all_years = sorted(df['any'].unique().tolist())
            selected_years = st.multiselect(
                "Selecciona anys:",
                all_years,
                default=all_years
            )
            
            df_filtered = df[
                (df['sector'].isin(selected_sectors)) &
                (df['any'].isin(selected_years))
            ].copy()
            
            st.info(f"📍 Registres seleccionats: **{len(df_filtered)}**")
    
    # ========================================================================
    # MODE 1: VISIÓ GENERAL
    # ========================================================================
    if view_mode == "🏠 Visió General":
        st.subheader("Visió General de Sectors")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sectors", df_filtered['sector'].nunique(), "✓")
        
        with col2:
            st.metric("Total Registres", len(df_filtered), "registres")
        
        with col3:
            st.metric("Anys Coberts", df_filtered['any'].nunique(), "anys")
        
        with col4:
            st.metric("Municipis", df_filtered['municipi'].nunique(), "municipis")
        
        st.divider()
        
        st.subheader("Dades per Sector")
        
        summary_table = df_filtered.groupby('sector').agg({
            'codigo_actuacion': 'count',
            'any': ['min', 'max'],
            'Total_Ingressos': 'mean',
            'Despesa_total': 'mean'
        }).round(2)
        
        summary_table.columns = ['Registres', 'Any Min', 'Any Max', 'Ingressos Mitjans', 'Despesa Mitjana']
        safe_show_dataframe(summary_table)
    
    # ========================================================================
    # MODE 2: COMPARAR SECTORS
    # ========================================================================
    elif view_mode == "📈 Comparar Sectors":
        st.subheader("Comparació entre Sectors")
        
        numeric_cols = get_numeric_columns(df_filtered)
        numeric_cols = [col for col in numeric_cols if col not in ['id', 'any']]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_vars = st.multiselect(
                "Selecciona variables per comparar:",
                numeric_cols,
                default=numeric_cols[:5] if len(numeric_cols) >= 5 else numeric_cols
            )
        
        with col2:
            chart_type = st.selectbox(
                "Tipus de gràfic:",
                ["Barres", "Línies", "Caixa", "Radar"]
            )
        
        if selected_vars and len(df_filtered) > 0:
            agg_data = df_filtered.groupby('sector')[selected_vars].mean().round(2)
            
            if chart_type == "Barres":
                fig = px.bar(agg_data.reset_index(), x='sector', y=selected_vars,
                            title="Comparació de Variables per Sector", barmode='group',
                            labels={'value': 'Valor', 'sector': 'Sector'})
            elif chart_type == "Línies":
                df_long = agg_data.reset_index().melt(id_vars='sector', var_name='Variable', value_name='Valor')
                fig = px.line(df_long, x='sector', y='Valor', color='Variable',
                             title="Evolució de Variables per Sector", markers=True)
            elif chart_type == "Caixa":
                df_plot = df_filtered[['sector'] + selected_vars].copy()
                df_long = df_plot.melt(id_vars='sector', value_vars=selected_vars, var_name='Variable', value_name='Valor')
                fig = px.box(df_long, x='Variable', y='Valor', color='sector',
                            title="Distribució de Variables per Sector")
            elif chart_type == "Radar":
                fig = go.Figure()
                for sector in agg_data.index:
                    fig.add_trace(go.Scatterpolar(r=agg_data.loc[sector].values, theta=selected_vars,
                                                   fill='toself', name=sector))
                fig.update_layout(title="Comparació Radar de Sectors")
            
            st.plotly_chart(fig, use_container_width=True)
            
            if st.checkbox("Mostrar taula de dades"):
                safe_show_dataframe(agg_data)
        else:
            st.warning("Selecciona almenys una variable")
    
    # ========================================================================
    # MODE 3: ANÁLISI INDIVIDUAL
    # ========================================================================
    elif view_mode == "🔍 Análisi Individual":
        st.subheader("Análisi Detallada per Sector")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_sector = st.selectbox("Selecciona un sector:", sorted(df_filtered['sector'].unique()))
        
        with col2:
            metric_type = st.selectbox("Estadístics:", ["Mitjana", "Màxim", "Mínim"])
        
        sector_data = df_filtered[df_filtered['sector'] == selected_sector].copy()
        
        if not sector_data.empty:
            st.subheader(f"Informació del Sector: {selected_sector}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Registres", len(sector_data))
            with col2:
                st.metric("Anys", sector_data['any'].min(), f"a {sector_data['any'].max()}")
            with col3:
                st.metric("Municipis", sector_data['municipi'].unique()[0] if len(sector_data) > 0 else "-")
            
            st.divider()
            
            st.subheader("Evolució Temporal")
            
            numeric_cols = get_numeric_columns(sector_data)
            numeric_cols = [col for col in numeric_cols if col != 'id']
            
            temporal_df = sector_data[['any', 'Hipotesis'] + numeric_cols].copy()
            temporal_df = temporal_df.reset_index(drop=True)
            temporal_df = temporal_df.loc[:, ~temporal_df.columns.duplicated()]
            
            if 'any' in temporal_df.columns:
                temporal_df = temporal_df.sort_values('any', ascending=False)
            
            safe_show_dataframe(temporal_df)
            
            st.subheader("Gràfic d'Evolució")
            
            key_metrics = ['Total_Ingressos', 'Despesa_total', 'Aprofitament_privats', 'Obres_durbanitzacio']
            available_metrics = [m for m in key_metrics if m in sector_data.columns]
            
            if available_metrics:
                fig = px.line(sector_data.sort_values('any'), x='any', y=available_metrics,
                             title=f"Evolució de Métriques - {selected_sector}", markers=True,
                             labels={'value': 'Valor', 'any': 'Any', 'variable': 'Variable'})
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hi ha dades per aquest sector")
    
    # ========================================================================
    # MODE 4: ESTADÍSTICS
    # ========================================================================
    elif view_mode == "📊 Estadístics":
        st.subheader("Análisi Estadística")
        
        tab1, tab2, tab3 = st.tabs(["Resum", "Correlacions", "Distribucions"])
        
        with tab1:
            st.subheader("Estadístics Descriptius")
            numeric_data = df_filtered[get_numeric_columns(df_filtered)].drop('id', axis=1)
            numeric_data = numeric_data.loc[:, ~numeric_data.columns.duplicated()]
            
            col1, col2 = st.columns([1, 2])
            with col1:
                stat_type = st.selectbox("Estadístic:", ["describe", "mean", "std", "min", "max"])
            with col2:
                st.info("Estadístics de les variables numèriques seleccionades")
            
            if stat_type == "describe":
                stats_df = numeric_data.describe().round(2)
            else:
                stats_df = getattr(numeric_data, stat_type)().round(2).to_frame(name='Valor')
            
            safe_show_dataframe(stats_df)
        
        with tab2:
            st.subheader("Matriu de Correlacions")
            numeric_data = df_filtered[get_numeric_columns(df_filtered)].drop('id', axis=1)
            numeric_data = numeric_data.loc[:, ~numeric_data.columns.duplicated()]
            
            corr_vars = st.multiselect("Selecciona variables:", numeric_data.columns.tolist(),
                                      default=numeric_data.columns.tolist()[:10])
            
            if corr_vars:
                corr_matrix = numeric_data[corr_vars].corr()
                fig = px.imshow(corr_matrix, title="Correlacions entre Variables",
                               labels=dict(color="Correlació"), color_continuous_scale='RdBu', zmin=-1, zmax=1)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Distribucions de Variables")
            selected_var = st.selectbox("Selecciona una variable:", get_numeric_columns(df_filtered))
            
            if selected_var != 'id':
                fig = px.histogram(df_filtered, x=selected_var, color='sector', nbins=30,
                                  title=f"Distribució de {selected_var}", barmode='overlay')
                st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # MODE 5: EXPORTAR
    # ========================================================================
    elif view_mode == "📥 Exportar":
        st.subheader("Exportar Dades")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            export_format = st.selectbox("Format:", ["CSV", "Excel"])
        
        with col2:
            include_sectors = st.multiselect("Sectors a exportar:", sorted(df_filtered['sector'].unique()),
                                            default=sorted(df_filtered['sector'].unique()))
        
        export_data = df_filtered[df_filtered['sector'].isin(include_sectors)]
        
        if not export_data.empty:
            if export_format == "CSV":
                csv = export_data.to_csv(index=False)
                st.download_button(label="📥 Descarregar CSV", data=csv,
                                  file_name=f"edv_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                  mime="text/csv")
            
            elif export_format == "Excel":
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    export_data.to_excel(writer, index=False, sheet_name='EDV Data')
                buffer.seek(0)
                st.download_button(label="📥 Descarregar Excel", data=buffer.getvalue(),
                                  file_name=f"edv_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                  mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
            st.info(f"Registres a exportar: **{len(export_data)}**")
        else:
            st.warning("No hi ha dades per exportar amb els filtres actuals")
    
    # ========================================================================
    # MODE 6: AFEGIR REGISTRE (SOLO ADMINS)
    # ========================================================================
    elif view_mode == "➕ Afegir Registre":
        if not is_admin():
            st.error("❌ Solo los administradores pueden agregar registros")
            st.info(f"Tu rol actual es: **{st.session_state.user_role}**")
        else:
            st.subheader("➕ Afegir Nou Registre EDV")
            st.info("📝 Solo administradores pueden crear nuevos registros")
            
            with st.form("form_afegir_registre"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    sector = st.selectbox("Sector *", [""] + sorted(df['sector'].unique()))
                    codigo_actuacion = st.text_input("Código Actuación *")
                    nom_actuacio = st.text_input("Nom Actuació *")
                
                with col2:
                    municipi = st.text_input("Municipi *")
                    any = st.number_input("Any *", min_value=2000, max_value=2050, value=datetime.now().year)
                    codi_actuacio = st.text_input("Codi Actuació")
                
                with col3:
                    tipus_actuacio = st.selectbox("Tipus Actuació", ["", "Residencial", "Comercial", "Industrial", "Mixta", "Altres"])
                    hipotesis = st.selectbox("Hipòtesis", ["", "Per adquisició", "Per Planejament", "Per a PR", "Per a obres", "Altres"])
                    titular = st.selectbox("Titular Adm. Act.", ["", "Incasòl", "Consorci", "Altres"])
                
                st.subheader("📐 Dades Físiques")
                fcol1, fcol2, fcol3, fcol4 = st.columns(4)
                
                with fcol1:
                    sol_sistemes = st.number_input("Sòl Sistemes", value=0.0, format="%.2f")
                    sol_zones = st.number_input("Sòl Zones", value=0.0, format="%.2f")
                
                with fcol2:
                    total_ambit = st.number_input("Total Àmbit", value=0.0, format="%.2f")
                    sol_viari = st.number_input("Sòl Viari", value=0.0, format="%.2f")
                
                with fcol3:
                    sostre_zones = st.number_input("Sostre Zones", value=0.0, format="%.2f")
                    edificabilitat = st.number_input("Edificabilitat Bruta", value=0.0, format="%.2f")
                
                with fcol4:
                    sostre_residencial = st.number_input("Sostre Residencial", value=0.0, format="%.2f")
                    habitatges = st.number_input("Nombre Habitatges", value=0, step=1)
                
                st.subheader("💰 Dades Econòmiques")
                ecol1, ecol2, ecol3 = st.columns(3)
                
                with ecol1:
                    total_ingressos = st.number_input("Total Ingressos", value=0.0, format="%.2f")
                    cessio = st.number_input("Cessió Administració", value=0.0, format="%.2f")
                    despesa_comercial = st.number_input("Despesa Comercialització", value=0.0, format="%.2f")
                
                with ecol2:
                    aprofitament = st.number_input("Aprofitament Privats", value=0.0, format="%.2f")
                    obres = st.number_input("Obres d'Urbanització", value=0.0, format="%.2f")
                    connexions = st.number_input("Connexions i Cànons", value=0.0, format="%.2f")
                
                with ecol3:
                    indemnitzacions = st.number_input("Indemnitzacions", value=0.0, format="%.2f")
                    gestio = st.number_input("Gestió", value=0.0, format="%.2f")
                    despesa_total = st.number_input("Despesa Total", value=0.0, format="%.2f")
                
                submitted = st.form_submit_button("✅ Afegir Registre", use_container_width=True)
                
                if submitted:
                    errors = []
                    if not sector or sector == "":
                        errors.append("• Sector és obligatori")
                    if not codigo_actuacion or codigo_actuacion.strip() == "":
                        errors.append("• Código Actuación és obligatori")
                    if not nom_actuacio or nom_actuacio.strip() == "":
                        errors.append("• Nom Actuació és obligatori")
                    if not municipi or municipi.strip() == "":
                        errors.append("• Municipi és obligatori")
                    if not hipotesis or hipotesis == "":
                        errors.append("• Hipòtesis és obligatori")
                    if not titular or titular == "":
                        errors.append("• Titular Adm. Act. és obligatori")
                    
                    if errors:
                        st.error("❌ Falten camps obligatoris:\n" + "\n".join(errors))
                    else:
                        new_record = {
                            'sector': sector,
                            'codigo_actuacion': codigo_actuacion.strip(),
                            'nom_actuacio': nom_actuacio.strip(),
                            'municipi': municipi.strip(),
                            'any': int(any),
                            'Codi_Actuacio': codi_actuacio.strip(),
                            'Tipus_actuacio': tipus_actuacio if tipus_actuacio else None,
                            'Sol_sistemes': sol_sistemes,
                            'Sol_zones': sol_zones,
                            'Total_ambit': total_ambit,
                            'Sol_viari': sol_viari,
                            'Sostre_zones': sostre_zones,
                            'edificabilitat_bruta': edificabilitat,
                            'Sostre_residencial': sostre_residencial,
                            'Nombre_dhabitatges': int(habitatges),
                            'Hipotesis': hipotesis if hipotesis else None,
                            'Titular_Adm__Act_': titular if titular else None,
                            'Total_Ingressos': total_ingressos,
                            'Cessio_Administracio_actuant': cessio,
                            'despesa_comercialitzacio': despesa_comercial,
                            'Aprofitament_privats': aprofitament,
                            'Obres_durbanitzacio': obres,
                            'Connexions_i_canons': connexions,
                            'Indemnitzacions': indemnitzacions,
                            'Gestio': gestio,
                            'Despesa_total': despesa_total
                        }
                        
                        success, message = insert_new_record(new_record)
                        if success:
                            st.success(message)
                            st.cache_data.clear()
                            st.balloons()
                            st.info("📱 Actualiza la app para ver el nuevo registre")
                        else:
                            st.error(message)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.divider()
    st.caption("💾 Font: Base de dades EDV | 🗄️ Última actualització: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
