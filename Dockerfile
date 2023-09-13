FROM tiangolo/uwsgi-nginx-flask:python3.11-alpine
RUN apk --update add bash nano, vim
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
