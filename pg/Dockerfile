FROM python:3.10.0

RUN pip install --pre psycopg[pool]
COPY app.py /usr/local/bin/
CMD [ "/usr/local/bin/app.py" ]