-- ============================================================================
-- BASE DE DATOS: EDV (Estudis de Viabilitat)
-- Tabla: edv_fitxes
-- ============================================================================
-- Descripción: Almacena todas las fichas EDV con información completa sobre
--              sectores urbanísticos en Catalunya
-- Fuente: Sección A. Resum fitxa EDV del Excel original
-- Nota: Excluye sección B. Explotació de dades según especificación
-- Orden: Campos ordenados exactamente como aparecen en el Excel
-- ============================================================================

USE gestio_de_projectes;
CREATE TABLE edv_fitxes (
    -- ========================================================================
    -- IDENTIFICADORES Y METADATOS
    -- ========================================================================
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Identificador único del registro',
    sector VARCHAR(50) COMMENT 'Sector (A, B, C, etc.) - fila 5 del Excel',
    codigo_actuacion VARCHAR(50) NOT NULL COMMENT 'Código de actuación del sector',
    nom_actuacio VARCHAR(255) COMMENT 'Nombre de la actuación o sector',
    municipi VARCHAR(255) COMMENT 'Municipio donde se ubica el sector',
    any INT COMMENT 'Año del análisis EDV',


    -- ========================================================================
    -- INFORMACIÓ SECTOR
    -- ========================================================================
    Codi_Actuacio VARCHAR(255) COMMENT 'Informació sector: Codi Actuació',
    Tipus_actuacio VARCHAR(255) COMMENT 'Informació sector: Tipus actuació',
    Sol_sistemes DECIMAL(20,10) COMMENT 'Informació sector: Sòl sistemes',
    Sol_zones DECIMAL(20,10) COMMENT 'Informació sector: Sòl zones',
    Total_ambit DECIMAL(20,10) COMMENT 'Informació sector: Total àmbit',
    Sol_viari DECIMAL(20,10) COMMENT 'Informació sector: Sòl viari',
    Sostre_zones DECIMAL(20,10) COMMENT 'Informació sector: Sostre zones',
    edificabilitat_bruta DECIMAL(20,10) COMMENT 'Informació sector: edificabilitat bruta',
    Sostre_residencial DECIMAL(20,10) COMMENT 'Informació sector: Sostre residencial',
    Nombre_dhabitatges INT COMMENT 'Informació sector: Nombre d''habitatges',

    -- ========================================================================
    -- INFORMACIÓ EDV
    -- ========================================================================
    Hipotesis VARCHAR(255) COMMENT 'Informació EDV: Hipòtesis',
    E1__Programacio VARCHAR(255) COMMENT 'Informació EDV: E1. Programació',
    E2__Adquisicio VARCHAR(255) COMMENT 'Informació EDV: E2. Adquisició',
    E3__Planejament VARCHAR(255) COMMENT 'Informació EDV: E3. Planejament',
    E4__Projecte_durbanitzacio VARCHAR(255) COMMENT 'Informació EDV: E4. Projecte d''urbanització',
    E5__Projecte_de_reparcellacio VARCHAR(255) COMMENT 'Informació EDV: E5. Projecte de reparcel·lació',
    E6__Execucio_obres VARCHAR(255) COMMENT 'Informació EDV: E6. Execució obres',
    E7__Comercialitzacio VARCHAR(255) COMMENT 'Informació EDV: E7. Comercialització',
    E8__Compte_liquidacio_definitiva VARCHAR(255) COMMENT 'Informació EDV: E8. Compte liquidació definitiva',
    E9__Tancament_darrera_venda VARCHAR(255) COMMENT 'Informació EDV: E9. Tancament (darrera venda)',

    -- ========================================================================
    -- ESTRUCTURA PROPIETAT
    -- ========================================================================
    Incasol DECIMAL(20,10) COMMENT 'Estructura propietat: Incasòl',
    Altres_propietaris DECIMAL(20,10) COMMENT 'Estructura propietat: Altres propietaris',
    Sol_amb_drets DECIMAL(20,10) COMMENT 'Estructura propietat: Sòl amb drets',
    Sol_sense_drets DECIMAL(20,10) COMMENT 'Estructura propietat: Sòl sense drets',
    Titular_Adm__Act_ VARCHAR(255) COMMENT 'Estructura propietat: Titular Adm. Act.',
    pct_drets_Adm__Act_ DECIMAL(20,10) COMMENT 'Estructura propietat: % drets Adm. Act.',

    -- ========================================================================
    -- EDV SECTOR
    -- ========================================================================
    Total_Ingressos DECIMAL(20,10) COMMENT 'EDV sector: Total Ingressos',
    Cessio_Administracio_actuant DECIMAL(20,10) COMMENT 'EDV sector: Cessió Administració actuant',
    despesa_comercialitzacio DECIMAL(20,10) COMMENT 'EDV sector: despesa comercialització',
    Aprofitament_privats DECIMAL(20,10) COMMENT 'EDV sector: Aprofitament privats',
    Obres_durbanitzacio DECIMAL(20,10) COMMENT 'EDV sector: Obres d''urbanització',
    Connexions_i_canons DECIMAL(20,10) COMMENT 'EDV sector: Connexions i cànons',
    Indemnitzacions DECIMAL(20,10) COMMENT 'EDV sector: Indemnitzacions',
    Gestio DECIMAL(20,10) COMMENT 'EDV sector: Gestió',
    Despesa_a_assumir_Adm__Act_ DECIMAL(20,10) COMMENT 'EDV sector: Despesa a assumir Adm. Act.',
    Despesa_total DECIMAL(20,10) COMMENT 'EDV sector: Despesa total',

    -- ========================================================================
    -- CÀLCUL DINÀMIC
    -- ========================================================================
    Calcul_dinamic_Taxa_aplicada DECIMAL(20,10) COMMENT 'Càlcul dinàmic: Taxa aplicada',
    Calcul_dinamic_Valor_residual_sol DECIMAL(20,10) COMMENT 'Càlcul dinàmic: Valor residual sòl',
    Calcul_dinamic_Valor_unitari DECIMAL(20,10) COMMENT 'Càlcul dinàmic: Valor unitari',
    Calcul_dinamic_Temps_mig_retorn DECIMAL(20,10) COMMENT 'Càlcul dinàmic: Temps mig retorn',

    -- ========================================================================
    -- CÀLCUL ESTÀTIC
    -- ========================================================================
    Calcul_estatic_Taxa_aplicada DECIMAL(20,10) COMMENT 'Càlcul estàtic: Taxa aplicada',
    Calcul_estatic_Valor_residual_sol DECIMAL(20,10) COMMENT 'Càlcul estàtic: Valor residual sòl',
    Calcul_estatic_Valor_unitari DECIMAL(20,10) COMMENT 'Càlcul estàtic: Valor unitari',
    Calcul_estatic_Temps_mig_retorn DECIMAL(20,10) COMMENT 'Càlcul estàtic: Temps mig retorn',

    -- ========================================================================
    -- ÍNDICES PARA OPTIMIZACIÓN DE CONSULTAS
    -- ========================================================================
    INDEX idx_sector_codigo_any (sector, codigo_actuacion, any),
    INDEX idx_codigo_any (codigo_actuacion, any),
    INDEX idx_municipi (municipi),
    INDEX idx_any (any),
    INDEX idx_sector (sector)
);
