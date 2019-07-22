FROM terrillo/python3flask

# STATIC paths for file.
# Don't use flask static. Nginx is your friend
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

# Place your flask application on the server
COPY ./app /app
COPY ./scripts ./app/scripts
COPY ./resources ./app/resources
WORKDIR /app

# Install requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m spacy download en

# NGINX setup
COPY ./nginx.sh /nginx.sh
RUN chmod +x /nginx.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["/nginx.sh"]
CMD ["/start.sh"]

EXPOSE 80 443
