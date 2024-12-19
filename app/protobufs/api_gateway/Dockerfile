FROM python

RUN mkdir /service
COPY ./  /service/

WORKDIR /service

RUN pip install -r requirements.txt


EXPOSE 5000
EXPOSE 80

ENTRYPOINT [ "python", "server.py" ]
