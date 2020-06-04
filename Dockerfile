FROM python:3.7
RUN pip install pipenv
WORKDIR /usr/src/app
ENV USER="saul-goodman"
RUN adduser --disabled-password --home "$(pwd)" --no-create-home "$USER"
COPY Pipfile Pipfile.lock start.sh ./
RUN pipenv lock --requirements > requirements.txt && pip install -r ./requirements.txt
COPY saul_goodman ./saul_goodman
RUN chown -R "$USER":"$USER" /usr/src/app
USER $USER
ENTRYPOINT ["./start.sh"]
