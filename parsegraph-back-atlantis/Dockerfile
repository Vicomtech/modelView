FROM python:3.9.13

# specifying the working directory inside the container
WORKDIR /usr/src/app

# installing the Python dependencies
COPY requirements.txt .
RUN apt-get dist-upgrade
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U flask-cors
RUN pip install pyopenssl

# copying the contents of our app' inside the container
COPY . .

# defining env vars
ENV FLASK_APP="entrypoint:app"
ENV FLASK_ENV=development

# running Flask as a module, we sleep a little here to make sure that the DB is fully instanciated before running our app'
CMD ["sh", "-c", "sleep 5 \ 
  && flask run --host=0.0.0.0 --cert=adhoc"]