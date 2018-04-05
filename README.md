# Simple Honey
This creates a simple webserver which acts as a honey pot, that is very easy to control.
It accepts POST and GET requests with web administration and easy customization.
Currently installs at around 256 MB.

## Example using docker
```
docker build -t simple-honey .
docker run \
    --name=simple-honey \
    -e SH_DB_HOST="HOST" \
    -e SH_DB_USER="USER" \
    -e SH_DB_PASS="PASS" \
    -e VIRTUAL_HOST='simpe-honey.example.com' \
    -td \
    --restart=always \
    simple-honey
```

## Environmental Vars
ENV Var | Default | Description
--- | --- | ---
`SH_DB_ENGINE` | postgresql | Database engine type
`SH_DB_USER` | *None* | Database user name
`SH_DB_PASS`  | *None* |  Database user password
`SH_DB_HOST` | some-postgres | Database host
`SH_DB_PORT` | 5432 | Database host
`SH_DB_NAME`  | simple_honey | Database name
`SH_ADMIN_URL` | 'the-admin' | URI for admin
`VIRTUAL_HOST`  |  *None*  | URL the Nginx proxy will route to this container
`TZ` | 'America/Denver' | Timezone for the container to run in


## Volume Mounts
 Path | Purpose
--- | ---
/opt/simple-honey | Code base path
/data/hosted_files | Put files here to make available to a client
/data/logs | Logs from the webserver
