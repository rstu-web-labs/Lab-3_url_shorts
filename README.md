# Lab-3_url_shorts

## Последовательность выполнения команд для успешного запуска

Заполните файл `.env`

```shell
cp .example.env .env
```

Для локальной разработки запустите:

```shell
docker-compose --env-file .env -f infra/docker-compose.local.yaml up --build
```
