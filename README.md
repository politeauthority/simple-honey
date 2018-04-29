# Simple Honey
This creates a simple webserver which acts as a honey pot, that is very easy to control.
It accepts POST and GET requests with web administration and easy customization.
Currently installs at around 256 MB.

## Example using docker
```
docker build -t simple-honey .
docker run \
    --name=simple-honey \
    -e SH_DB_USER="root" \
    -e SH_DB_PASS="RdYy0aM2GOzGWRgL" \
    -e SH_ADMIN_URL="xFPL30NcqhNwrWDY" \
    -e SH_ADMIN_PASS="Mj5UO6dEXtihNalZ" \
    -e VIRTUAL_HOST='example.com,*.other-example.com' \
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
`SH_ADMIN_URL` | the-admin | Your chosen URI for admin
`SH_ADMIN_USER` | admin | Your chosen user for the admin.
`SH_ADMIN_PASS` | W8YcmXMWuTwth5tz | Your chosen password for the admin.
`SH_HOSTED_FILES_URL` | files | URI for hosted files
`SH_HOSTED_FILES` | /data/hosted_files | Path for uploaded files for the server to host
`VIRTUAL_HOST`  |  *None*  | URL the Nginx proxy will route to this container
`TZ` | 'America/Denver' | Timezone for the container to run in


## Volume Mounts
 Path | Purpose
--- | ---
/opt/simple-honey | Code base path
/data/hosted_files | Put files here to make available to a client
/data/logs | Logs from the webserver
/data/simple-honey.cache | Cache file for options and uri map
