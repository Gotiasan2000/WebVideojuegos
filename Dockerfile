FROM python:3.9-slim-bookworm

WORKDIR /code

# Copia el archivo de requisitos
COPY ./requirements.txt /code/requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia el código de la aplicación
COPY . /code/

# Exponer el puerto 8000 (en vez de 80, que es el puerto por defecto de FastAPI)
EXPOSE 8000

# Usar uvicorn para correr la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
