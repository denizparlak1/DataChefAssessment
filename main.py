from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db.redis.redis import get_redis_client
from route.campaign import campaign
from route.upload import upload_data
app = FastAPI()

origins = [
    "http://ec2-3-249-239-49.eu-west-1.compute.amazonaws.com:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # Connect to Redis during startup
    get_redis_client()

    # Perform other startup tasks here
    print("Starting up...")
    # ...


@app.on_event("shutdown")
async def shutdown_event():
    # Perform shutdown tasks here
    print("Shutting down...")
    # ...


app.include_router(campaign.router)
app.include_router(upload_data.router)
