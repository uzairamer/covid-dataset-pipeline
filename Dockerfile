FROM apache/airflow:2.2.4-python3.8

USER root
RUN apt-get update
RUN apt-get install -y libpq-dev \
                        gcc 
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app/

# in order to keep the container running
# ENTRYPOINT ["tail", "-f", "/dev/null"]
