FROM python:2.7


COPY . /techtrends
WORKDIR /techtrends

RUN pip install -r requirements.txt 

RUN python init_db.py
EXPOSE 7111
ENTRYPOINT ["python"]

CMD ["app.py"]

