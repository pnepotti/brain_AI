FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# Dar permisos de ejecución al script de entrada
RUN chmod +x ./scripts/entrypoint.sh

# Exponer puerto
EXPOSE 8000

# Establecer el script como el punto de entrada
ENTRYPOINT ["./scripts/entrypoint.sh"]