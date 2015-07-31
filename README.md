## About

Extension of the updated version of the Flask-Boilerplate project found here: https://github.com/mjhea0/flask-boilerplate/tree/master/_updated

### Additions to flask-boilerplate
+ user accounts
+ email confirmation
+ password reset
+ account related decorators
+ good testing coverage
+ Twitter OAuth sign in
+ Heroku-ready, Travis CI-ready
+ testing & production configs

## Setup

Clone this repo and add your new repo location:

	$ git clone https://github.com/jkeat/fboil.git
	$ git remote rm origin
	$ git remote add origin <the location of my new git repository>
	$ git push -u origin master

Make sure you have [pip](https://pip.pypa.io/en/latest/installing.html) and [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) installed.

### PostgreSQL

Create two [postgresql](http://www.postgresql.org/download/) databases called `fboil` and `fboil_test`.

If you name them something different, which you probably should, make sure you change the config variable `SQLALCHEMY_DATABASE_URI` in `config.py`'s `DevelopmentConfig` and `TestingConfig` classes.

### Twitter

Make two new [Twitter apps](https://apps.twitter.com/), one called `<Your app>` and one called `<Your app> dev`.

Set the dev version's callback URL to `http://127.0.0.1:5000/oauth-authorized` and the production version's to `https://[your app].herokuapp.com/oauth-authorized`.

(If you can get the dynamic callback working, where you send the callback URL to Twitter, then do that! Then you can check the `APP_SETTINGS` environment variable and send the appropriate callback. Then you only need to make one Twitter app. And send me a pull request!)

### Action!

Run 

	$ make install

This creates a virtualenv and installs the dependencies.

Next you need to set these environment variables in env/bin/activate

	$ export APP_SETTINGS="config.DevelopmentConfig"
	$ export SECRET_KEY="really-long-good-random-key"
	$ export SECURITY_PASSWORD_SALT="different-long-good-random-key"
	$ export MAIL_USERNAME="username99"
	$ export MAIL_PASSWORD="p4ssw0rd"
	$ export MAIL_DEFAULT_SENDER="username99@gmail.com"
	$ export TWITTER_CONSUMER_KEY="your-twitter-app-consumer-api-key"
	$ export TWITTER_CONSUMER_SECRET="your-twitter-app-secret-api-key"

Activate the virtualenv

	$ source env/bin/activate

Always activate it before you start working on your project!
	
Then initialize the development database

	$ make database

Finally, run

	$ make server

To run a shell with the important stuff imported

	$ make shell

To run tests

	$ make test  # basic testing using nosetests
	$ make coverage  # show which areas aren't tested

To get set up on heroku, first install the toolbelt: https://toolbelt.heroku.com/

Then, run

	$ heroku create the-next-big-failure
	$ heroku config:set APP_SETTINGS=config.ProductionConfig SECRET_KEY=not-the-same-as-your-dev-key SECURITY_PASSWORD_SALT=also-not-the-same-as-your-dev-key MAIL_USERNAME=username99 MAIL_PASSWORD=p4ssw0rd TWITTER_CONSUMER_KEY="your-twitter-app-consumer-api-key" TWITTER_CONSUMER_KEY="your-twitter-app-secret-api-key"
	$ heroku addons:create heroku-postgresql:hobby-dev
	$ git push heroku master
	$ heroku run python manage.py db upgrade
	$ heroku open

And you're ready to go!

#### Travis-CI

If you want to have your app automatically tested when you push it to GitHub, you can use [Travis-CI](travis-ci.org).

(If you're just getting started with Flask, I'd recommend saving this for later.)

Sign in and add your repo. You need to set the same config variables on Travis-CI as you did on Heroku, besides APP_SETTINGS, which is already set to config.TestingConfig for you in the .travis.yml file.

Use different values for SECRET_KEY and SECURITY_PASSWORD_SALT, though.

#### Makefile

I'd recommend reading through the Makefile so you know what the different commands are actually doing.

### TODO:
+ More tutorial-esque instructions
+ `Collectstatic configuration error` on Heroku
+ use Flask-Security instead of self-rolled email confirmation & password reset systems
+ CSS
	+ Branch for bare HTML, no CSS framework
	+ Branch for Semantic-UI
	+ Single layout for form/main to inherit
+ Favicon stuff

### Ideas for next steps
+ Send emails in background task
	+ use second dyno and turn it on/off when needed
	+ (will cost less than a penny/month)
+ Static files on S3
+ CloudFlare
