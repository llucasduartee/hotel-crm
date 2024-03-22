FROM python:3.9


WORKDIR /app


COPY . /app


RUN pip install -r requirements.txt


ENV DJANGO_SETTINGS_MODULE=crm.settings


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]