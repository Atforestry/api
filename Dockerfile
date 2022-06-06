FROM python:3

ARG FETCH_DATA_URL=fetch-data:8000
ARG BATCH_RUN_URL=batch-run:8010
ARG MODEL_PREDICTION_URL=model-prediction:8020
ARG USER_QUERY_URL=user-query:80
ARG API_URL=api:8030
ARG DB_URL=db:5432
ARG POSTGRES_DB=atforestry
ARG POSTGRES_USER=postgres
ARG POSTGRES_PASSWORD=postgres

ENV FETCH_DATA_URL $FETCH_DATA_URL
ENV BATCH_RUN_URL $BATCH_RUN_URL
ENV MODEL_PREDICTION_URL $MODEL_PREDICTION_URL
ENV USER_QUERY_URL $USER_QUERY_URL
ENV API_URL $API_URL
ENV DB_URL $DB_URL
ENV POSTGRES_DB $POSTGRES_DB
ENV POSTGRES_USER $POSTGRES_USER
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./src
COPY ./start.sh .

EXPOSE 8000

CMD ["./start.sh"]
