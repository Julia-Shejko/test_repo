# <span style="color:OliveDrab">Support service application</span>


## <span style="color:DarkOliveGreen">Adjust the application</span>

### Create '.env' file based on '.env.default'
```bash
cp .env.default .env
```


### Install deps
```bash
pipenv sync --dev

# Activate the environment
pipenv shell
```


### Collect static files
```bash
python src/manage.py collectstatic
```


## Run using Docker Compose
```bash
docker-compose up -d
```


### Useful commands
```bash
# Build images
docker-compose build

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# Check containers status
docker-compose ps


## Logs

# get all logs
docker-compose logs

# get specific logs
docker-compose logs app

# get limited logs
docker-compose logs --tail 10 app

# get flowed logs
docker-compose logs -f app
```





- ### Frameworks:
    - Django
    - Django REST framework    

- ### Libraries:
    - pydantic
    - requests
    - djangorestframework-simplejwt
    - psycopg2-binary
    - django-stubs
    - djangorestframework-stubs
    - gunicorn

## <span style="color:DarkOliveGreen">Code quality tools</span>
- ## Validation with CircleCI

- ### Linter:
    - flake8
- ### Code formatters:
    - black
    - isort
- ### Type checker:
    - mypy


## <span style="color:DarkOliveGreen">Application description</span>

# Database

```mermaid
erDiagram
    Users {
        int id
        string frist_name
        string last_name
        string email
        string password
        bool is_staff
        bool is_active
        string role
        datetime created_at
        datetime updated_at
    }
    Tickets {
        int id
        int customer_id
        int manager_id
        string header
        text body
        datetime created_at
        datetime updated_at
    }
    Comments {
        int id
        int prev_comment_id
        int user_id
        int ticket_id
        text body
        datetime created_at
        datetime updated_at
    }

    Users ||--o{ Tickets : ""
    Tickets ||--o{ Comments : ""
    Comments ||--o{ Comments : ""
```
