import logging

from flask import Flask, request as req

from app.controllers import pages
from app.models import db


app = Flask(__name__)
app.config.from_object('config.development')

app.register_blueprint(pages.blueprint)

app.logger.setLevel(logging.NOTSET)


@app.after_request
def log_response(resp):
    app.logger.info("{} {} {}\n{}".format(
        req.method, req.url, req.data, resp)
    )
    return resp
