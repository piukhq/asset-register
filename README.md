# POC Asset register

```
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
psql "host=localhost port=5432 dbname=postgres user=postgres"
CREATE DATABASE asset_register;
```