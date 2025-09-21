#!/usr/bin/env python3
"""
Script para iniciar el desarrollo con configuración automática
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    print("🚀 Email Manager IA - Desarrollo")
    print("=" * 50)
    print("📋 Configuración automática:")
    print("   • Frontend: http://localhost:5178")
    print("   • Backend: http://localhost:5000")
    print("   • API: http://localhost:5000/api")
    print("   • Health: http://localhost:5000/api/health")
    print("=" * 50)

def check_backend():
    """Verificar que el backend esté funcionando."""
    try:
        import requests
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend funcionando correctamente")
            return True
        else:
            print(f"⚠️  Backend respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend no disponible: {e}")
        return False

def start_backend():
    """Iniciar el backend."""
    print("\n🔧 Iniciando backend...")
    backend_dir = Path("backend")
    if backend_dir.exists():
        try:
            # Cambiar al directorio backend y ejecutar
            os.chdir(backend_dir)
            subprocess.Popen([sys.executable, "run.py"], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
            print("✅ Backend iniciado en segundo plano")
            os.chdir("..")
            return True
        except Exception as e:
            print(f"❌ Error iniciando backend: {e}")
            return False
    else:
        print("❌ Directorio backend no encontrado")
        return False

def start_frontend():
    """Iniciar el frontend."""
    print("\n🎨 Iniciando frontend...")
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        try:
            # Cambiar al directorio frontend y ejecutar
            os.chdir(frontend_dir)
            subprocess.run(["npm", "run", "dev"], check=True)
        except Exception as e:
            print(f"❌ Error iniciando frontend: {e}")
            return False
    else:
        print("❌ Directorio frontend no encontrado")
        return False

def main():
    """Función principal."""
    print_banner()
    
    # Verificar si el backend ya está corriendo
    if check_backend():
        print("✅ Backend ya está funcionando")
    else:
        print("🔧 Iniciando backend...")
        if not start_backend():
            print("❌ No se pudo iniciar el backend")
            return
    
    # Esperar un momento para que el backend se inicie
    print("⏳ Esperando que el backend se inicie...")
    import time
    time.sleep(3)
    
    # Verificar nuevamente
    if check_backend():
        print("✅ Backend funcionando correctamente")
        print("\n🎨 Iniciando frontend...")
        print("📱 Abre http://localhost:5178 en tu navegador")
        start_frontend()
    else:
        print("❌ Backend no se pudo iniciar correctamente")

if __name__ == '__main__':
    main()
