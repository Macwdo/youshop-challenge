FROM python:3.11.1

WORKDIR /home

EXPOSE 8000
# python doesn't allow to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get clean && apt-get update
RUN apt-get install -y gcc python3-dev python-dev build-essential musl-dev wkhtmltopdf

# python doesn't buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip wheel

COPY requirements.txt /home/requirements.txt
RUN pip install -r requirements.txt

COPY commands.sh /home/commands.sh

RUN chmod +x /home/commands.sh

WORKDIR /home/app

COPY src /home/app

CMD ["/home/commands.sh"]