FROM python:3.13-alpine3.21

WORKDIR /app

# Copia o arquivo de requisitos
COPY src/requirements.txt ./

# Atualiza pacotes e instala dependências básicas
RUN apk update && apk add --no-cache \
    git \
    firefox \
    geckodriver
# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . /app/
ENV ENVIRONMENT=CONTAINER

# Comando para rodar a aplicação
CMD ["python3", "src/scraper/app.py"]
