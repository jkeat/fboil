#!/usr/bin/env python
import os
from flask import *
from app import *

app = create_app(os.environ['APP_SETTINGS'])
app.test_request_context().push()

# run with the -i flag to enter shell after executing
# $ python -i shell.py
