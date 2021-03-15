FROM python:2.7
WORKDIR /app
COPY . . 
RUN pip install -r requirements.txt 

RUN python init_db.py
EXPOSE 7111
ENTRYPOINT ["python"]

CMD ["app.py"]

