import os

from fastapi import FastAPI
from mangum import Mangum

from api.routers import meta, root, teacher, timeslot, utils

app = FastAPI()


print("ENVIRONMENT VARIABLES")
print(os.environ["REGION"])
print(os.environ["TABLE_NAME"])


# from starlette.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(root.router)
app.include_router(teacher.router)
app.include_router(timeslot.router)
app.include_router(meta.router)
app.include_router(utils.router)

lambda_handler = Mangum(app)
