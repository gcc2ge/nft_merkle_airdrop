FROM ubuntu:18.04

# Install python3
RUN apt-get update && \
    apt-get install -y python3 \
                        python3-dev \
                        python3-pip \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*



#Install other libs
ADD ./requirements.txt /home/
RUN pip3 install -r /home/requirements.txt

COPY data /home/data
COPY merkle_drop /home/merkle_drop

ENV PYTHONPATH=/home/

WORKDIR /home/merkle_drop
CMD ["python3", "./server.py"]