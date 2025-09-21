#!/usr/bin/env python3
"""
Script para verificar la configuración del proyecto
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Verificar configuración del entorno."""
    print("🔍 Verificando configuración del entorno...")
    print("=" * 50)
    
    # Verificar variables de entorno
    env_vars = {
        'FLASK_ENV': os.environ.get('FLASK_ENV', 'development'),
        'VITE_API_URL': os.environ.get('VITE_API_URL', 'No configurada'),
    }
    
    for var, value in env_vars.items():
        print(f"📋 {var}: {value}")
    
    print("\n🔧 Configuración automática:")
    
    # Detectar entorno
    is_production = env_vars['FLASK_ENV'] == 'production'
    
    if is_production:
        print("   🌐 Modo: PRODUCCIÓN")
        print("   🔗 Frontend: https://email-manager-ia-testing.vercel.app")
        print("   🔗 Backend: https://emailmanageriatesting.onrender.com")
        print("   🔗 API: https://emailmanageriatesting.onrender.com/api")
    else:
        print("   🏠 Modo: DESARROLLO")
        print("   🔗 Frontend: http://localhost:5178")
        print("   🔗 Backend: http://localhost:5000")
        print("   🔗 API: http://localhost:5000/api")
    
    return is_production

def check_files():
    """Verificar archivos de configuración."""
    print("\n📁 Verificando archivos de configuración...")
    print("=" * 50)
    
    files_to_check = [
        "backend/app/config.py",
        "frontend/vite.config.js",
        "frontend/src/services/api.js",
        "render.yaml",
        "frontend/vercel.json"
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - No encontrado")
    
    return True

def check_dependencies():
    """Verificar dependencias."""
    print("\n📦 Verificando dependencias...")
    print("=" * 50)
    
    # Backend
    backend_requirements = Path("backend/requirements.txt")
    if backend_requirements.exists():
        print("✅ backend/requirements.txt")
    else:
        print("❌ backend/requirements.txt - No encontrado")
    
    # Frontend
    frontend_package = Path("frontend/package.json")
    if frontend_package.exists():
        print("✅ frontend/package.json")
    else:
        print("❌ frontend/package.json - No encontrado")
    
    return True

def main():
    """Función principal."""
    print("🚀 Email Manager IA - Verificación de Configuración")
    print("=" * 60)
    
    # Verificar entorno
    is_production = check_environment()
    
    # Verificar archivos
    check_files()
    
    # Verificar dependencias
    check_dependencies()
    
    print("\n" + "=" * 60)
    print("📋 Resumen:")
    
    if is_production:
        print("🌐 Configurado para PRODUCCIÓN")
        print("   • Usa servidores externos (Vercel + Render)")
        print("   • Base de datos PostgreSQL en Render")
        print("   • Variables de entorno de producción")
    else:
        print("🏠 Configurado para DESARROLLO")
        print("   • Usa servidores locales")
        print("   • Base de datos SQLite local")
        print("   • Configuración de desarrollo")
    
    print("\n🔧 Para cambiar el entorno:")
    print("   • Desarrollo: No configurar FLASK_ENV o configurar como 'development'")
    print("   • Producción: Configurar FLASK_ENV='production'")
    
    print("\n🚀 Para iniciar el desarrollo:")
    print("   • Backend: cd backend && python run.py")
    print("   • Frontend: cd frontend && npm run dev")
    print("   • O usar: python start_dev.py")

if __name__ == '__main__':
    main()
