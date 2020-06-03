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

# Custom nginx conf to add server section
COPY .docker/configs/nginx/conf.d/nginx-custom.conf /etc/nginx/conf.d/nginx-custom.conf

# Add in the codebase
ADD . /app
COPY wait-for-it.sh /app
