FROM ubuntu:22.04

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip3 install librouteros fastapi uvicorn


COPY . /opt/
WORKDIR /opt/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 8090/tcp
