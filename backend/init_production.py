#!/usr/bin/env python3
"""
Script de inicialización para producción
"""

import os
import sys
from datetime import datetime

def init_production():
    """Inicializar la aplicación para producción."""
    
    print("🚀 Inicializando Email Manager IA para producción...")
    print("=" * 60)
    
    # Verificar variables de entorno
    print("1️⃣ Verificando variables de entorno...")
    try:
        from check_env import check_environment
        if not check_environment():
            print("❌ Variables de entorno no configuradas correctamente")
            return False
    except Exception as e:
        print(f"❌ Error verificando entorno: {e}")
        return False
    
    # Inicializar aplicación
    print("\n2️⃣ Inicializando aplicación Flask...")
    try:
        from app import create_app, db
        app = create_app()
        print("✅ Aplicación Flask inicializada")
    except Exception as e:
        print(f"❌ Error inicializando Flask: {e}")
        return False
    
    # Inicializar base de datos
    print("\n3️⃣ Inicializando base de datos...")
    try:
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas de base de datos creadas")
            
            # Verificar tablas
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Tablas disponibles: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False
    
    # Verificar servicios
    print("\n4️⃣ Verificando servicios externos...")
    
    # OpenAI
    try:
        from app.services.openai_service import OpenAIService
        openai_service = OpenAIService()
        status = openai_service.get_status()
        if status['status'] == 'ready':
            print("✅ OpenAI: Conectado")
        else:
            print(f"⚠️  OpenAI: {status['message']}")
    except Exception as e:
        print(f"❌ OpenAI: Error - {e}")
    
    # Microsoft Graph (solo verificar configuración)
    try:
        from app.config import Config
        config = Config()
        if config.MICROSOFT_CLIENT_ID and config.MICROSOFT_CLIENT_SECRET:
            print("✅ Microsoft Graph: Configurado")
        else:
            print("⚠️  Microsoft Graph: Credenciales no configuradas")
    except Exception as e:
        print(f"❌ Microsoft Graph: Error - {e}")
    
    # Verificar endpoints
    print("\n5️⃣ Verificando endpoints...")
    try:
        with app.test_client() as client:
            # Health check
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ Health check: OK")
            else:
                print(f"⚠️  Health check: {response.status_code}")
            
            # Debug endpoint
            response = client.get('/api/debug')
            if response.status_code == 200:
                print("✅ Debug endpoint: OK")
            else:
                print(f"⚠️  Debug endpoint: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error verificando endpoints: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 Inicialización completada")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print("\n📋 Próximos pasos:")
    print("1. Verifica que todas las variables de entorno estén configuradas en Render")
    print("2. Despliega el frontend en Vercel")
    print("3. Prueba la aplicación completa")
    print("\n🔗 URLs importantes:")
    print("- Health check: /api/health")
    print("- Debug info: /api/debug")
    print("- Database health: /api/health/db")
    
    return True

if __name__ == '__main__':
    success = init_production()
    if not success:
        sys.exit(1)
