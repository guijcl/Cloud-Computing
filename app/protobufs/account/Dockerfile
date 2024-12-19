FROM python

RUN mkdir /service
COPY ./  /service/


WORKDIR /service
RUN pip install -r requirements.txt

EXPOSE 51052
EXPOSE 50052
ENTRYPOINT [ "python", "account.py" ]


