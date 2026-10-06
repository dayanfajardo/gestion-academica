# Imagen no tan pesada de python
FROM python:3.10-slim

# Creamos la carpeta dentro del contenedor
WORKDIR /app

# Copiamos las dependencias de nuestra app
COPY requirements.txt .

# Instalamos librerias
RUN pip install --no-cache-dir -r requirements.txt

# Tomamos fotografia del proyecto
COPY . .

# Exponemos el puerto
EXPOSE 5001

# Comando para arrancar nuestro servicio
CMD ["python", "app.py"]
