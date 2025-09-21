#!/usr/bin/env python3
"""
Script para verificar el estado de los rate limits de OpenAI
"""

import requests
import json
import time
from datetime import datetime, timedelta

def check_openai_rate_limits():
    """Verifica el estado de los rate limits de OpenAI"""
    
    print("🔍 Verificando estado de rate limits de OpenAI...")
    print("=" * 50)
    
    try:
        # Verificar si el servidor está funcionando
        response = requests.get("http://localhost:5000/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Servidor backend funcionando")
        else:
            print("❌ Servidor backend no responde")
            return
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return
    
    try:
        # Verificar rate limits específicos
        response = requests.get("http://localhost:5000/api/emails/openai-rate-limit", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Estado de rate limits:")
            print(f"   - OpenAI configurado: {data.get('openai_configured', False)}")
            print(f"   - Modelo: {data.get('model', 'N/A')}")
            print(f"   - Último error: {data.get('last_error', 'Ninguno')}")
            print(f"   - Timestamp: {data.get('timestamp', 'N/A')}")
            
            if data.get('last_error'):
                error = data.get('last_error', '')
                if 'rate_limit' in error.lower() or '429' in error:
                    print("⚠️  RATE LIMIT ACTIVO - Esperando reset...")
                    
                    # Calcular tiempo de espera estimado
                    if '20s' in error:
                        print("   - RPM reset: ~20 segundos")
                    elif '5h' in error or '5h17m' in error:
                        print("   - TPM reset: ~5 horas y 17 minutos")
                        print("   - Hora estimada de reset:", (datetime.now() + timedelta(hours=5, minutes=17)).strftime("%H:%M:%S"))
                else:
                    print("   - Otro error de OpenAI")
            else:
                print("✅ No hay rate limits activos")
        else:
            print(f"❌ Error verificando rate limits: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando rate limits: {e}")
    
    print("\n" + "=" * 50)
    print("💡 Recomendaciones:")
    print("1. Si hay rate limit activo, espera el tiempo indicado")
    print("2. Considera actualizar tu plan de OpenAI para límites más altos")
    print("3. Mientras tanto, la app usará clasificación basada en reglas")
    print("4. Los límites se han configurado ultra conservadores para evitar rate limits")

if __name__ == "__main__":
    check_openai_rate_limits()
