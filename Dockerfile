FROM python3

RUN adduser -D stepik

WORKDIR /home/stepik

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY run.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R stepik:stepik ./
USER stepik

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]