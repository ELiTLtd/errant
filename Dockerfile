FROM terrillo/python3flask

# STATIC paths for file.
# Don't use flask static. Nginx is your friend
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

# Place your flask application on the server
COPY ./app/main.py /app/main.py
COPY ./app/errant.py /app/errant.py
COPY ./app/requirements.txt /app/requirements.txt
COPY ./scripts/align_text.py /app/scripts/align_text.py
COPY ./scripts/cat_rules.py /app/scripts/cat_rules.py
COPY ./scripts/rdlextra.py /app/scripts/rdlextra.py
COPY ./scripts/toolbox.py /app/scripts/toolbox.py
COPY ./resources/en_GB-large.txt /app/resources/en_GB-large.txt
COPY ./resources/en-ptb_map /app/resources/en-ptb_map
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
