
# Base alpine image with node and npm preinstalled
FROM python:3

# Add docker-compose-wait tool
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN pip install pipenv

COPY . /watchdog
WORKDIR /watchdog

# this throws a couple of errors but seems to still work
RUN pipenv install --system --deploy

CMD ["python", "/watchdog/runner.py"]
