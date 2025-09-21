#!/usr/bin/env python3
"""
Script para configurar el despliegue con nueva cuenta
"""

import os
import shutil
from pathlib import Path

def setup_new_deployment():
    """Configura los archivos para el despliegue con nueva cuenta"""
    
    print("🚀 Configurando despliegue con nueva cuenta...")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Error: Ejecuta este script desde el directorio raíz del proyecto")
        return
    
    # 1. Crear backup de archivos originales
    print("📁 Creando backup de archivos originales...")
    if os.path.exists("render.yaml"):
        shutil.copy("render.yaml", "render-original.yaml")
        print("✅ Backup de render.yaml creado")
    
    if os.path.exists("frontend/vercel.json"):
        shutil.copy("frontend/vercel.json", "frontend/vercel-original.json")
        print("✅ Backup de vercel.json creado")
    
    # 2. Copiar archivos de nueva cuenta
    print("📋 Configurando archivos para nueva cuenta...")
    
    if os.path.exists("render-nuevo.yaml"):
        shutil.copy("render-nuevo.yaml", "render.yaml")
        print("✅ render.yaml actualizado para nueva cuenta")
    
    if os.path.exists("frontend/vercel-nuevo.json"):
        shutil.copy("frontend/vercel-nuevo.json", "frontend/vercel.json")
        print("✅ vercel.json actualizado para nueva cuenta")
    
    # 3. Crear archivo de variables de entorno de ejemplo
    env_example = """# Variables de Entorno para Nueva Cuenta
# Copia este archivo como .env y completa los valores

# Backend (Render)
FLASK_ENV=production
SECRET_KEY=tu-secret-key-muy-largo-y-seguro-aqui
JWT_SECRET_KEY=tu-jwt-secret-key-muy-largo-y-seguro-aqui
DATABASE_URL=postgresql://usuario:password@host:puerto/database

# Microsoft Azure
MICROSOFT_CLIENT_ID=tu-client-id-aqui
MICROSOFT_CLIENT_SECRET=tu-client-secret-aqui
MICROSOFT_TENANT_ID=tu-tenant-id-aqui
MICROSOFT_REDIRECT_URI=https://tu-backend-nuevo.onrender.com/auth/callback

# OpenAI
OPENAI_API_KEY=tu-openai-api-key-aqui
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.3

# Frontend (Vercel)
VITE_API_URL=https://tu-backend-nuevo.onrender.com/api
"""
    
    with open("env-nuevo-ejemplo.txt", "w", encoding="utf-8") as f:
        f.write(env_example)
    
    print("✅ Archivo de variables de entorno de ejemplo creado: env-nuevo-ejemplo.txt")
    
    # 4. Crear script de verificación
    verification_script = """#!/usr/bin/env python3
import requests
import json

def verify_deployment():
    print("🔍 Verificando despliegue...")
    
    # URLs que necesitarás actualizar
    backend_url = "https://tu-backend-nuevo.onrender.com"
    frontend_url = "https://tu-frontend-nuevo.vercel.app"
    
    print(f"Backend URL: {backend_url}")
    print(f"Frontend URL: {frontend_url}")
    
    # Verificar backend
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend funcionando")
        else:
            print("❌ Backend no responde")
    except Exception as e:
        print(f"❌ Error verificando backend: {e}")
    
    # Verificar frontend
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend funcionando")
        else:
            print("❌ Frontend no responde")
    except Exception as e:
        print(f"❌ Error verificando frontend: {e}")

if __name__ == "__main__":
    verify_deployment()
"""
    
    with open("verify_deployment.py", "w", encoding="utf-8") as f:
        f.write(verification_script)
    
    print("✅ Script de verificación creado: verify_deployment.py")
    
    print("\n" + "=" * 50)
    print("🎯 Próximos pasos:")
    print("1. Ve a https://render.com y crea una cuenta nueva")
    print("2. Ve a https://vercel.com y crea una cuenta nueva")
    print("3. Crea una base de datos PostgreSQL en Render")
    print("4. Configura las variables de entorno en ambos servicios")
    print("5. Despliega el backend en Render")
    print("6. Despliega el frontend en Vercel")
    print("7. Actualiza las URLs en ambos servicios")
    print("8. Ejecuta: python verify_deployment.py")
    print("\n📋 Revisa el archivo DEPLOYMENT_NEW_ACCOUNT.md para instrucciones detalladas")

if __name__ == "__main__":
    setup_new_deployment()
