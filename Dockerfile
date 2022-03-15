# docker build -t logsight/logsight-result-api .

# set base image (host OS)
FROM python:3.9

ENV LDFLAGS="-L/usr/lib/x86_64-linux-gnu"
ENV CFLAGS="-I/usr/include"

# set the working directory in the container
WORKDIR /code
# install dependencies
RUN pip install PyGithub
RUN pip install logsight-sdk-py==0.1.21

# copy code
COPY ./ .
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["sh", "/entrypoint.sh"]