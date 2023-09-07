from mangum import Mangum
from service.main import app

# Mangum is a library that helps you deploy your FastAPI application
# into an AWS Lambda function.
handler = Mangum(app)