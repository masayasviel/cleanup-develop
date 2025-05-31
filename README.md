# Cleanup develop

## venv

```sh
make venv
```

### activate

```sh
source .venv/bin/activate
deactivate
```

## Docker

```shell
make up
```

### migrate

```sh
# create migrate file
docker-compose run web python manage.py makemigrations defaultdb
# migrate
docker-compose run web python manage.py migrate
```

### fixture

```sh
docker-compose run web python manage.py load_fixtures
```

### php my admin

`http://localhost:8080`

### down

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
# IAMロール作成系は下記オプションをつける
--capabilities CAPABILITY_NAMED_IAM
```
