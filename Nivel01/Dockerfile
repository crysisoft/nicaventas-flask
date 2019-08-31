FROM python

MAINTAINER Itihell itihell.mejia@gmail.com

COPY app /app
RUN pip install -r /app/requirements.txt

WORKDIR app

EXPOSE 8000

CMD ["python", "main.py"]
