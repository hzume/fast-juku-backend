from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from api.routers import root, teacher, timeslot, meta


app = FastAPI()

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

lambda_handler = Mangum(app)
