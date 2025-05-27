set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Recoger archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate

# Instalar dependencias de npm para Tailwind
cd theme/static_src
npm install

# Volver a raíz del proyecto
cd ../../

# Ejecutar build de Tailwind (ahora rimraf ya existe)
python manage.py tailwind build
