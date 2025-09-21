#!/usr/bin/env python3
"""
Script para verificar variables de entorno en producción
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Verificar que todas las variables de entorno estén configuradas."""
    
    print("🔍 Verificando variables de entorno...")
    print("=" * 50)
    
    # Variables requeridas
    required_vars = {
        'FLASK_ENV': 'production',
        'SECRET_KEY': 'string',
        'JWT_SECRET_KEY': 'string',
        'DATABASE_URL': 'postgresql://...',
        'MICROSOFT_CLIENT_ID': 'string',
        'MICROSOFT_CLIENT_SECRET': 'string',
        'MICROSOFT_TENANT_ID': 'string',
        'MICROSOFT_REDIRECT_URI': 'https://...',
        'OPENAI_API_KEY': 'string'
    }
    
    # Variables opcionales con valores por defecto
    optional_vars = {
        'OPENAI_MODEL': 'gpt-4o-mini',
        'OPENAI_MAX_TOKENS': '1000',
        'OPENAI_TEMPERATURE': '0.3'
    }
    
    missing_vars = []
    invalid_vars = []
    
    # Verificar variables requeridas
    for var, expected_type in required_vars.items():
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: NO CONFIGURADA")
        else:
            if expected_type == 'string' and len(value) < 10:
                invalid_vars.append(f"{var} (muy corta)")
                print(f"⚠️  {var}: {value[:20]}... (muy corta)")
            elif expected_type == 'postgresql://...' and not value.startswith('postgresql://'):
                invalid_vars.append(f"{var} (formato incorrecto)")
                print(f"⚠️  {var}: {value[:20]}... (formato incorrecto)")
            elif expected_type == 'https://...' and not value.startswith('https://'):
                invalid_vars.append(f"{var} (formato incorrecto)")
                print(f"⚠️  {var}: {value[:20]}... (formato incorrecto)")
            else:
                print(f"✅ {var}: {value[:20]}...")
    
    # Verificar variables opcionales
    print("\n📋 Variables opcionales:")
    for var, default_value in optional_vars.items():
        value = os.environ.get(var, default_value)
        print(f"✅ {var}: {value}")
    
    # Resumen
    print("\n" + "=" * 50)
    if missing_vars:
        print(f"❌ Variables faltantes: {', '.join(missing_vars)}")
        return False
    
    if invalid_vars:
        print(f"⚠️  Variables con problemas: {', '.join(invalid_vars)}")
        return False
    
    print("✅ Todas las variables de entorno están configuradas correctamente")
    return True

def check_database_connection():
    """Verificar conexión a la base de datos."""
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            db.session.execute('SELECT 1')
            print("✅ Conexión a base de datos: OK")
            return True
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return False

def check_openai_connection():
    """Verificar conexión a OpenAI."""
    try:
        from app.services.openai_service import OpenAIService
        service = OpenAIService()
        status = service.get_status()
        
        if status['status'] == 'ready':
            print("✅ Conexión a OpenAI: OK")
            return True
        else:
            print(f"⚠️  OpenAI: {status['message']}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión a OpenAI: {e}")
        return False

def main():
    """Función principal."""
    print("🚀 Email Manager IA - Verificación de Entorno")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar variables de entorno
    env_ok = check_environment()
    
    if not env_ok:
        print("\n❌ Configuración de entorno incompleta")
        sys.exit(1)
    
    # Verificar conexiones
    print("\n🔌 Verificando conexiones...")
    db_ok = check_database_connection()
    openai_ok = check_openai_connection()
    
    if db_ok and openai_ok:
        print("\n✅ Todas las verificaciones pasaron correctamente")
        print("🚀 La aplicación está lista para producción")
    else:
        print("\n⚠️  Algunas verificaciones fallaron")
        print("🔧 Revisa la configuración antes de desplegar")

if __name__ == '__main__':
    main()
