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

dev:
```
docker-compose -f docker-compose-dev.yml up --build
```
prod:
```
docker-compose up --build
```

