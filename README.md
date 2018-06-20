# Simple Honey
### So, why?
* **Core Idea**
  Simple Honey is a light weight, Dockerized, python based web server, with lots of features for quickly handling legitimate or iligitatmet web requests. Out of the box Simple-Honey responds to any and all requests with a blank (0 byte) HTTP 200 response to any request made.
  Once a request is made, Simple-Honey records the IP address, User Agent String, requested server domain, and  requested server uri, from the remote client. This is incredibly useful for server admin's trying to identity "bad actors" regularly scanning servers for uris such as "http://phpmyadmin.example.com/" and more.

* **Really Quick Deployment/ Hosting of small tasks**
  The aURI mapping features in the Simple-Honey give users the capabilities to quickly create a custom uri route which can map to multiple different types of reponses such as;
  * **Static files** - (html/ css/ js/ images/ video)
  * **Redirect** - Create short urls which will respond with a 301 response and push a user to a differnt url.
  * **Raw Content** - Give a url JSON content to serve to the client
  * **Uploaded Cutsom HTML** Add files over the web admin and then route URIs to hit that end point.

* **Securirty/ Bad-Actor Hunting Reseach**
  Once configured in the Simple-Honey admin, you can create custom /robots.txt and other web uris, and get insight into which ips/ user agents are crawling your domain(s), whether or not they are following the policies you've publically set and so much more!

* **Really Quick Hosting Contet**

  Simple-Honey's admin is always creating new features to make hosting content on multiple domains/ subdomains / anything you can think of super simple, for a full feature set of what type of end-user featues can be enabled, go to the website im going to make for that...

## How to install Simple-Honey
### (Step 1) Install Simple-Honey
```
git clone https://github.com/politeauthority/simple-honey.git
docker build -t simple-honey .
docker run \
    --name=simple-honey \
    -e SH_DB_USER="theproductionuser" \
    -e SH_DB_PASS="thekillerpass" \
    -e SH_ADMIN_URL="8NxyeYizYbCr76O40" \
    -e SH_ADMIN_PASS="Mj5UO6dEXtihNalZ" \
    -e VIRTUAL_HOST='example.com,*.other-example.com' \
    -td \
    --restart=always \
    simple-honey
```
  #### Environmental Vars
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

#### Volume Mounts/ Places of Interest
 Path | Purpose
--- | ---
/opt/simple-honey | Code base path
/data/hosted_files | Put files here to make available to a client
/data/logs | Logs from the webserver
/data/simple-honey.cache | Cache file for options and uri map
#### (Step 2) Create a the database (via Docker)
```
docker stop some-postgres
docker rm some-postgres
docker run \
    --name=some-postgres \
    --network=mynetwork \
    -d \
    -e POSTGRES_USER="theproductionuser" \
    -e POSTGRES_PASSWORD="thekillerpass" \
    -v /root/data/some-postgres/postgres:/var/lib/postgresql/data \
    -v /root/data/some-postgres/backups:/var/tmp \
    --restart=always \
    postgres:alpine
```

### (Step 3) Create the HTTP/S proxy handler
This is another project I dont manage but love and Simple-Honey proudly stands off of, but if its not workings, ask them not me! Howver, this is more or less how, I'm making use of it. For info on SSL support, look to Jwilder, he's got waaaaaay better docs.
https://github.com/jwilder/nginx-proxy
```
docker run \
     --name=nginx-proxy \
     --network=mynetwork \
    -d \
    -p 80:80 \
    -p 443:443 \
    -v /var/run/docker.sock:/tmp/docker.sock:ro \
    --restart=always \
    jwilder/nginx-proxy
 ```

## Future Developement
* More custom URI typpes
  * Custom python modules
  * Simple customizable, uploadable HTML/Jinja templates
*   JSON file logging.
  Convert all current web logging into a JSON log format, this would allow pulling in Simple-Honey data into more interesting data aggregator/ collectors. Simple-Honey logs into other logg
*   Web API
  An optional web based API, requring authentication via the prescribed web admin user/ pass. this would allow pulling Simple-Honey data into more interesting data aggregator/ collectors.

## Your Still Here?
So with all three docker containers Simple-Honey installs at **449.5MB**, which is all 3 services, database, web proxy, and simple honey. PLUS we're working on bring that down even more!
