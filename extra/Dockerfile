FROM ubuntu:jammy-20240911.1
WORKDIR /app
RUN apt update
RUN apt upgrade -y
RUN apt install python3-pip nginx sqlite3 -y
RUN pip install flask flask_sqlalchemy flask_login sqlalchemy gunicorn
RUN rm /etc/nginx/sites-enabled/default 
COPY nginx.conf /etc/nginx/nginx.conf
COPY certificate.pem /etc/nginx/certificate.pem
COPY key.pem /etc/nginx/key.pem
COPY templates/ /app/templates/
COPY models.py /app
COPY app.py /app
EXPOSE 80 443 5000
