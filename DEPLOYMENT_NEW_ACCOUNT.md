# 🚀 Guía de Despliegue - Nueva Cuenta

## 📋 **PASO 1: Preparar el Código**

### 1.1 Actualizar URLs de Producción
Necesitarás cambiar las URLs en estos archivos:

**`frontend/vercel.json`:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "env": {
    "VITE_API_URL": "https://TU-NUEVO-BACKEND.onrender.com/api"
  }
}
```

**`render.yaml`:**
```yaml
services:
  - type: web
    name: email-manager-backend-nuevo
    env: python
    plan: free
    pythonVersion: "3.11"
    buildCommand: "cd backend && pip install -r requirements-prod.txt"
    startCommand: "cd backend && python run.py"
    healthCheckPath: "/api/health"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        value: postgresql://usuario:password@host:puerto/database
      - key: MICROSOFT_CLIENT_ID
        sync: false
      - key: MICROSOFT_CLIENT_SECRET
        sync: false
      - key: MICROSOFT_TENANT_ID
        sync: false
      - key: MICROSOFT_REDIRECT_URI
        value: https://TU-NUEVO-BACKEND.onrender.com/auth/callback
      - key: OPENAI_API_KEY
        sync: false
      - key: OPENAI_MODEL
        value: gpt-4o-mini
      - key: OPENAI_MAX_TOKENS
        value: "1000"
      - key: OPENAI_TEMPERATURE
        value: "0.3"
```

## 📋 **PASO 2: Crear Cuentas**

### 2.1 Vercel (Frontend)
1. Ve a https://vercel.com
2. Crea una cuenta nueva
3. Conecta tu cuenta de GitHub
4. Importa el repositorio

### 2.2 Render (Backend)
1. Ve a https://render.com
2. Crea una cuenta nueva
3. Conecta tu cuenta de GitHub
4. Crea un nuevo servicio web

### 2.3 PostgreSQL (Base de Datos)
1. En Render, ve a "New" → "PostgreSQL"
2. Configura:
   - **Name**: `email-manager-db-nuevo`
   - **Database**: `email_manager`
   - **User**: `email_manager_user`
   - **Password**: Genera una contraseña segura
3. Copia la **Database URL** (la necesitarás después)

## 📋 **PASO 3: Configurar Variables de Entorno**

### 3.1 Microsoft Azure (Opcional - si quieres nueva app)
1. Ve a https://portal.azure.com
2. Crea una nueva App Registration
3. Configura:
   - **Name**: `Email Manager IA - Nueva`
   - **Redirect URI**: `https://TU-NUEVO-BACKEND.onrender.com/auth/callback`
4. Copia:
   - **Client ID**
   - **Client Secret**
   - **Tenant ID**

### 3.2 OpenAI
1. Ve a https://platform.openai.com
2. Crea una nueva API Key
3. Copia la clave

## 📋 **PASO 4: Desplegar Backend en Render**

### 4.1 Crear Servicio Web
1. En Render, ve a "New" → "Web Service"
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Name**: `email-manager-backend-nuevo`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements-prod.txt`
   - **Start Command**: `cd backend && python run.py`

### 4.2 Configurar Variables de Entorno
En la sección "Environment Variables" de Render, agrega:

```
FLASK_ENV=production
SECRET_KEY=tu-secret-key-muy-largo-y-seguro
JWT_SECRET_KEY=tu-jwt-secret-key-muy-largo-y-seguro
DATABASE_URL=postgresql://usuario:password@host:puerto/database
MICROSOFT_CLIENT_ID=tu-client-id
MICROSOFT_CLIENT_SECRET=tu-client-secret
MICROSOFT_TENANT_ID=tu-tenant-id
MICROSOFT_REDIRECT_URI=https://TU-NUEVO-BACKEND.onrender.com/auth/callback
OPENAI_API_KEY=tu-openai-api-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.3
```

### 4.3 Desplegar
1. Haz clic en "Create Web Service"
2. Espera a que termine el build (5-10 minutos)
3. Copia la URL del backend (ej: `https://email-manager-backend-nuevo.onrender.com`)

## 📋 **PASO 5: Desplegar Frontend en Vercel**

### 5.1 Importar Proyecto
1. En Vercel, ve a "New Project"
2. Importa tu repositorio de GitHub
3. Configura:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 5.2 Configurar Variables de Entorno
En la sección "Environment Variables" de Vercel, agrega:

```
VITE_API_URL=https://TU-NUEVO-BACKEND.onrender.com/api
```

### 5.3 Desplegar
1. Haz clic en "Deploy"
2. Espera a que termine el build (2-3 minutos)
3. Copia la URL del frontend (ej: `https://tu-proyecto.vercel.app`)

## 📋 **PASO 6: Actualizar URLs**

### 6.1 Actualizar Backend
1. En Render, ve a tu servicio web
2. Ve a "Environment"
3. Actualiza `MICROSOFT_REDIRECT_URI` con la URL real del frontend

### 6.2 Actualizar Frontend
1. En Vercel, ve a tu proyecto
2. Ve a "Settings" → "Environment Variables"
3. Actualiza `VITE_API_URL` con la URL real del backend

## 📋 **PASO 7: Verificar Despliegue**

### 7.1 Verificar Backend
```bash
curl https://TU-NUEVO-BACKEND.onrender.com/api/health
```

### 7.2 Verificar Frontend
1. Abre la URL de Vercel en tu navegador
2. Intenta iniciar sesión con Microsoft
3. Verifica que los correos se carguen correctamente

## 📋 **PASO 8: Configurar Dominio Personalizado (Opcional)**

### 8.1 Vercel
1. Ve a "Settings" → "Domains"
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones

### 8.2 Render
1. Ve a "Settings" → "Custom Domains"
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones

## 🎯 **URLs Finales**

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-backend.onrender.com`
- **API**: `https://tu-backend.onrender.com/api`
- **Health Check**: `https://tu-backend.onrender.com/api/health`

## 🔧 **Comandos Útiles**

### Verificar estado local:
```bash
python check_config.py
```

### Iniciar desarrollo:
```bash
python start_dev.py
```

### Verificar rate limits:
```bash
python check_rate_limits.py
```

## ⚠️ **Notas Importantes**

1. **Rate Limits**: La configuración está optimizada para evitar rate limits
2. **Base de Datos**: Se crea automáticamente en Render
3. **Variables de Entorno**: Mantén las claves seguras
4. **Dominios**: Puedes usar dominios personalizados
5. **Monitoreo**: Usa los health checks para verificar el estado

## 🆘 **Solución de Problemas**

### Backend no inicia:
- Verifica las variables de entorno
- Revisa los logs en Render
- Asegúrate de que la base de datos esté configurada

### Frontend no conecta:
- Verifica que `VITE_API_URL` esté configurado
- Asegúrate de que el backend esté funcionando
- Revisa la consola del navegador

### Microsoft no funciona:
- Verifica que `MICROSOFT_REDIRECT_URI` esté correcto
- Asegúrate de que las credenciales estén bien
- Revisa que la app esté configurada en Azure

¡Listo! Sigue estos pasos y tendrás tu aplicación desplegada en ambas plataformas.
