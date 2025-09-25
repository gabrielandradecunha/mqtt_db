# Broker to database

Script para extrair dados de um broker MQTT e inserir em banco de dados relacional.

## Visão geral

Este projeto permite conectar-se a um broker MQTT, assinar tópicos específicos, receber mensagens e persistir esses dados em um banco de dados (por exemplo, PostgreSQL). A ideia é automatizar o fluxo de dados vindos de sensores, dispositivos IoT ou qualquer fonte que publique no MQTT.

## Estrutura do repositório

<img width="577" height="430" alt="image" src="https://github.com/user-attachments/assets/c4ea1afa-2bcf-4e0c-9eff-eb51c5de434c" />


### Arquivos principais

- `main.py` — Ponto de entrada da aplicação.
- `router.py` — Lida com roteamento das mensagens recebidas (por tópico, tipo, etc.).
- `database.py` — Camada de abstração para conexão, inserção e operações no banco de dados.
- `init.sql` — Script SQL inicial para criar tabelas, funções e triggers necessárias no banco.
- `Dockerfile` / `docker-compose.yml` — Para containerização da aplicação + serviços auxiliares (ex: banco de dados, broker MQTT).
- `.env.example` — Modelo de variáveis de ambiente que a aplicação precisa (host, porta, usuário, senha do banco, credenciais MQTT etc.).

### Passos iniciais

1. **Copie o arquivo `.env.example` para `.env`** e configure suas variáveis:

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=meu_usuario
   DB_PASSWORD=senha
   DB_NAME=mqtt_db

   MQTT_HOST=broker.exemplo.com
   MQTT_PORT=1883
   MQTT_USERNAME=usuario_mqtt
   MQTT_PASSWORD=senha_mqtt
   MQTT_TOPICS=topico1,topico2


2. Inicialize o banco de dados
Execute o script `init.sql` no seu banco para criar as tabelas, triggers e funções necessárias.

3. Instale as dependências
   ```bash
   pip install -r requirements.txt
   

5. Execute a aplicação (considerando que já tenha um banco)

   ```bash
   python3 .















   







