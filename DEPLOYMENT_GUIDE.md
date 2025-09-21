# Guía de Despliegue - Email Manager IA

## Resumen
Esta aplicación se despliega en dos servicios:
- **Frontend**: Vercel (React + Vite)
- **Backend**: Render (Flask + Python)
- **Base de datos**: PostgreSQL (Render)

## URLs de Producción
- Frontend: https://email-manager-ia-testing.vercel.app
- Backend: https://emailmanageriatesting.onrender.com
- API Health: https://emailmanageriatesting.onrender.com/api/health

## Variables de Entorno Requeridas

### Backend (Render)
```bash
FLASK_ENV=production
SECRET_KEY=<generated>
JWT_SECRET_KEY=<generated>
DATABASE_URL=postgresql://email_manager_user:GQWBUD04ZlWyKuisF269nmIS98YtpVnz@dpg-d33fpd3uibrs73ajf8ug-a.oregon-postgres.render.com/email_manager
MICROSOFT_CLIENT_ID=<tu_client_id>
MICROSOFT_CLIENT_SECRET=<tu_client_secret>
MICROSOFT_TENANT_ID=<tu_tenant_id>
MICROSOFT_REDIRECT_URI=https://emailmanageriatesting.onrender.com/auth/callback
OPENAI_API_KEY=<tu_openai_api_key>
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.3
```

### Frontend (Vercel)
```bash
VITE_API_URL=https://emailmanageriatesting.onrender.com/api
```

## Pasos para Despliegue

### 1. Backend en Render
1. Conecta tu repositorio de GitHub a Render
2. Selecciona el archivo `render.yaml` como configuración
3. Configura las variables de entorno en el dashboard de Render
4. El despliegue se iniciará automáticamente

### 2. Frontend en Vercel
1. Conecta tu repositorio de GitHub a Vercel
2. Configura el directorio raíz como `frontend`
3. Configura la variable de entorno `VITE_API_URL`
4. El despliegue se iniciará automáticamente

### 3. Configuración de Microsoft Graph
1. Ve a Azure Portal > App registrations
2. Actualiza la URL de redirección a: `https://emailmanageriatesting.onrender.com/auth/callback`
3. Copia las credenciales a las variables de entorno de Render

### 4. Configuración de OpenAI
1. Obtén tu API key de OpenAI
2. Configúrala en las variables de entorno de Render

## Verificación del Despliegue

### Backend
```bash
# Health check
curl https://emailmanageriatesting.onrender.com/api/health

# Debug info
curl https://emailmanageriatesting.onrender.com/api/debug

# Database health
curl https://emailmanageriatesting.onrender.com/api/health/db
```

### Frontend
1. Visita https://email-manager-ia-testing.vercel.app
2. Verifica que la aplicación carga correctamente
3. Prueba el login con Microsoft

## Características Implementadas

### ✅ Clasificación Automática
- Los correos se clasifican automáticamente al abrir la aplicación
- Usa OpenAI GPT-4o-mini para clasificación inteligente
- Fallback a clasificación basada en reglas si OpenAI falla

### ✅ Sincronización de Correos
- Sincronización automática con Microsoft Graph
- Actualización de estados de lectura
- Clasificación en tiempo real

### ✅ Interfaz de Usuario
- Dashboard tipo Kanban con columnas de prioridad
- Drag & drop para cambiar prioridades
- Modal de respuesta integrado
- Tema claro/oscuro

## Solución de Problemas

### Error de CORS
- Verifica que las URLs estén en `CORS_ORIGINS` en `config.py`

### Error de Base de Datos
- Verifica que `DATABASE_URL` esté configurada correctamente
- Usa `/api/init-db` para inicializar las tablas

### Error de OpenAI
- Verifica que `OPENAI_API_KEY` esté configurada
- Revisa los logs de Render para errores de API

### Error de Microsoft Graph
- Verifica que las credenciales estén correctas
- Asegúrate de que la URL de redirección coincida

## Monitoreo

### Logs de Render
- Ve al dashboard de Render para ver logs en tiempo real
- Busca errores relacionados con OpenAI o Microsoft Graph

### Logs de Vercel
- Ve al dashboard de Vercel para ver logs de build y runtime

## Actualizaciones

### Backend
- Los cambios se despliegan automáticamente al hacer push a la rama principal
- Las migraciones de base de datos se ejecutan automáticamente

### Frontend
- Los cambios se despliegan automáticamente al hacer push a la rama principal
- El build se ejecuta en Vercel

## Costos
- **Render**: Plan gratuito (con limitaciones de sleep)
- **Vercel**: Plan gratuito (con limitaciones de ancho de banda)
- **OpenAI**: Pago por uso (muy económico con GPT-4o-mini)
- **Microsoft Graph**: Gratuito para uso personal/educativo