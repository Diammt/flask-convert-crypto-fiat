from .start import app
from .start import API_URL, swagger 
from .start import app
import logging as lg
import json

@app.cli.command()
def api_generate():
    # print(swagger(app))
    with open("project/api"+API_URL, "w+") as f:
        json.dump(swagger(app), f, indent=4)
    lg.warning("API generate successfuly at {}".format(API_URL))

if __name__ == '__main__':
    app.run(debug=True)