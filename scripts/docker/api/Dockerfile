FROM python:3.6-stretch

RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common vim
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python-dev python3-pip python3-venv
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git telnet curl

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

WORKDIR /home

COPY . .

RUN pip install -r requirements_test.txt
RUN pip install python-dotenv
