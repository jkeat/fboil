import logging

from flask import Flask, request as req

from app.controllers import pages

app = Flask(__name__)
app.config.from_object('config.development')

app.register_blueprint(pages.blueprint)

app.logger.setLevel(logging.NOTSET)


from app import models


@app.after_request
def log_response(resp):
    app.logger.info("{} {} {}\n{}".format(
        req.method, req.url, req.data, resp)
    )
    return resp
