# Cleanup develop

# venv

```sh
make venv
```

## db

```shell
make up
```

### php my admin

`http://localhost:8080`

## docker

```shell
make down
make down_volume
docker images -qa | xargs docker rmi
```

