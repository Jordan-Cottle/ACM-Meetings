import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('square.html')

@app.route('/Common/<name>')
def webGL(name):
    with open(f'static/Common/{name}') as file: 
        return file.read()

@app.route('/Square.js')
def glUtils():
    with open(r'static\Square.js') as file: 
        return file.read()