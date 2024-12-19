# 3rd party moudles
import connexion
from flask import render_template
from flask_cors import CORS
from prometheus_client import start_http_server, Summary

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# read the swagger.yml file to configure the endpoints
app.add_api("front_end_copy.yaml")

# Create a URL route in our application for "/"
@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000
    :return:        the rendered template "home.html"
    """
    return render_template("home.html") 
    
@app.route("/health")
def health():
    return 'it works',200

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@REQUEST_TIME.time()   
def serve():
  app.run(debug=True,host='0.0.0.0', port="80")
  #app.run(ssl_context='adhoc') #oferece alguma proteçao
  #app.run(port=5000)
  #CORS(app.app)


if __name__ == "__main__":
    serve()