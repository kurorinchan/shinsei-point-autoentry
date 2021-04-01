FROM joyzoursky/python-chromedriver:3.8

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install

ENTRYPOINT [ "pipenv", "run", "python", "autoentry.py", "--driver", "/usr/local/bin/chromedriver" ]