FROM python:3-alpine

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . .

ENTRYPOINT [ "python", "smtptohttp.py" ]
