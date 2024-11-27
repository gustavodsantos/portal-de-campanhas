# Usar a imagem base do Python
FROM python:3.12

# Instalar dependências de sistema necessárias
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos pyproject.toml e poetry.lock da raiz do projeto para o contêiner
COPY pyproject.toml /app/
COPY poetry.lock /app/

# Instalar as dependências sem o pacote raiz
RUN poetry install --no-root --without dev

# Copiar o restante do código do projeto para o contêiner
COPY ./ /app/

# Expor a porta que o Django vai usar
EXPOSE 8000

# Comando para rodar o Django
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
