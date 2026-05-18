from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True 
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/styles")
    server.watch("static/scripts")
    server.watch("app.py")
    server.serve(port=7070)
