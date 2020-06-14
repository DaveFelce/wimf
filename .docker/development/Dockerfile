FROM tiangolo/uwsgi-nginx:python3.8

# Flask section
ENV PYTHONBUFFERED 1
ENV APPLICATION_ROOT /app/
RUN mkdir -p $APPLICATION_ROOT
WORKDIR $APPLICATION_ROOT
RUN pip install pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --system

# Expose ports for nginx
ENV LISTEN_PORT 8080
EXPOSE 8080

# Change the maintainer's uWSGI override location, to keep our configs out of the /app dir
# Can't just COPY the file as it must be needed before any COPY gets run in here
ENV UWSGI_INI /app/.docker/configs/uwsgi/uwsgi.ini

# Custom nginx conf to add server section
COPY .docker/configs/nginx/development/conf.d/nginx-custom.conf /etc/nginx/conf.d/nginx-custom.conf

# Add in the codebase
ADD . /app
COPY wait-for-it.sh /app
