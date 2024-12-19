FROM python

RUN mkdir /service
COPY ./  /service/

WORKDIR /service
RUN pip3 install -r requirements.txt



EXPOSE 50051
EXPOSE 51051
ENTRYPOINT [ "python3", "music.py" ]


