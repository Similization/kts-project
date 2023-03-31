FROM ubuntu:latest

WORKDIR /kts-project

RUN apt update &&  apt upgrade &&  \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update && \
    apt install python3.10 -y && \
    apt install python3.10-dev -y &&  \
    apt install python3-pip -y && \
    apt install python3.10-venv -y &&  \
    # postgres install
    apt install postgresql postgresql-contrib  &&\
    # postgres start
    apt systemctl start postgresql.service &&  \
    # use psql
    sudo -u postgres psql &&  \
    # create password
    \password postgres && mysecretpassword && mysecretpassword && \
    # create database
    create database kts_project && \
    # grant privileges to user <postgres>
    grant all privileges on database kts_project to postgres && \
    # quit from psql
    \q


RUN mkdir kts_project && cd kts_project &&  \
    python3 -m venv kts_project-env &&  \
    . ./kts_project-env/bin/activate

RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]
