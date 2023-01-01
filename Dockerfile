FROM python:3.10

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

CMD [ "pipenv", "run", "python", "bot.py" ]


