FROM python

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# install dependencies
RUN pip install --upgrade pip
COPY ./requirement.txt /usr/src/app/requirement.txt
RUN pip install -r /usr/src/app/requirement.txt

# Entrypoint
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy Project
COPY . /usr/src/app/


CMD ["sh","/usr/src/app/entrypoint.sh"]
