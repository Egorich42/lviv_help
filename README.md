## Site for help refugees in Lviv

Information and tables for free rooms and necessary goods

### Requirements:
 - Docker
 - docker-compose

 for local-development
 - pipenv or pip
 - python 3

### Local development

```
pipenv shell
pipenv install
python run.py
```

### How to run

Before run:

- Add your creds to `init_dev.sql`/`init_prof.sql`:
  - username instead `your_user_name`
  - database name instead `your_database_name_here`
  - password instead of `SET YOUR PASSWORD HERE`

Run production:
```
docker-compose -f docker-compose-prod.yml up --build
```
development:
```
docker-compose up --build
```

