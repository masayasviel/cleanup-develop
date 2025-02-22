# Cleanup develop

## venv

```sh
make venv
```

## activate

```sh
source .venv/bin/activate
deactivate
```

## db

```shell
make up
```

### migrate

```sh
docker-compose run web python manage.py makemigrations defaultdb
docker-compose run web python manage.py migrate
```

### php my admin

`http://localhost:8080`

## docker

```shell
make down
make down_volume
docker images -qa | xargs docker rmi
```

