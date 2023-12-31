from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from api.routers import root, teacher, timeslot, meta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(root.router)
app.include_router(teacher.router)
app.include_router(timeslot.router)
app.include_router(meta.router)

lambda_handler = Mangum(app)

"""Sample pure Lambda function

Parameters
----------
event: dict, required
    API Gateway Lambda Proxy Input Format

    Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

context: object, required
    Lambda Context runtime methods and attributes

    Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

Returns
------
API Gateway Lambda Proxy Output Format: dict

    Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
"""

