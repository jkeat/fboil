import logging

from flask import Flask, request as req

app = Flask(__name__)
app.config.from_object('config.development')


from app.controllers import pages
from app import models


app.register_blueprint(pages.blueprint)

app.logger.setLevel(logging.NOTSET)


@app.after_request
def log_response(resp):
    app.logger.info("{} {} {}\n{}".format(
        req.method, req.url, req.data, resp)
    )
    return resp
