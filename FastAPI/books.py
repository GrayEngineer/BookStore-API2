from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS= {
    "book_1":{"title":"title_one", "Auther":"Auther_one"},
    "book_2":{"title":"title_two", "Auther":"Auther_two"},
    "book_3":{"title":"title_three", "Auther":"Auther_three"},
}

class DirectionName(str, Enum):
    north="North"
    south="South"
    east="East"
    west="West"



@app.get("/")
async def read_all_books():
    return BOOKS

# @app.get("/directions/{directions_name}")
# async def get_direction(direction_name: DirectionName):
#     if direction_name== DirectionName.north:
#         return {"Direction": direction_name, "sub":"Up"}   
#     if direction_name== DirectionName.south:
#         return {"Direction": direction_name, "sub":"Down"}
#     if direction_name== DirectionName.west:
#         return {"Direction": direction_name, "sub":"Left"} 
#     if direction_name== DirectionName.east:
#         return {"Direction": direction_name, "sub":"Right"}            

@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title" : "My favorite book"}    

@app.get("/books/{book_id}")
async def read_book(book_id:int):
    return {"book_id": book_id}


@app.post("/")
async def create_book(book_title, book_auther):
    current_book_id =0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split("_")[-1])
            if x > current_book_id:
                current_book_id = x

    BOOKS[f'book_{current_book_id + 1}'] ={'title': book_title, 'auther': book_auther}
    return BOOKS[f'book_{current_book_id + 1}']            

@app.put("/")
async def update_book(book_name: str, book_title: str, book_auther: str):
    book_information = {"title": book_title, "auther": book_auther}
    BOOKS[book_name] = book_information
    return book_information

@app.delete("/{book_name}")    
async def delete_book(book_name):
    del BOOKS[book_name]
    return f"Book {book_name} deleted"