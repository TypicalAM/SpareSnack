# pull official base image
FROM python:alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 and Pillow dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev zlib zlib-dev jpeg-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# setup entrypoint
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh to make sure that postgres starts before we do
ENTRYPOINT ["sh","/usr/src/app/entrypoint.sh"]
