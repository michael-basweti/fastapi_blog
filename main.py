# from select import select
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import Base, engine
from handlers import general_http_exception_handler, validation_exception_handler
from routers import pages, posts, users


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Create the database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Optionally, you can add code here to run on shutdown


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

# include in_schema=False to hide this route from the automatic docs

app.include_router(pages.router)

app.include_router(users.router, prefix="/api/users", tags=["Users"])

app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])


# StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
async def custom_general_http_exception_handler(
    request: Request, exception: StarletteHTTPException
):
    return await general_http_exception_handler(request, exception)


# RequestValidationError Handler
@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(
    request: Request, exception: RequestValidationError
):
    return await validation_exception_handler(request, exception)
