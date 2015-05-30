## fboil

Extension of the updated Flask-Boilerplate project found here: https://github.com/mjhea0/flask-boilerplate/tree/master/_updated

### getting started
first create a postgresql database called flask_boilerplate

then run

	make install

next you need to set these environment variables in config/env/bin/activate

	export SECRET_KEY="really-long-good-random-key"
	export SECURITY_PASSWORD_SALT="different-long-good-random-key"
	export MAIL_USERNAME="username99"
	export MAIL_PASSWORD="p4ssw0rd"

finally, run

	make server

### additions to flask-boilerplate
+ user accounts
+ email confirmation
+ password reset
