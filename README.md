# Project description
A Http server for account and password Management.

# Outline
* ### Project Structure
* ### Solution Features
* ### Quick Start
* ### APIs Overview

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
# Solution Features

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
# APIs Overview
There are simple descriptions for these two APIs. Please access [Swagger API document](http:localhost:8000/docs) for more details and complete sample requests/responses after running containers following steps above.
### API 1: Create Account

#### Method: `POST`
#### Endpoint: `/api/v1/user`
#### Inputs: JSON payload
| Field       | Type        |  Validation |
| ----------- | ----------- | ----------- |
| username    | `str`       | 8-32 characters
| password    | `str`       | 8-32 characters, and have include at least 1 lowercase letter, 1 uppercase letter, and 1 digit.

#### Output: JSON payload
| Field       | Type        |
| ----------- | ----------- |
| success     | `boolean`   |
| reason      | `str`       |

### API 2: Verify Account and Password
- **If the password verification fails five times, the user should wait one minute before attempting to verify the password again**
- **The log in times will be reset every 10 minutes**
#### Inputs: JSON payload
| Field       | Type        |  Validation |
| ----------- | ----------- | ----------- |
| username    | `str`       | 8-32 characters
| password    | `str`       | 8-32 characters, and have include at least 1 lowercase letter, 1 uppercase letter, and 1 digit.

#### Output: JSON payload
| Field       | Type        |
| ----------- | ----------- |
| success     | `boolean`   |
| reason      | `str`       |