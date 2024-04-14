# Project description
A Http server for account and password Management.

# Outline
* ### Project Structure
* ### Quick Start
* ### APIs

# Project Structure
```
auth_system
├── myAlembic/
├── src
│   ├── auth
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py  
│   │   ├── models.py  
│   │   ├── dependencies.py
│   │   ├── services.py
│   │   ├── security.py
│   │   └──limiter.lua
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── exceptions.py  
│   ├── database.py  
│   ├── redis_pool.py  
│   ├── config.py  
│   └── log.py  
├── .env
│   ├── .db.env
│   ├── .dev.env  
│   └── .prod.env
│ 
├── .gitignore
├── .pre-commit-config.yaml
├── .dockerignore
├── pyproject.toml
├── docker-compose-prod.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── alembic.ini
```
# Quick Start
1. ### Clone the project
    ```bash
    git clone https://github.com/Chen-Yuan-Lai/auth_system.git
    ```
2. ### Enter the project
   ```bash
   cd auth_system
   ```
3. ### Rename a folder that store environment variables 
    ```bash
    mv .env.example .env
    ```
4. ### Run docker compose
   ```bash
   # Old CLI
   docker-compose -f docker-compose-prod.yml down -v

   # New CLI
   docker compose -f docker-compose-prod.yml down -v
   ```
# APIs
