from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(title="Description")
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "0e39b99a-ab60-4a14-8ac8-3c2a4898a632",
                "title": "Computer",
                "author": "Author 1",
                "description": "Good book",
                "rating": 90
            }
        }

BOOKS = []

@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_book_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i=1
        new_book = []
        while i <= books_to_return:
            new_book.append(BOOKS[i-1])
            i += 1
        return new_book   
        
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id:UUID):
    
        
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id : UUID, book: Book):
    counter = 0
    
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS [counter - 1]

@app.delete("/{book_id}")
async def delete_book(book_id : UUID):
    counter = 0
    
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID:{book_id} delete'




def create_book_no_api():
    book_1 = Book(
        id="1e39b99a-ab60-4a14-8ac8-3c2a4898a638",
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=60
    )

    book_2 = Book(
        id="2e39b99a-ab60-4a14-8ac8-3c2a4898a638",
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=40
    )

    book_3 = Book(
        id="3e39b99a-ab60-4a14-8ac8-3c2a4898a638",
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=30
    )

    book_4 = Book(
        id="4e39b99a-ab60-4a14-8ac8-3c2a4898a638",
        title="Title 4",
        author="Author 4",
        description="Description 4",
        rating=40
    )

    BOOKS.extend([book_1, book_2, book_3, book_4])
