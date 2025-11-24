# Diccionario de Datos - Base de Datos EDV
## ORDEN ORIGINAL DEL EXCEL (CON CAMPO SECTOR)

### Información General
- **Base de datos**: EDV (Estudis de Viabilitat)
- **Tabla**: edv_fitxes
- **Fuente**: Sección A. Resum fitxa EDV
- **Registros**: 12 snapshots de 4 sectores diferentes
- **Campos**: 47 campos de datos + 5 identificadores = 52 columnas totales

---

## Estructura de la Tabla

### Identificadores Principales
| # | Campo SQL | Tipo | Descripción |
|---|-----------|------|-------------|
| 1 | id | INT PK AUTO_INCREMENT | Identificador único del registro |
| 2 | **sector** | **VARCHAR(50)** | **Sector (A, B, C) - Row 5 del Excel** |
| 3 | codigo_actuacion | VARCHAR(50) NOT NULL | Código de actuación del sector |
| 4 | nom_actuacio | VARCHAR(255) | Nombre de la actuación/sector |
| 5 | municipi | VARCHAR(255) | Municipio donde se ubica |
| 6 | any | INT | Año del análisis EDV |

---

## Campos de Datos (en orden del Excel)


### Informació sector

| # | Campo SQL | Tipo | Campo Original |
|---|-----------|------|----------------|
| 7 | Codi_Actuacio | VARCHAR(255) | Codi Actuació |
| 8 | Nom_Actuacio | VARCHAR(255) | Nom Actuació |
| 9 | Municipi | VARCHAR(255) | Municipi |
| 10 | Tipus_actuacio | VARCHAR(255) | Tipus actuació |
| 11 | Sol_sistemes | DECIMAL(20,10) | Sòl sistemes |
| 12 | Sol_zones | DECIMAL(20,10) | Sòl zones |
| 13 | Total_ambit | DECIMAL(20,10) | Total àmbit |
| 14 | Sol_viari | DECIMAL(20,10) | Sòl viari |
| 15 | Sostre_zones | DECIMAL(20,10) | Sostre zones |
| 16 | edificabilitat_bruta | DECIMAL(20,10) | edificabilitat bruta |
| 17 | Sostre_residencial | DECIMAL(20,10) | Sostre residencial |
| 18 | Nombre_dhabitatges | INT | Nombre d'habitatges |

### Informació EDV

| # | Campo SQL | Tipo | Campo Original |
|---|-----------|------|----------------|
| 19 | Any | INT | Any |
| 20 | Hipotesis | VARCHAR(255) | Hipòtesis |
| 21 | E1__Programacio | VARCHAR(255) | E1. Programació |
| 22 | E2__Adquisicio | VARCHAR(255) | E2. Adquisició |
| 23 | E3__Planejament | VARCHAR(255) | E3. Planejament |
| 24 | E4__Projecte_durbanitzacio | VARCHAR(255) | E4. Projecte d'urbanització |
| 25 | E5__Projecte_de_reparcellacio | VARCHAR(255) | E5. Projecte de reparcel·lació |
| 26 | E6__Execucio_obres | VARCHAR(255) | E6. Execució obres |
| 27 | E7__Comercialitzacio | VARCHAR(255) | E7. Comercialització |
| 28 | E8__Compte_liquidacio_definitiva | VARCHAR(255) | E8. Compte liquidació definitiva |
| 29 | E9__Tancament_darrera_venda | VARCHAR(255) | E9. Tancament (darrera venda) |

### Estructura propietat

| # | Campo SQL | Tipo | Campo Original |
|---|-----------|------|----------------|
| 30 | Incasol | DECIMAL(20,10) | Incasòl |
| 31 | Altres_propietaris | DECIMAL(20,10) | Altres propietaris |
| 32 | Sol_amb_drets | DECIMAL(20,10) | Sòl amb drets |
| 33 | Sol_sense_drets | DECIMAL(20,10) | Sòl sense drets |
| 34 | Titular_Adm__Act_ | VARCHAR(255) | Titular Adm. Act. |
| 35 | pct_drets_Adm__Act_ | DECIMAL(20,10) | % drets Adm. Act. |

### EDV sector

| # | Campo SQL | Tipo | Campo Original |
|---|-----------|------|----------------|
| 36 | Total_Ingressos | DECIMAL(20,10) | Total Ingressos |
| 37 | Cessio_Administracio_actuant | DECIMAL(20,10) | Cessió Administració actuant |
| 38 | despesa_comercialitzacio | DECIMAL(20,10) | despesa comercialització |
| 39 | Aprofitament_privats | DECIMAL(20,10) | Aprofitament privats |
| 40 | Obres_durbanitzacio | DECIMAL(20,10) | Obres d'urbanització |
| 41 | Connexions_i_canons | DECIMAL(20,10) | Connexions i cànons |
| 42 | Indemnitzacions | DECIMAL(20,10) | Indemnitzacions |
| 43 | Gestio | DECIMAL(20,10) | Gestió |
| 44 | Despesa_a_assumir_Adm__Act_ | DECIMAL(20,10) | Despesa a assumir Adm. Act. |
| 45 | Despesa_total | DECIMAL(20,10) | Despesa total |

### Càlcul dinàmic

| # | Campo SQL | Tipo | Campo Original |
|---|-----------|------|----------------|
| 46 | Calcul_dinamic_Taxa_aplicada | DECIMAL(20,10) | Taxa aplicada |
| 47 | Calcul_dinamic_Valor_residual_sol | DECIMAL(20,10) | Valor residual sòl |
| 48 | Calcul_dinamic_Valor_unitari | DECIMAL(20,10) | Valor unitari |
| 49 | Calcul_dinamic_Temps_mig_retorn | DECIMAL(20,10) | Temps mig retorn |

### Càlcul estàtic

| # | Campo SQL | Tipo | Campo Original |
|---|-----------|------|----------------|
| 50 | Calcul_estatic_Taxa_aplicada | DECIMAL(20,10) | Taxa aplicada |
| 51 | Calcul_estatic_Valor_residual_sol | DECIMAL(20,10) | Valor residual sòl |
| 52 | Calcul_estatic_Valor_unitari | DECIMAL(20,10) | Valor unitari |
| 53 | Calcul_estatic_Temps_mig_retorn | DECIMAL(20,10) | Temps mig retorn |


---

## Notas Importantes

### Campo SECTOR (NUEVO)
El campo **sector** se extrae de la fila 5 del Excel, donde se agrupan los análisis:
- **Sector A**: Hospitalet Llobregat (código 1444-1)
- **Sector B**: Granollers (código 0128-2)
- **Sector C**: Vilafranca del Penedès (códigos 1223-1 y 1223-2)

Este campo facilita consultas y agrupaciones por sector.

### Campos Duplicados Intencionales
Los siguientes campos aparecen duplicados porque existen tanto como identificadores principales como en los datos del Excel:
- **Codi_Actuacio** / codigo_actuacion
- **Nom_Actuacio** / nom_actuacio  
- **Municipi** / municipi
- **Any** / any

Esto es intencional para preservar la estructura exacta del Excel original.

### Campos con Categoría Heredada
Algunos campos no tienen categoría explícita en el Excel, pero heredan la categoría del campo anterior:
- Campos después de "Càlcul dinàmic_Taxa aplicada" pertenecen a "Càlcul dinàmic"
- Campos después de "Càlcul estàtic_Taxa aplicada" pertenecen a "Càlcul estàtic"

### Sección Excluida
La sección **B. Explotació de dades** del Excel NO se incluye en esta base de datos según especificación del usuario.

---

## Datos Contenidos

### Sectores y Registros
| Sector | Código | Nombre | Municipio | Análisis |
|--------|--------|--------|-----------|----------|
| Sector A | 1444-1 | Sector A | Hospitalet Llobregat | 4 (2005, 2017, 2021, 2023) |
| Sector B | 0128-2 | Sector B | Granollers | 3 (2010, 2022, 2025) |
| Sector C | 1223-1 | Sector C | Vilafranca del Penedès | 4 (2004, 2006, 2007, 2010) |
| Sector C | 1223-2 | Sector C | Vilafranca del Penedès | 1 (2025) |

**Total**: 12 registros con datos históricos de 2004 a 2025

---

## Consultas de Ejemplo con Campo Sector

```sql
-- Obtener todos los análisis de un sector específico
SELECT * FROM edv_fitxes WHERE sector = 'Sector A';

-- Comparar sectores en un año específico
SELECT sector, codigo_actuacion, Total_Ingressos, Despesa_total
FROM edv_fitxes 
WHERE any = 2010
ORDER BY sector;

-- Análisis por sector (promedios)
SELECT sector, 
       COUNT(*) as num_analisis,
       AVG(Total_Ingressos) as ingresos_promedio,
       AVG(Despesa_total) as despesa_promedio
FROM edv_fitxes
GROUP BY sector;
```
