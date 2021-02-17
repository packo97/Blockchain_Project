# Python 3.8 image
FROM python:3.8

# Set working directory
WORKDIR /usr/src/blockchain-app

# Copy all in working directory
COPY . /usr/src/blockchain-app
VOLUME [ "/usr/src/blockchain-app/docker-configs" ]

# Install requirements
RUN pip install -r requirements.txt

# Expose port 50000 to 60000
EXPOSE 50000-60000