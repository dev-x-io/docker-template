# Gebruik het nieuwste officiële Alpine-beeld als basis
FROM alpine:latest

ENV APP_VERSION=v0.0.0


VOLUME [ "/devxio", "/modules", "/templates", "/docs" ]

# Kopieer het Python-script (banner.py) naar de container
COPY ./app/ /app

# Kopieer de jinja templates naar de container
COPY ./templates/ /templates

# Stel een werkdirectory in
WORKDIR /app

# Installeer Python, pip, upgrade pip en installeer Python-bibliotheken in één RUN commando
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Stel het Python-script in als het commando dat wordt uitgevoerd wanneer de container wordt gestart
ENTRYPOINT ["python3", "main.py"]
CMD ["-h"]