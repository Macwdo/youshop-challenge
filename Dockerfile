FROM python:3.11.1

WORKDIR /app

EXPOSE 8000
# python doesn't allow to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get clean && apt-get update
RUN apt-get install -y gcc python3-dev python-dev build-essential musl-dev wkhtmltopdf

# python doesn't buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip wheel

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./commands.sh /app/commands.sh

COPY ./src /app

CMD ["/app/commands.sh"]