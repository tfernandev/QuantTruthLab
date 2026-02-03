# Pasos para subir a GitHub y desplegar en Render

El repositorio Git local ya está listo (rama `main`, commit inicial hecho). Solo faltan estos pasos que debes hacer en el navegador y en la terminal.

---

## 1. Crear el repositorio en GitHub

1. Entra en **https://github.com/new**
2. **Repository name:** `QuantTruthLab`
3. **Visibility:** Public (o Private si prefieres)
4. **No** marques "Add a README" (ya tienes uno en el proyecto)
5. Clic en **Create repository**

---

## 2. Conectar tu proyecto local y subir el código

En la terminal, desde la carpeta del proyecto (`QuantTruthLab`), ejecuta (sustituye `TU_USUARIO` por tu usuario de GitHub):

```powershell
cd "c:\Users\Usuario\source\repos\QuantTruthLab"
git remote add origin https://github.com/TU_USUARIO/QuantTruthLab.git
git push -u origin main
```

Si GitHub te pide autenticación, usa tu usuario y un **Personal Access Token** (no la contraseña). Crear token: GitHub → Settings → Developer settings → Personal access tokens.

---

## 3. Desplegar en Render

### Backend (Web Service)

1. Entra en **https://dashboard.render.com**
2. **New +** → **Web Service**
3. Conecta GitHub si no lo has hecho y elige el repo **QuantTruthLab**
4. Configura:
   - **Name:** `quanttruthlab-api`
   - **Branch:** `main`
   - **Root Directory:** *(dejar vacío)*
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. **Create Web Service** y espera el deploy (~3–5 min).
6. Anota la URL del backend (ej. `https://quanttruthlab-api.onrender.com`).

### Frontend (Static Site)

1. En el Dashboard: **New +** → **Static Site**
2. Mismo repo **QuantTruthLab**
3. Configura:
   - **Name:** `quanttruthlab`
   - **Branch:** `main`
   - **Root Directory:** `web_ui`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. En **Environment** añade:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://quanttruthlab-api.onrender.com/api` (usa tu URL real de backend)
5. **Create Static Site** y espera el deploy (~2–4 min).

---

## 4. Comprobar

- Backend: `https://quanttruthlab-api.onrender.com/` → debe devolver `{"status":"ok","system":"Quant Platform Ready"}`
- Frontend: abre la URL del sitio estático y verifica que diga "Truth Engine Conectado" y que un backtest de prueba funcione.

A partir de aquí, cada `git push origin main` volverá a desplegar backend y frontend en Render.
