# Plan de Despliegue: QuantTruthLab en Render

**Objetivo:** Publicar frontend (React) y backend (FastAPI) en Render con deploys automáticos desde GitHub.

**URLs finales:**
- Backend: `https://quanttruthlab-api.onrender.com`
- Frontend: `https://quanttruthlab.onrender.com`

---

## Pre-requisitos

- [ ] Cuenta en [GitHub](https://github.com)
- [ ] Cuenta en [Render](https://render.com)
- [ ] Git instalado localmente
- [ ] Proyecto funcionando en local (backend + frontend)

---

## Fase 1: Preparar el repositorio

### 1.1 Verificar dependencias

Añadir `scipy` a `requirements.txt` (usado por el backtest):

```
scipy>=1.10.0
```

### 1.2 Crear/verificar .gitignore

Asegurarse de que **NO** se ignoren los datos Parquet (necesarios para el backend):

```
# Incluir data/processed/*.parquet en el repo
# NO poner: data/processed/ en .gitignore
```

Sí ignorar: `__pycache__`, `.venv`, `node_modules`, `.env`, logs, etc.

### 1.3 Variables de entorno del frontend

El frontend ya usa `VITE_API_URL` (ver `App.tsx`). En Render la configurarás al desplegar.

### 1.4 Subir a GitHub

```bash
# Si aún no tienes repo en GitHub
git init
git add .
git commit -m "Initial commit - QuantTruthLab"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/QuantTruthLab.git
git push -u origin main
```

---

## Fase 2: Desplegar el Backend en Render

### 2.1 Crear Web Service

1. Entra a [Render Dashboard](https://dashboard.render.com)
2. **New +** → **Web Service**
3. Conecta tu cuenta de GitHub y selecciona el repositorio `QuantTruthLab`

### 2.2 Configurar el Backend

| Campo | Valor |
|-------|-------|
| **Name** | `quanttruthlab-api` |
| **Region** | Oregon (US West) o el más cercano |
| **Branch** | `main` |
| **Root Directory** | *(vacío – raíz del repo)* |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` |

### 2.3 Variables de entorno (Backend)

No son obligatorias para el arranque básico. Opcionales:

| Key | Value | Notas |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11` | Si quieres fijar versión |

### 2.4 Instance Type

- **Free** (tiene spin-down tras ~15 min sin uso)

### 2.5 Crear el servicio

- Clic en **Create Web Service**
- Espera a que termine el deploy (3–5 min)
- Anota la URL: `https://quanttruthlab-api.onrender.com`

### 2.6 Comprobar que funciona

Abre en el navegador: `https://quanttruthlab-api.onrender.com/`  
Debería devolver: `{"status":"ok","system":"Quant Platform Ready"}`

Prueba también: `https://quanttruthlab-api.onrender.com/api/discovery/`

---

## Fase 3: Desplegar el Frontend en Render

### 3.1 Crear Static Site

1. En Render Dashboard: **New +** → **Static Site**
2. Conecta el mismo repositorio `QuantTruthLab`

### 3.2 Configurar el Frontend

| Campo | Valor |
|-------|-------|
| **Name** | `quanttruthlab` |
| **Branch** | `main` |
| **Root Directory** | `web_ui` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `dist` |

### 3.3 Variables de entorno (Frontend)

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://quanttruthlab-api.onrender.com/api` |

*(Sustituye por tu URL real de backend si cambiaste el nombre)*

### 3.4 Crear el sitio

- Clic en **Create Static Site**
- Espera el deploy (2–4 min)
- URL final: `https://quanttruthlab.onrender.com`

### 3.5 Comprobar

- Abre la URL del frontend
- Debería mostrar "Truth Engine Conectado" si el backend responde
- Ejecuta un backtest de prueba

---

## Fase 4: Deploys automáticos desde GitHub

### 4.1 Configuración por defecto

Render hace **auto-deploy** cuando:
- Haces `git push` a la rama `main`
- Se detecta un nuevo commit

No hace falta configurar nada extra: ya está activo.

### 4.2 Comportamiento

| Evento | Backend | Frontend |
|--------|---------|----------|
| Push a `main` | Redeploy automático | Redeploy automático |
| Push a otra rama | No se despliega | No se despliega |
| Tiempo de deploy | ~3–5 min | ~2–4 min |

### 4.3 Notificaciones (opcional)

En cada servicio → **Settings** → **Notifications**:
- Activa emails cuando un deploy falle

---

## Fase 5: Checklist final

- [ ] Backend responde en `https://quanttruthlab-api.onrender.com/`
- [ ] Discovery API responde: `/api/discovery/`
- [ ] Frontend carga en `https://quanttruthlab.onrender.com`
- [ ] Status "Conectado" en la UI
- [ ] Backtest de prueba ejecutado correctamente
- [ ] Push a `main` dispara redeploy en ambos servicios

---

## Resolución de problemas

### Backend no arranca

- Revisa **Logs** en Render
- Verifica que `data/processed/` con los Parquet esté en el repo
- Comprueba que `scipy` esté en `requirements.txt`

### Frontend muestra "Offline"

- Comprueba que `VITE_API_URL` apunte a la URL correcta del backend (sin barra final en `/api`)
- El backend en Free tier puede tardar ~30 s en “despertar” tras inactividad

### CORS

El backend ya tiene `allow_origins=["*"]`. Si añades dominio propio, conviene restringir:

```python
allow_origins=[
    "https://quanttruthlab.onrender.com",
    "https://tudominio.com"
]
```

### Datos Parquet

Si los archivos `data/processed/*.parquet` son grandes (>100 MB), considera:
- Usar [Git LFS](https://git-lfs.github.com), o
- Reducir el rango de fechas de los datos

---

## Resumen de URLs y comandos

| Qué | Dónde |
|-----|-------|
| Backend API | `https://quanttruthlab-api.onrender.com` |
| Frontend | `https://quanttruthlab.onrender.com` |
| Deploy backend | `git push origin main` |
| Deploy frontend | `git push origin main` |

---

*Documento generado para QuantTruthLab — Despliegue en Render*
