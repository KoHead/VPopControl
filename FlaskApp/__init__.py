# -*- coding: utf-8 -*-
import socket
from system import return_listdir, delete_mailbox, create_mailbox, create_domain
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    hostname=socket.gethostname()
    return "Hello on %s" % hostname

@app.route("/mailbox")
def mailbox_list():
    list_mailbox=return_listdir()
    return jsonify(results=list_mailbox)

@app.route("/delete/<mailboxname>")
def mailbox_delete(mailboxname):
    result_delete=delete_mailbox(mailboxname)
    return (result_delete)

@app.route("/create/mailbox/<mailboxname>")
def mailbox_create(mailboxname):
    result_create=create_mailbox(mailboxname)
    return (result_create)

@app.route("/create/domain/<domain_name>")
def domain_create(domain_name):
    result_create=create_domain(domain_name)
    return (result_create)

if __name__ == "__main__":
    app.run()
