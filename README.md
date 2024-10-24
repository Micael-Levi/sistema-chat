# Sistema Chat

Este é o projeto de um sistema de chat utilizando Django, Django Rest Framework, Channels, Redis, e WebSockets. O projeto é configurado para rodar em contêineres Docker, usando PostgreSQL como banco de dados e Redis para comunicação em tempo real.

## Instruções para rodar o projeto

### Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Passos para rodar o projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/sistema_chat.git
   cd sistema_chat
   ```
   
2. Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:
   
   ```bash
    # Configuração Django
    SECRET_KEY=
    DEBUG=
    
    # Configuração banco
    POSTGRES_DB=
    POSTGRES_HOST=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_PORT=
    
    # Portas expostas
    EXPOSE_PORT=
    EXPOSE_PORT_WS=
    EXPOSE_DATABASE_PORT=
   ```
   
3. Execute o Docker Compose para levantar os contêineres:
   
  ```bash
   docker-compose up --build -d
  ```

### Decisões de Desenvolvimento

-  A aplicação foi desenvolvida inteiramente em Python, utilizando Django e Django Rest Framework, escolhidos por sua robustez, alta produtividade e ampla adoção na comunidade;
- Para implementar o WebSocket, foi utilizada a biblioteca Django Channels, e o Redis foi escolhido como backend para gerenciar os canais de comunicação, devido à sua velocidade, eficiência e excelente capacidade de escalabilidade;
- Visando a produção, foi configurado o uWSGI como servidor HTTP para rodar a aplicação Django, enquanto o Uvicorn gerencia as conexões WebSocket, garantindo um ambiente de execução eficiente e confiável para diferentes tipos de tráfego;
- Tanto o Redis quanto o banco de dados PostgreSQL foram configurados no docker-compose para facilitar a execução do projeto durante o desenvolvimento. No entanto, para um ambiente de produção, o ideal seria hospedar o banco de dados em um servidor dedicado ou em uma infraestrutura externa mais adequada;
- O projeto foi modularizado em apps independentes, cada um responsável pela implementação de funcionalidades específicas de um mesmo fluxo, o que facilita a manutenção, escalabilidade e testes individuais de cada módulo.

### Rodando os Testes

1. Acesse o contêiner principal do Django:

   ```bash
   docker-compose exec web sh
   ```
   
2. Dentro do contêiner, rode os testes com o comando:

   ```bash
   pytest
   ```
