FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN apt-get update

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

RUN apt-get update

RUN apt-get install -y git vim wget

RUN wget https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh

RUN bash script.deb.sh

RUN apt-get install -y git-lfs

RUN git clone https://huggingface.co/jihopark/GPT2-Article-Large2

WORKDIR /app/GPT2-Article-Large2

RUN cat a.tar* | tar xvf -

RUN rm a.tar*

WORKDIR /app

COPY . .

CMD python3 server.py
