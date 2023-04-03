#This is BASE IMG
FROM python:3.10

#Define the PORT that the Flask app will run in
EXPOSE 5000

#Define the working dir (move into the working dir)
WORKDIR /app

#excute a command to install flask
RUN pip install flask

#copy from your file system to the docker IMG (copying the file into the IMG)
#Copy . (Current file system working directory - `Flask-Store-App`)
#to . (Current IMG working directory -`/App`)
COPY . .

#What commands should run when this IMG starts up as a container?
#flask is the executable and the rest are parameters!
# --host 0.0.0.0 allows external clients to send requests to the flask app in this container
CMD ["flask", "run", "--host", "0.0.0.0"]