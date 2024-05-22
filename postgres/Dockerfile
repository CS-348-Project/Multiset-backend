FROM postgres:13.3
ENV POSTGRES_DB=cs348
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

ENV LOGGING_LEVEL=error
COPY ./local_schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB
