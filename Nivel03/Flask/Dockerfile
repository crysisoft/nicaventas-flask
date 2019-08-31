FROM python

COPY app /app
RUN pip install -r /app/requirements.txt

WORKDIR app

## THE LIFE SAVER
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

## Launch the wait tool and then your application
CMD /wait && python app.py