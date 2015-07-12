## fboil

Extension of the updated version of the Flask-Boilerplate project found here: https://github.com/mjhea0/flask-boilerplate/tree/master/_updated

### getting started
first create two postgresql databases called fboil and fboil_test

then run

	make install

next you need to set these environment variables in config/development/env/bin/activate

	export APP_SETTINGS="config.development"
	export SECRET_KEY="really-long-good-random-key"
	export SECURITY_PASSWORD_SALT="different-long-good-random-key"
	export MAIL_USERNAME="username99"
	export MAIL_PASSWORD="p4ssw0rd"
	
then initialize the databases

	make database

finally, run

	make server

to activate the virtualenv later

	source config/development/env/bin/activate

to run a shell with the important stuff imported

	make shell

to run tests

	nosetests

to get set up on heroku

	heroku create the-next-big-flop (your app name)
	heroku config:set APP_SETTINGS="config.production" SECRET_KEY="not-the-same-as-your-dev-key" SECURITY_PASSWORD_SALT="also-not-the-same-as-your-dev-key" MAIL_USERNAME="username99" MAIL_PASSWORD="p4ssw0rd"
	heroku addons:create heroku-postgresql:hobby-dev
	git push heroku master
	heroku run python manage.py db upgrade
	heroku open

### additions to flask-boilerplate
+ user accounts
+ email confirmation
+ password reset
+ account related decorators
+ 100% testing coverage
+ Heroku-friendly
+ testing & production configs
