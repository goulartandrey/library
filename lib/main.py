from fastapi import FastAPI

from lib.routers import auth, books, users, wishlist

app = FastAPI(title="API DOS GURI")


app.include_router(auth.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(wishlist.router)
