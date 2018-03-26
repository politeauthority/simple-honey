FROM frolvlad/alpine-python3
RUN apk add --no-cache \
    bash \
    python3 \
    python-dev \
    py-pip \
    gcc \
    postgresql-dev \
    py3-psycopg2 \
    && rm -rf /var/cache/apk/*

COPY ./ /opt/simple-honey/
RUN pip3 install -r /opt/simple-honey/requirements.txt
ENV SH_DB_ENGINE='postgresql'
ENV SH_DB_HOST="some-postgres"
ENV SH_DB_USER="User"
ENV SH_DB_PASS="Pass"
ENV SH_DB_PORT="5432"
ENV SH_DB_NAME="simple_honey"
ENV SH_ADMIN_URL="the-admin"
ENV FLASK_APP="/opt/simple-honey/manage.py"
ENV TZ=America/Denver

VOLUME /opt/simple-honey
VOLUME /data
RUN mkdir -p /data/hosted_files
EXPOSE 80

WORKDIR /opt/simple-honey/
CMD gunicorn -b 0.0.0.0:80 app:app
