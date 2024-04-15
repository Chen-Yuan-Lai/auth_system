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
│   │   ├── schemas.py  # pydantic models
│   │   ├── models.py   # db models
│   │   ├── dependencies.py # db connection dependencies
│   │   ├── services.py
│   │   ├── security.py
│   │   └──limiter.lua
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── exceptions.py  # global exceptions
│   ├── database.py    # db connection
│   ├── redis_pool.py  # redis connection
│   ├── config.py      # global configs
│   └── log.py         # customized logger
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
# Solution Details
1. Implement two **RESTful HTTP APIs** for creating and verifying an account and password.
2. Use **Python** and **FastAPI** framework to implement the solution.
3. Use Pydantic schema for input validation.
4. Centralized handling predictable and unpredictable error with customized **middleware** and **exception handler**.
5. Use **PostgreSQL** for data storage
6. Use **Redis** to implement log in retry logic. And run the **lua script** for atomic pipeline.
7. Package the solution in a Docker container and push it to **Docker Hub**.
8. Provide a comprehensive API document with **Swagger UI**. 


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
   docker-compose -f docker-compose-prod.yml up -d

   # New CLI
   docker compose -f docker-compose-prod.yml up -d
   ```
   `-d`: run containers in the background
5. ### Send a POST request for signing up
    ```bash
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
            "username": "Ian",
            "password": "Aa1234567"
        }' \
    http://localhost:8000/api/v1/user
    ```
6. ### Send a POST request for signing in
   ```bash
   curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
            "username": "Ian",
            "password": "Aa1234567"
        }' \
    http://localhost:5000/api/signIn
   ```
7. ### Stop all containers
    ```bash
    # Old CLI
    docker-compose -f docker-compose-prod.yml down -v

    # New CLI
    docker compose -f docker-compose-prod.yml down -v
    ```
    `-v`: delete all volumes
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
- If the password verification fails five times, the user should wait one minute before attempting to verify the password again
- The log in times will be reset every 10 minutes
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


