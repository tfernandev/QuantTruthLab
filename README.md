# Quant Truth Lab

Un "Laboratorio de Verdad" cuantitativo diseñado para auditar, estresar y diagnosticar estrategias de trading con rigor estadístico.

Este proyecto permite simular estrategias algorítmicas sobre datos reales de criptomonedas (BTC/USDT, ETH/USDT) teniendo en cuenta comisiones, slippage y gestión de riesgo, con un enfoque en la **honestidad estadística** (P-Values, comparación contra azar, análisis de robustez).

## 🚀 Requisitos Previos

*   **Python 3.10+**
*   **Node.js 20+** (Requerido por Vite)
*   Windows/Linux/Mac

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPO>
cd QuantTruthLab
```

### 2. Configurar el Backend (Python)
Se recomienda usar un entorno virtual.

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.\.venv\Scripts\Activate.ps1

# Activar entorno (Mac/Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar el Frontend (React)
```bash
cd web_ui
# Crear archivo de entorno
echo VITE_API_URL=http://localhost:8000/api > .env

# Instalar dependencias
npm install
```

## ▶️ Ejecución

### 1. Iniciar el Backend (Terminal 1)
Desde la raíz del proyecto (`QuantTruthLab`):
```bash
python -m uvicorn backend.app.main:app --reload --port 8000 --host 0.0.0.0
```
El "Truth Engine" estará activo en `http://localhost:8000`.

### 2. Iniciar el Frontend (Terminal 2)
Desde la carpeta `web_ui`:
```bash
npm run dev
```
La interfaz estará accesible en `http://localhost:5173`.

## 🧪 Tests Unitarios

Para validar la integridad del motor de simulación y las estrategias:

```bash
# Desde la raíz del proyecto
pytest
```

## 🏗️ Estructura del Proyecto

*   `backend/`: API FastAPI y lógica de orquestación.
*   `core/`: El corazón del sistema (Broker, Estrategias, Métricas).
    *   `strategies/`: Implementación de lógica de trading (RSI, MACD, etc.).
    *   `execution/`: Motor de simulación de órdenes.
*   `web_ui/`: Frontend en React + Vite + Tailwind CSS.
*   `data/`: Almacenamiento local de datos (Parquet).

## ⚠️ Disclaimer
Esta herramienta es educativa. No garantiza ganancias futuras. El trading de criptomonedas conlleva un alto riesgo de pérdida de capital.
