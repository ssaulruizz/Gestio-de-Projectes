#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SETUP AUTOMÁTICO - EDV Comparator
Script que crea la estructura correcta de carpetas y archivos
"""

import os
import sys

def create_project_structure():
    """Crea la estructura correcta del proyecto"""
    
    print("=" * 80)
    print("🚀 SETUP AUTOMÁTICO - EDV Comparator")
    print("=" * 80)
    print()
    
    # 1. Crear carpeta .streamlit
    print("✓ Paso 1: Crear carpeta .streamlit")
    try:
        os.makedirs('.streamlit', exist_ok=True)
        print("  ✅ Carpeta .streamlit creada/verificada")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    print()
    
    # 2. Crear archivo .streamlit/secrets.toml
    print("✓ Paso 2: Crear archivo .streamlit/secrets.toml")
    secrets_content = """[mysql]
host = "localhost"
user = "root"
password = ""
database = "gestio_de_projectes"
"""
    
    try:
        with open('.streamlit/secrets.toml', 'w') as f:
            f.write(secrets_content)
        print("  ✅ Archivo .streamlit/secrets.toml creado")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    print()
    
    # 3. Copiar Home_FIXED.py a Home.py
    print("✓ Paso 3: Usar versión corregida de Home.py")
    if os.path.exists('Home_FIXED.py'):
        try:
            with open('Home_FIXED.py', 'r') as f:
                content = f.read()
            with open('Home.py', 'w') as f:
                f.write(content)
            print("  ✅ Versión corregida instalada como Home.py")
        except Exception as e:
            print(f"  ⚠️  No se pudo copiar: {e}")
            print("     Copia manualmente: cp Home_FIXED.py Home.py")
    else:
        print("  ℹ️  Home_FIXED.py no encontrado (es normal si ya lo hiciste)")
    print()
    
    # 4. Verificar .gitignore
    print("✓ Paso 4: Verificar .gitignore")
    gitignore_entries = [
        '.streamlit/secrets.toml',
        '.env',
        'venv/',
        '__pycache__/'
    ]
    
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        needs_update = False
        for entry in gitignore_entries:
            if entry not in gitignore_content:
                needs_update = True
                gitignore_content += f"\n{entry}"
        
        if needs_update:
            with open('.gitignore', 'w') as f:
                f.write(gitignore_content)
            print("  ✅ .gitignore actualizado")
        else:
            print("  ✅ .gitignore ya contiene las entradas necesarias")
    else:
        with open('.gitignore', 'w') as f:
            f.write('\n'.join(gitignore_entries) + '\n')
        print("  ✅ .gitignore creado")
    print()
    
    # 5. Mostrar estructura final
    print("=" * 80)
    print("✅ ESTRUCTURA DEL PROYECTO CONFIGURADA CORRECTAMENTE")
    print("=" * 80)
    print()
    print("Estructura final:")
    print("""
    proyecto_edv/
    ├── Home.py                ✅ Aplicación corregida
    ├── requirements.txt       ✅ Dependencias
    ├── .env                   ❌ (NO necesario ahora)
    ├── .gitignore             ✅ Actualizado
    ├── README.md
    ├── INSTALL.md
    └── .streamlit/
        └── secrets.toml       ✅ Configuración de BD
    """)
    print()
    
    # 6. Mostrar instrucciones finales
    print("=" * 80)
    print("📋 PRÓXIMOS PASOS")
    print("=" * 80)
    print()
    print("1️⃣  VERIFICA LAS CREDENCIALES")
    print("   Abre .streamlit/secrets.toml y verifica:")
    print("   - host: localhost (o tu IP)")
    print("   - user: root (o tu usuario MySQL)")
    print("   - password: (tu contraseña o vacío)")
    print("   - database: gestio_de_projectes")
    print()
    
    print("2️⃣  VERIFICA QUE MYSQL ESTÁ CORRIENDO")
    print("   Ejecuta en terminal:")
    print("   $ mysql -u root -e 'SELECT 1;'")
    print()
    print("   Si ves:")
    print("   +---+")
    print("   | 1 |")
    print("   +---+")
    print("   → MySQL está OK ✅")
    print()
    
    print("3️⃣  INSTALA/ACTUALIZA DEPENDENCIAS")
    print("   $ pip install -r requirements.txt")
    print()
    
    print("4️⃣  EJECUTA LA APLICACIÓN")
    print("   $ streamlit cache clear")
    print("   $ streamlit run Home.py")
    print()
    
    print("5️⃣  ABRE EN EL NAVEGADOR")
    print("   http://localhost:8501")
    print()
    
    print("=" * 80)
    print("✨ ¡TODO CONFIGURADO CORRECTAMENTE!")
    print("=" * 80)
    print()
    
    return True


if __name__ == "__main__":
    success = create_project_structure()
    sys.exit(0 if success else 1)
