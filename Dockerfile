FROM frolvlad/alpine-python3

EXPOSE 80

ENV SH_DB_ENGINE='postgresql'
ENV SH_DB_HOST="some-postgres"
ENV SH_DB_USER="User"
ENV SH_DB_PASS="Pass"
ENV SH_DB_PORT="5432"
ENV SH_DB_NAME="simple_honey"
ENV SH_ADMIN_URL="the-admin"
ENV SH_ADMIN_USER="admin"
ENV SH_ADMIN_PASS="W8YcmXMWuTwth5tz"
ENV SH_HOSTED_FILES_URL="files"
ENV SH_HOSTED_FILES="/data/hosted_files/"
ENV SH_CACHE_FILE="/data/simple-honey.cache"
ENV FLASK_APP="/opt/simple-honey/manage.py"
ENV TZ=America/Denver

VOLUME /opt/simple-honey
VOLUME /data

COPY ./ /opt/simple-honey/

RUN apk add --no-cache \
    bash \
    python3 \
    python-dev \
    py-pip \
    gcc \
    postgresql-dev \
    py3-psycopg2 \
    && rm -rf /var/cache/apk/*

WORKDIR /opt/simple-honey/

RUN pip3 install -r requirements.txt
RUN mkdir -p ${SH_HOSTED_FILES}
RUN mkdir -p ${SH_HOSTED_FILES}/templates
RUN mkdir -p /data/cache/
RUN touch ${SH_CACHE_FILE}

CMD gunicorn -b 0.0.0.0:80 app:app
