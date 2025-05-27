set -o errexit

pip install -r requierments.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py tailwind build