FROM python:3.10

COPY ./ercc/requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ercc/source ./

CMD [ "python", "./main.py" ]