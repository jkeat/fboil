## fboil

Extension of the updated Flask-Boilerplate project found here: https://github.com/mjhea0/flask-boilerplate/tree/master/_updated

### getting started
first create a postgresql database called flask_boilerplate

then run

	make server

you'll get an error. you need to put these environment variable exports in config/env/bin/activate

	export SECRET_KEY="really-long-good-random-key"
	export SECURITY_PASSWORD_SALT="different-long-good-random-key"
	export MAIL_USERNAME="username99"
	export MAIL_PASSWORD="p4ssw0rd"

finally, run

	make server

### major additions to flask-boilerplate
+ user accounts
+ email confirmation
+ password reset
