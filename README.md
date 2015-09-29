# Fboil

Fboil is a muscular, charming, and loyal Flask boilerplate powered by Flask-Login, WTForms, PostgreSQL & SQLAlchemy, and Flask-Testing. There's also Twitter OAuth login, branches for Semantic-UI/no CSS, and a lot more. Fboil is ready to run on Heroku and test on Travis-CI.

Demo: https://fboil.herokuapp.com/

Fboil is built off the [updated version](https://github.com/mjhea0/flask-boilerplate/tree/master/_updated) of Flask-Boilerplate.

##### Additions to Flask-Boilerplate

+ User accounts
	+ Email/username/password
		+ Email confirmation
		+ Password reset
	+ Twitter OAuth
+ Lots of tests
+ Flexible CSS
	+ Semantic-UI (`master` branch)
	+ No CSS framework (`bare-css` branch)
+ Multiple configs (development, testing, production)
+ Heroku-ready, Travis CI-ready

## Setup

Clone this repo then add your new repo location

	$ git clone https://github.com/jkeat/fboil.git
	$ mv fboil <Your app>
	$ cd <Your app>
	$ git remote rm origin
	$ git remote add origin <the location of your new git repo>
	$ git push -u origin master

Make sure you have [pip](https://pip.pypa.io/en/latest/installing.html) and [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) installed.

### PostgreSQL

Create two [postgresql](http://www.postgresql.org/download/) databases called `<Your app>` and `<Your app>_dev`.

Change the config variable `SQLALCHEMY_DATABASE_URI` in `config.py`'s `DevelopmentConfig` and `TestingConfig` classes from `fboil` and `fboil_dev` to `<Your app>` and `<Your app>_dev`.

### Twitter

Make two new [Twitter apps](https://apps.twitter.com/), one called `<Your app>` and one called `<Your app> dev`.

Set the dev version's callback URL to `http://127.0.0.1:5000/oauth-authorized` and the production version's to `https://<Your app>.herokuapp.com/oauth-authorized`.

> If you can get the dynamic callback working, where you send the callback URL to Twitter, then do that! You can send the appropriate callback based on the `APP_SETTINGS` environment variable, so you only need to make one Twitter app. Then tell me how you got it working!

### Action

Navigate to your project's directory and run 

	$ make install

This creates a virtualenv and pip installs the packages listed in `requirements.txt`.

Next you need to set these environment variables at the top of `env/bin/activate`

	export APP_SETTINGS="config.DevelopmentConfig"
	export SECRET_KEY="really-long-good-random-key"
	export SECURITY_PASSWORD_SALT="different-long-good-random-key"
	export MAIL_USERNAME="username99"
	export MAIL_PASSWORD="p4ssw0rd"
	export MAIL_DEFAULT_SENDER="username99@example.com"
	export TWITTER_CONSUMER_KEY="your-twitter-app-consumer-api-key"
	export TWITTER_CONSUMER_SECRET="your-twitter-app-secret-api-key"

Activate the virtualenv

	$ source env/bin/activate

Always activate it before you start working on your project!
	
Then initialize the development database

	$ make database

Add & commit everything!

	$ git add .
	$ git commit -m "Fboil initializations"

Finally, run

	$ make server

Open up the app at `http://127.0.0.1:5000/`

## Helpful tools

To run a python shell with the important stuff imported

	$ make shell

To run tests

	$ make test  # basic testing using nosetests
	$ make coverage  # show which areas of your code aren't tested

## Heroku

To get set up on Heroku, make a [Heroku account](https://signup.heroku.com/) and install the [toolbelt](https://toolbelt.heroku.com/).

Log in to the Heroku CLI

	$ heroku login

Then, run

	$ heroku create <Your app>
	$ heroku config:set APP_SETTINGS=config.ProductionConfig SECRET_KEY=not-the-same-as-your-dev-key SECURITY_PASSWORD_SALT=also-not-the-same-as-your-dev-salt MAIL_USERNAME=username99 MAIL_PASSWORD=p4ssw0rd MAIL_DEFAULT_SENDER=username99@example.com TWITTER_CONSUMER_KEY=your-twitter-app-consumer-api-key TWITTER_CONSUMER_KEY=your-twitter-app-secret-api-key
	$ heroku addons:create heroku-postgresql:hobby-dev
	$ git push heroku master
	$ heroku run python manage.py db upgrade
	$ heroku open

And you're ready to go!

## Travis-CI

If you want to have your app automatically tested when you push it to GitHub, you can use [Travis-CI](travis-ci.org).

(If you're just getting started with Flask, save this for later.)

Sign in to Travis-CI with your GitHub account and add your repository. You need to set the same config variables on Travis-CI as you did on Heroku, besides `APP_SETTINGS`, which is already set to `config.TestingConfig` for you in the `.travis.yml` file.

Make sure you don't use the same `SECRET_KEY` and `SECURITY_PASSWORD_SALT` as your development or production versions.

## Ideas for next steps
+ Send emails in background task
	+ Use second Heorku dyno and turn it on only when needed
	+ Will cost less than a penny/month
+ Static files on S3
	+ https://flask-cdn.readthedocs.org/en/latest/
+ CloudFlare

## TODO
+ Clean up CSS & JS
+ `Collectstatic configuration error` on Heroku?
+ Flask-Security
	+ Testing
	+ Clean up unused old user blueprint stuff
+ Make a simple extension of fboil (a Twitter clone or something)
+ Save Twitter I.D. as unique identifier, not username

