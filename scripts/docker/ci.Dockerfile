from docker

RUN apk add make
RUN apk add bash
RUN apk add python3
RUN apk --update add 'py-pip' && pip install 'docker-compose'

ADD . /app

WORKDIR /app
