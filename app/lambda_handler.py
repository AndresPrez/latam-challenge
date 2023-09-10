import sys
from mangum import Mangum
from main import app

# Add the path to the Lambda Layer directory to sys.path
layer_path = '/opt'
if layer_path not in sys.path:
    sys.path.append(layer_path)

handler = Mangum(app)