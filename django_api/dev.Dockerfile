FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

ENV DJANG_SETTINGS_MODULE "src.config.settings"
ENV DJANGO_PORT 8000

EXPOSE ${DJANGO_PORT}

CMD python manage.py runserver 0.0.0.0:${DJANGO_PORT}