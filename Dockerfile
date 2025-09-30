FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Install netcat for the entrypoint script
RUN apt-get update && apt-get install -y netcat-openbsd

COPY entrypoint.sh . 
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
