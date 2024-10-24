# Exemplo de Dockerfile
FROM python:3.13-slim-bullseye

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN apt-get update -y && apt-get install build-essential python-dev python3-dev -y
RUN pip install -r requirements.txt
RUN pip install --upgrade setuptools wheel
# Garantir que o script start.sh tenha permissão de execução
RUN chmod +x /app/start.sh

# Definir o comando de inicialização
CMD ["/app/start.sh"]
