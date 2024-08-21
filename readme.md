# Agendador de Mensagens com Flask

Este projeto é uma aplicação web desenvolvida com Flask para agendar e gerenciar mensagens que serão enviadas para grupos do Google Chats. A aplicação permite criar, editar, excluir e visualizar mensagens agendadas, além de gerenciar webhooks associados a essas mensagens.

## Funcionalidades

- **Gerenciamento de Mensagens:**
  - Cadastrar mensagens com horário e dias da semana para envio.
  - Editar mensagens agendadas.
  - Excluir mensagens.
  - Visualizar mensagens agendadas.

- **Gerenciamento de Webhooks:**
  - Cadastrar e editar webhooks.
  - Associar webhooks a mensagens para envio.

## Tecnologias Utilizadas

- **Flask**: Framework para desenvolvimento web em Python.
- **SQLAlchemy**: ORM para gerenciamento de banco de dados.
- **SQLite**: Banco de dados leve para persistência de dados.
- **APScheduler**: Biblioteca para agendamento de tarefas.
- **Requests**: Biblioteca para envio de requisições HTTP.

## Configuração do Ambiente

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/usuario/repositorio.git
   cd repositorio


2. **Crie e Ative um Ambiente Virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Windows: venv\Scripts\activate


3. **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt

4. **Crie o Banco de Dados:**

    O banco de dados SQLite será criado automaticamente ao iniciar a aplicação pela primeira vez. No entanto, você pode forçar a criação do banco de dados com:

    ```bash
    flask shell
    >>> from app import db
    >>> db.create_all()

5. **Configure as Credenciais do Google Chats:**

    Certifique-se de ter o arquivo de credenciais JSON do Google Chats e coloque-o no diretório credential/ como bot-monitor.json.


6. **Inicie a Aplicação:**

    ```bash
    flask run

    A aplicação estará disponível em http://127.0.0.1:5000/.

7. **Rotas da Aplicação:**


- /: Página inicial que lista todas as mensagens agendadas e permite editar e excluir mensagens.

- /schedule_message: Endpoint para agendar novas mensagens.

- /edit/<int:message_id>: Página para editar uma mensagem existente.

- /delete/<int:message_id>: Endpoint para excluir uma mensagem.

- /webhooks: Página para gerenciar webhooks (criar, editar e visualizar).

8. **Contribuição**

    1. Faça um Fork do Repositório
    2. Crie uma Branch para suas alterações
    3. Faça o Commit das suas alterações
    4. Envie um Pull Request

9. **Licença**

    Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes..