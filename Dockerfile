FROM python:3.13-alpine3.21

WORKDIR /app

# Copia apenas o requirements.txt primeiro para melhor cache
COPY src/*requirements.txt ./ 

# Atualiza pacotes e instala dependências básicas
RUN apk update && apk add --no-cache \
    git \
    firefox \
    geckodriver

# Instala as dependências do Python
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r dev-requirements.txt

# Copia o restante do código para o container
COPY . /app/

# Define variável de ambiente
ENV ENVIRONMENT=CONTAINER

# Comando para rodar a aplicação
CMD ["python3", "src/scraper/app.py"]