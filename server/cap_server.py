from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('config_form.html')

@app.route("/sort_results", methods=['GET'])
def return_results():
    return render_template('cap_image.html')

@app.route("/inspect_caps")
def inspect_caps():
    return render_template('inspect_caps.html')

@app.route("/reject_caps", methods=['POST'])
def inspect_caps():
    return None


if __name__ == "__main__":
    app.run()

