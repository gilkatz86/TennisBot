#coding: utf-8

import os
import config

from flask import Flask, request
from bot import bot #, score_request


app = Flask(__name__)

@app.route("/", methods=['POST'])
def root():
  return bot(request)

app.run(port=os.environ['PORT'])
