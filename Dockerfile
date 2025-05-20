FROM public.ecr.aws/docker/library/alpine:3.14

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "application.py"]

RUN pip install newrelic


ENV NEW_RELIC_APP_NAME="Blacklist-app"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG_LEVEL=info


ENTRYPOINT [ "newrelic-admin", "run-program" ]