# ✅ Checklist de Despliegue - Nueva Cuenta

## 📋 **PREPARACIÓN (✅ Completado)**
- [x] Código optimizado para rate limits
- [x] Archivos de configuración actualizados
- [x] Scripts de verificación creados
- [x] Backup de archivos originales

## 🔐 **PASO 1: CREAR CUENTAS**

### 1.1 Render (Backend + Base de Datos)
- [ ] Ir a https://render.com
- [ ] Crear cuenta nueva
- [ ] Conectar con GitHub
- [ ] Crear base de datos PostgreSQL:
  - [ ] Nombre: `email-manager-db-nuevo`
  - [ ] Usuario: `email_manager_user`
  - [ ] Contraseña: Generar una segura
  - [ ] Copiar **Database URL**

### 1.2 Vercel (Frontend)
- [ ] Ir a https://vercel.com
- [ ] Crear cuenta nueva
- [ ] Conectar con GitHub

### 1.3 Microsoft Azure (Opcional)
- [ ] Ir a https://portal.azure.com
- [ ] Crear nueva App Registration:
  - [ ] Nombre: `Email Manager IA - Nueva`
  - [ ] Redirect URI: `https://tu-backend-nuevo.onrender.com/auth/callback`
  - [ ] Copiar **Client ID**, **Client Secret**, **Tenant ID**

### 1.4 OpenAI
- [ ] Ir a https://platform.openai.com
- [ ] Crear nueva API Key
- [ ] Copiar la clave

## 🚀 **PASO 2: DESPLEGAR BACKEND EN RENDER**

### 2.1 Crear Servicio Web
- [ ] En Render: "New" → "Web Service"
- [ ] Conectar repositorio de GitHub
- [ ] Configurar:
  - [ ] **Name**: `email-manager-backend-nuevo`
  - [ ] **Environment**: `Python 3`
  - [ ] **Build Command**: `cd backend && pip install -r requirements-prod.txt`
  - [ ] **Start Command**: `cd backend && python run.py`

### 2.2 Configurar Variables de Entorno
- [ ] `FLASK_ENV` = `production`
- [ ] `SECRET_KEY` = `tu-secret-key-muy-largo-y-seguro`
- [ ] `JWT_SECRET_KEY` = `tu-jwt-secret-key-muy-largo-y-seguro`
- [ ] `DATABASE_URL` = `postgresql://usuario:password@host:puerto/database`
- [ ] `MICROSOFT_CLIENT_ID` = `tu-client-id`
- [ ] `MICROSOFT_CLIENT_SECRET` = `tu-client-secret`
- [ ] `MICROSOFT_TENANT_ID` = `tu-tenant-id`
- [ ] `MICROSOFT_REDIRECT_URI` = `https://tu-backend-nuevo.onrender.com/auth/callback`
- [ ] `OPENAI_API_KEY` = `tu-openai-api-key`
- [ ] `OPENAI_MODEL` = `gpt-4o-mini`
- [ ] `OPENAI_MAX_TOKENS` = `1000`
- [ ] `OPENAI_TEMPERATURE` = `0.3`

### 2.3 Desplegar
- [ ] Hacer clic en "Create Web Service"
- [ ] Esperar build (5-10 minutos)
- [ ] Copiar URL del backend: `https://tu-backend-nuevo.onrender.com`

## 🎨 **PASO 3: DESPLEGAR FRONTEND EN VERCEL**

### 3.1 Importar Proyecto
- [ ] En Vercel: "New Project"
- [ ] Importar repositorio de GitHub
- [ ] Configurar:
  - [ ] **Framework Preset**: `Vite`
  - [ ] **Root Directory**: `frontend`
  - [ ] **Build Command**: `npm run build`
  - [ ] **Output Directory**: `dist`

### 3.2 Configurar Variables de Entorno
- [ ] `VITE_API_URL` = `https://tu-backend-nuevo.onrender.com/api`

### 3.3 Desplegar
- [ ] Hacer clic en "Deploy"
- [ ] Esperar build (2-3 minutos)
- [ ] Copiar URL del frontend: `https://tu-proyecto.vercel.app`

## 🔗 **PASO 4: ACTUALIZAR URLs**

### 4.1 Actualizar Backend
- [ ] En Render: Ir a tu servicio web
- [ ] Ir a "Environment"
- [ ] Actualizar `MICROSOFT_REDIRECT_URI` con URL real del frontend

### 4.2 Actualizar Frontend
- [ ] En Vercel: Ir a tu proyecto
- [ ] Ir a "Settings" → "Environment Variables"
- [ ] Actualizar `VITE_API_URL` con URL real del backend

## ✅ **PASO 5: VERIFICAR DESPLIEGUE**

### 5.1 Verificar Backend
- [ ] Abrir: `https://tu-backend-nuevo.onrender.com/api/health`
- [ ] Debe mostrar: `{"status": "healthy"}`

### 5.2 Verificar Frontend
- [ ] Abrir: `https://tu-proyecto.vercel.app`
- [ ] Debe cargar la página de login

### 5.3 Verificar Integración
- [ ] Hacer clic en "Iniciar Sesión con Microsoft"
- [ ] Completar autenticación
- [ ] Verificar que se carguen los correos
- [ ] Verificar que la clasificación automática funcione

## 🔧 **PASO 6: CONFIGURACIÓN ADICIONAL**

### 6.1 Dominio Personalizado (Opcional)
- [ ] **Vercel**: "Settings" → "Domains" → Agregar dominio
- [ ] **Render**: "Settings" → "Custom Domains" → Agregar dominio

### 6.2 Monitoreo
- [ ] Configurar alertas en Render
- [ ] Configurar alertas en Vercel
- [ ] Revisar logs regularmente

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### Backend no inicia:
- [ ] Verificar variables de entorno
- [ ] Revisar logs en Render
- [ ] Verificar que la base de datos esté configurada

### Frontend no conecta:
- [ ] Verificar que `VITE_API_URL` esté configurado
- [ ] Verificar que el backend esté funcionando
- [ ] Revisar consola del navegador

### Microsoft no funciona:
- [ ] Verificar que `MICROSOFT_REDIRECT_URI` esté correcto
- [ ] Verificar credenciales en Azure
- [ ] Verificar que la app esté configurada correctamente

## 📊 **URLs FINALES**

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-backend-nuevo.onrender.com`
- **API**: `https://tu-backend-nuevo.onrender.com/api`
- **Health Check**: `https://tu-backend-nuevo.onrender.com/api/health`

## 🎯 **COMANDOS ÚTILES**

```bash
# Verificar configuración local
python check_config.py

# Verificar rate limits
python check_rate_limits.py

# Verificar despliegue
python verify_deployment.py

# Iniciar desarrollo local
python start_dev.py
```

## 📝 **NOTAS IMPORTANTES**

1. **Rate Limits**: Configuración optimizada para evitar rate limits
2. **Base de Datos**: Se crea automáticamente en Render
3. **Variables de Entorno**: Mantener las claves seguras
4. **Dominios**: Puedes usar dominios personalizados
5. **Monitoreo**: Usar health checks para verificar estado

---

**¡Listo! Sigue este checklist paso a paso y tendrás tu aplicación desplegada correctamente.**
