# InterficieApp
Aplicación móvil para gestión de gimnasios con Django REST (Backend) y Quasar Framework (Frontend)

## 📋 Requisitos Previos

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js 16.x+](https://nodejs.org/)
- [PostgreSQL 13+](https://www.postgresql.org/download/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Poetry](https://python-poetry.org/docs/#installation) (Opcional)

## 🚀 Configuración Inicial

### 1. Clonar repositorio
```bash
git clone https://github.com/tu-usuario/gym-management-app.git #Nombres por Cambiar
cd gym-management-app

# Entrar en directorio backend
cd backend

# Instalar dependencias (Usar poetry o pip)
poetry install  # Opción recomendada
# ó
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Entrar en directorio frontend
cd ../frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env