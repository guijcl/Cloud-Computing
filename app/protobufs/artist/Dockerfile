FROM python

RUN mkdir /service
COPY ./  /service/

WORKDIR /service

RUN pip install -r requirements.txt

EXPOSE 51055
EXPOSE 50055
ENTRYPOINT [ "python", "artist.py" ]
