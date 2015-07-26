## fboil

Extension of the updated version of the Flask-Boilerplate project found here: https://github.com/mjhea0/flask-boilerplate/tree/master/_updated

### Getting started
First create two postgresql databases called fboil and fboil_test

Make a new twitter app: https://apps.twitter.com/

Then run

	make install

Next you need to set these environment variables in env/bin/activate

	export APP_SETTINGS="config.DevelopmentConfig"
	export SECRET_KEY="really-long-good-random-key"
	export SECURITY_PASSWORD_SALT="different-long-good-random-key"
	export MAIL_USERNAME="username99"
	export MAIL_PASSWORD="p4ssw0rd"
	export MAIL_DEFAULT_SENDER="username99@gmail.com"
	export TWITTER_CONSUMER_KEY="your-twitter-app-consumer-api-key"
	export TWITTER_CONSUMER_SECRET="your-twitter-app-secret-api-key"

Activate the virtualenv

	source env/bin/activate
	
Then initialize the databases

	make database

Finally, run

	make server

To run a shell with the important stuff imported

	make shell

To run tests

	make test  # basic testing using nosetests
	make coverage  # show which areas aren't tested

To get set up on heroku, first install the toolbelt: https://toolbelt.heroku.com/

Then, run

	heroku create the-next-big-failure
	heroku config:set APP_SETTINGS=config.ProductionConfig SECRET_KEY=not-the-same-as-your-dev-key SECURITY_PASSWORD_SALT=also-not-the-same-as-your-dev-key MAIL_USERNAME=username99 MAIL_PASSWORD=p4ssw0rd TWITTER_CONSUMER_KEY="your-twitter-app-consumer-api-key" TWITTER_CONSUMER_KEY="your-twitter-app-secret-api-key"
	heroku addons:create heroku-postgresql:hobby-dev
	git push heroku master
	heroku run python manage.py db upgrade
	heroku open

And you're ready to go!

### additions to flask-boilerplate
+ user accounts
+ email confirmation
+ password reset
+ account related decorators
+ good testing coverage
+ Twitter OAuth sign in
+ Heroku-friendly
+ testing & production configs


### TODO:
+ git cloning instructions (set remote, etc)
+ virtualenv instructions
+ psql instructions
+ Travis-CI instructions
+ "Collectstatic configuration error" on Heroku
+ use Flask-Security instead of self-rolled email confirmation & password reset systems


### Ideas for next steps
+ Send emails in background task
	+ use second dyno and turn it on/off when needed
	+ (will cost less than a penny/month)
+ Static files on S3
+ CloudFlare
