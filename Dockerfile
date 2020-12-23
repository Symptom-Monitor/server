FROM tiangolo/uwsgi-nginx-flask:python3.8-2020-12-19

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy source
COPY . .

# Create data volume
VOLUME [ "/data" ]
ENV DATA_DIR "/data"

# Nginx config
ENV STATIC_PATH /app/public

EXPOSE 80
