#!/usr/bin/env python3
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
