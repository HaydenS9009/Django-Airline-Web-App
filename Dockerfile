FROM python:3.8-bullseye
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY requirements.txt $WORKDIR
RUN pip3 install -r requirements.txt

COPY . $WORKDIR
RUN rm -r env/

CMD python manage.py runserver 0.0.0.0:8000