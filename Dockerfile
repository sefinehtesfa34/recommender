FROM python:3.8-alpine
LABEL maintainer = "mindplex.com"
WORKDIR  /recommender

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt  /recommender/requirements.txt
RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --update --no-cache py3-numpy py3-pandas@testing
ENV PYTHONPATH=/usr/lib/python3.8/site-packages

RUN pip install -r requirements.txt

# copy project
COPY . /recommender/

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
USER appUser