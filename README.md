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

### fixture

```sh
docker-compose run web python manage.py load_fixtures
```

### php my admin

`http://localhost:8080`

## docker

```shell
make down
make down_volume
docker images -qa | xargs docker rmi
```

## CFn

```sh
cd infrastructure
chmod 777 create.sh update.sh
editor ./params/{file name}
# 拡張子は含めない
./create.sh {yml file name}
./update.sh {yml file name}
```
