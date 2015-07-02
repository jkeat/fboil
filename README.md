## fboil

Extension of the updated version of the Flask-Boilerplate project found here: https://github.com/mjhea0/flask-boilerplate/tree/master/_updated

### getting started
first create two postgresql databases called fboil and fboil_test

then run

	make install

next you need to set these environment variables in config/env/bin/activate
(set APP_SETTINGS to config.your_deployment_config_file on deployment)

	export APP_SETTINGS="config.development"
	export SECRET_KEY="really-long-good-random-key"
	export SECURITY_PASSWORD_SALT="different-long-good-random-key"
	export MAIL_USERNAME="username99"
	export MAIL_PASSWORD="p4ssw0rd"
	
then initialize the databases

	make database

finally, run

	make server

to activate the virtualenv later, run

	source config/development/env/bin/activate

to run a shell with the important stuff imported

	make shell

### additions to flask-boilerplate
+ user accounts
+ email confirmation
+ password reset
