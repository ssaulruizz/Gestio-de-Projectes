# 📊 EDV Comparator - Estudis de Viabilitat

## 🎯 Què és aquesta aplicació?

**EDV Comparator** és una eina de gestió i comparació d'Estudis de Viabilitat (EDV) de sectors urbanístics a Catalunya. Permet visualitzar, analitzar i gestionar dades de projectes urbanístics amb un sistema de seguretat basat en rols d'usuari.

---

## 🔐 Sistema de Login i Permisos

### Credencials de Prova

L'aplicació requereix login obligatori. Hi ha tres tipus d'usuaris amb permisos diferents:

**👤 Admin** (Administrador - Máxim permisos)
- Usuari: `admin`
- Contrasenya: `admin123`
- Permisos: 
  - Ver todos los datos
  - Crear nuevos registros
  - Exportar datos
  - Acceso a todas las secciones

**👥 Usuario** (Usuari Regular - Permisos limitados)
- Usuari: `usuario`
- Contrasenya: `user123`
- Permisos:
  - Ver todos los datos
  - NO puede crear registros
  - Exportar datos
  - NO ve la sección "➕ Afegir Registre"

**📖 Viewer** (Visualitzador - Solo lectura)
- Usuari: `viewer`
- Contrasenya: `viewer123`
- Permisos:
  - Ver todos los datos
  - NO puede crear registros
  - Exportar datos
  - NO ve la sección "➕ Afegir Registre"

### Per canviar d'usuari

1. Clica el botó **🔓 Cerrar Sesión** a la barra lateral
2. Introdueix les credencials del nou usuari
3. Clica **🔓 Iniciar Sesión**

---

## 📱 Interfície Principal

### Barra Superior
- **Logo i títol**: EDV Comparator - Estudis de Viabilitat
- **Descripció**: Eina de comparació de sectors urbanístics a Catalunya

### Barra Lateral (Sidebar)
Conté els controls principals:

**Informació de l'usuari**
- Mostra l'usuari actual connectat
- Badge indicant el rol (ADMIN, USER)

**Mode de visualització**
- Selecciona quin tipus de vista vols veure
- Els admins veuen totes les opcions
- Els usuaris normals NO veuen "➕ Afegir Registre"

**Filtres**
- **Selecciona sectors**: Tria quins sectors vols analitzar
- **Selecciona anys**: Tria quins anys vols visualitzar
- **Mostrador de registres**: Mostra quants registres coincideixen amb els filtres

---

## 📊 Secciones Disponibles

### 1️⃣ 🏠 Visió General

**Descripció**: Mostra un resum ràpid de tots els dades carregades.

**Que mostra:**
- **Total Sectors**: Nombre de sectors seleccionats
- **Total Registres**: Nombre de registres (projectes) carregats
- **Anys Coberts**: Range de anys disponibles
- **Municipis**: Nombre de municipis representats

**Taula resumida**
Mostra per cada sector:
- Nombre de registres
- Any mínim i màxim
- Ingressos mitjans
- Despesa mitjana

**Ús**: Per tenir una visió ràpida del projecte i verificar que els filtres funcionen correctament.

---

### 2️⃣ 📈 Comparar Sectors

**Descripció**: Compara múltiples variables entre sectors amb gràfics interactius.

**Com funciona:**
1. **Selecciona variables per comparar**: Tria quines mètriques vols comparar (Total Ingressos, Despesa, etc.)
2. **Selecciona tipus de gràfic**:
   - **Barres**: Comparació directa en barres agrupades
   - **Línies**: Evolució de variables per sector
   - **Caixa**: Distribució de dades (quartils, outliers)
   - **Radar**: Representació radial (perfect per comparar múltiples variables)

3. **Veure taula de dades**: Marca la casella per veure els números exactes

**Ús**: 
- Identificar tendències entre sectors
- Veure quins sectors són més competitius
- Analitzar patrons econòmics

---

### 3️⃣ 🔍 Análisi Individual

**Descripció**: Mostra un análisis detallat d'un sector specific.

**Com funciona:**
1. **Selecciona un sector** de la llista desplegable
2. **Veure mètriques clau**:
   - Nombre de registres en aquest sector
   - Anys que cobreix (de X a Y)
   - Municipis involved

3. **Taula de temporalitat**: 
   - Mostra l'evolució temporal ordenada per anys
   - Inclou la hipòtesis de cada registre
   - Totes les variables numèriques

4. **Gràfic d'evolució**:
   - Linies temporal de:
     - Total Ingressos
     - Despesa Total
     - Aprofitament Privats
     - Obres d'Urbanització

**Ús**:
- Analitzar en profunditat un sector specific
- Veure tendències temporals
- Entendre l'evolució econòmica

---

### 4️⃣ 📊 Estadístics

**Descripció**: Análisis estadístic avançat de les dades.

**Tres pestanyes:**

**Resum**
- Estadístics descriptius generals:
  - Describe: Resumen estadístico completo (count, mean, std, min, max, quartiles)
  - Mean: Valor promedio
  - Std: Desviación estándar
  - Min: Valor mínimo
  - Max: Valor máximo

**Correlacions**
- Matriu de correlació entre variables
- Identifica relacions positives i negatives
- Visualització amb mapa de calor (rojo/blau)
- Selecciona quines variables vols correlacionar

**Distribucions**
- Histograma de cualquier variable
- Dividit per sectors
- Mostra la distribució de freqüències
- Útil per identificar outliers o patrons

**Ús**:
- Validar hipòtesis estadístiques
- Identificar correlacions entre variables
- Detectar anomalies en les dades

---

### 5️⃣ 📥 Exportar

**Descripció**: Descarrega les dades en formats estàndard.

**Formats disponibles:**
- **CSV**: Format text planer, compatible amb Excel, Python, etc.
- **Excel**: Format .xlsx amb estructura de taula

**Com funciona:**
1. Selecciona el format desitjat
2. Tria quins sectors vols exportar
3. Clica el botó de descàrrega

**Nota**: S'exportaran els registres segons els filtres aplicats (sectors i anys)

**Ús**:
- Compartir dades amb altres persones
- Processar dades amb altres eines (Excel, Python, etc.)
- Fer backups de les dades

---

### 6️⃣ ➕ Afegir Registre (NOMÉS ADMINS)

**Descripció**: Permet crear nous registres EDV. VISIBLE SOLS PER ADMINISTRADORS.

**Com funciona:**

**Secció 1: Dades Bàsiques**
- **Sector**: Selecciona de la llista desplegable (obligatori)
- **Código Actuación**: Codi identificador (obligatori)
- **Nom Actuació**: Descripció del projecte (obligatori)
- **Municipi**: Localitat (obligatori)
- **Any**: Any del projecte (obligatori)
- **Codi Actuació**: Codi alternatiu (opcional)
- **Tipus Actuació**: Selecciona el tipus (residencial, comercial, etc.)
- **Hipòtesis**: Fase del projecte (per adquisició, planejament, etc.)
- **Titular Adm. Act.**: Organització responsable

**Secció 2: Dades Físiques**
- **Sòl Sistemes**: m² de sòl per sistemes
- **Sòl Zones**: m² de sòl per zones
- **Total Àmbit**: m² total
- **Sòl Viari**: m² viari
- **Sostre Zones**: m² sostre de zones
- **Edificabilitat Bruta**: m² edificable
- **Sostre Residencial**: m² residencial
- **Nombre Habitatges**: Quantitat d'habitatges

**Secció 3: Dades Econòmiques**
- **Total Ingressos**: Ingressos totals (€)
- **Cessió Administració**: Import cedit
- **Despesa Comercialització**: Costos de venta
- **Aprofitament Privats**: Benefici privat (€)
- **Obres d'Urbanització**: Cost d'obres (€)
- **Connexions i Cànons**: Taxes de connexió (€)
- **Indemnitzacions**: Indemnitzacions (€)
- **Gestió**: Costos de gestió (€)
- **Despesa Total**: Despesa total (€)

**Validació**:
- Els camps marcats amb * són obligatoris
- Si falten camps, mostra quins
- Valida que els camps de text no estiguin buits

**Confirmació**:
- Si té èxit: Mostra ✅ i descàrrega automàtica
- Si falla: Mostra el missatge d'error exacte

**Ús**:
- Afegir nous projectes a la base de dades
- Actualitzar informació de projectes existents
- Mantenir la BD actualitzada

---

## ⚙️ Configuració i Filtres

### Com funcionen els filtres

1. **Selecciona Sectors**: Escull quins sectors vols analitzar
   - Opció per defecte: Primeres 3 sectors
   - Pots deseleccionar tot i triar-ne de nous

2. **Selecciona Anys**: Tria quin rang temporal vols
   - Opció per defecte: Tots els anys disponibles
   - Pots filtrar per anys específics

3. **Comptador**: Mostra quants registres coincideixen

**Nota**: Els filtres s'apliquen a TOTES les seccions (excepte "Afegir Registre")

---

## 💾 Com Executar l'Aplicació

### Requisits
- Python 3.8+
- MySQL (o base de dades compatible)
- Streamlit instal·lat
- Dependències: pandas, plotly, mysql-connector

### Passos de Configuració

1. **Configura `.streamlit/secrets.toml`**:
```ini
[mysql]
host = "localhost"
user = "root"
password = ""
database = "gestio_de_projectes"
```

2. **Instal·la dependències**:
```bash
pip install -r requirements.txt
```

3. **Executa l'app**:
```bash
streamlit run Home.py
```

4. **Accedeix a través del navegador**:
Normalment apareixerà a `http://localhost:8501`

---

## 🔧 Gestió d'Usuaris

### Per afegir nous usuaris

Edita el fitxer `Home.py` i busca la secció `USERS`:

```python
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "usuario": {"password": "user123", "role": "user"},
    "viewer": {"password": "viewer123", "role": "viewer"},
    # Afegeix nous usuaris aquí:
    "nouusuari": {"password": "contrasenya", "role": "user"}
}
```

**Rols disponibles**:
- `"admin"`: Accés total
- `"user"`: Accés limitat (sense crear registres)
- `"viewer"`: Sols lectura

### Per producció

En producció, NO guardes contrasenyes directament al codi. Usa:
- Variables d'entorn
- Base de dades segura
- Sistemes d'autenticació com Azure AD, LDAP, etc.

---

## 🎨 Característiques de Disseny

- **Interfície responsiva**: Funciona en ordinador, tauleta i mòbil
- **Temes**: Suporta temes clar i fosc (depenent de les preferències del sistema)
- **Badges de rol**: Indicador visual del rol de l'usuari
- **Gràfics interactius**: Pots fer hover per veure detalls
- **Taules ordenables**: Clica les capçaleres per ordenar
- **Descàrregues ràpides**: Exporta amb un sol click

---


