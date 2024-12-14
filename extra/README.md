# Extra Manual Testing Files  
Main analysis from files in main directory

## Run
run `docker build --tag flask .`
run `docker run -it -p 80:80 -p 443:443 -p 5000:5000 flask`

In docker container:
run `nginx`
run `gunicorn -b 0.0.0.0:5000 app:app`

Then from another device access the website via:
http://<ip_address of machine running flask app>
or
https://<ip_address of machine running flask app>

The 2 devices have to be connected to the same wifi.