from flask import Flask
app = Flask(__name__)
app.secret_key = 'I loev coding'
DATABASE = 'logins_schema'