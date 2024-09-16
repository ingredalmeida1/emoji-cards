FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y -qq --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    freeglut3 \
    freeglut3-dev \
    libfreetype6 \
    libfreetype6-dev \
    fontconfig \
    libfontconfig1 \
    libfontconfig1-dev \
    python3-pip \
    python-is-python3

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python -u main.py
