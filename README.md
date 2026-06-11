# library-api project


## Project Description:

Build an API server using FastAPI
that connects to a MySQL database
and manages a system of books and
library members.

## Technologies Used

- Python
- FastAPI
- MySQL
- Docker
- Pydantic


## Folder structure:
```
library-api/
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   └── app.log
├── README.md
├── requirements.txt
└── .gitignore
```
## Installation

**What to write:**  
List the step-by-step instructions for installing your project on a new computer.

**Why this section exists:**  
This helps anyone who wants to run your project get it set up correctly.

**Example structure:**

1. Clone the repository:
```bash
https://github.com/asherpirov/libraryproject.git```



2. Install dependencies:
```bash
pip install fastapi uvicorn pydantic 
```
## docker container script:

```bash
docker run --name library-mysql
-e MYSQL_ROOT_PASSWORD=secret
-e MYSQL_DATABASE=library_db
-p 3306:3306
-d mysql:latest
```
**Database Information:**

**Database Name:** library_db

## Database Tables

### Table: `books`

| Column Name             | Data Type                                              | Constraints                          | Description                                                                                             |
|-------------------------|--------------------------------------------------------|--------------------------------------|---------------------------------------------------------------------------------------------------------|
| `id`                    | `INT`                                                  | `PRIMARY KEY AUTO_INCEREMENT` | `Unique identifier`                                                                                     |
| `title`                 | `VARCHAR(50)`                                          | `NOT NULL` | `Book title, non-empty column, maximum 50 characters`                                                   |
| `author`                | `VARCHAR(50)`                                          | `NOT NULL` | `Author name, non-empty column, maximum 50 characters`                                                  |
| `genre`                 | ` ENUM(Fiction ,Non-Fiction ,Science ,History ,Other)` | `NOT NULL` | ` Allowed genre values: Fiction, Nonfiction, Science, History, Other ,Any other value returns an error` |
| `is_available`          | `BOOLEAN`                                              | `NOT NULL`| `Is the book available for loan FALSE indicates loaned`                                                 |
| `borrowed_by_member_id` |`INT`|| `The ID of the memeber holding the book`                                                                |


### Table: `members`

| Column Name    | Data Type | Constraints                   | Description                                  |
|----------------|-----------|-------------------------------|----------------------------------------------|
| `id`           | `INT` | `PRIMARY KEY AUTO_INCEREMENT` | `Unique identifier`                          |
| `name`         |`VARCHAR(50)` | `NOT NULL`                    | `member's name`                              |
| `email`        | `VARCHAR(50)`| `UNIQUE NOT NULL`             | `member's email`                             |
| `is_active`    | `BOOLEAN`| `NOT NULL DEAULT 1`           | `If the member active — FALSE - Cannot lend` |
| `total_borrows` | `INT`| `NOT NULL DEAULT 0`           |    `Total number of lends - increases by 1 for each lend`|


## System Rules
1. ***creating a book*** -> the user send post with title/author/genre
adds is_available=True, borrowed by=NULL 
2. ***genre*** -> Must be Fiction / Non-Fiction / Science / History / Other — any other value returns an error.
Must be verified on both POST and PUT.
3. ***creating a member*** -> User sends name/email — system adds is_active=True, total_borrows=0
4. ***email*** -> Must be unique — if it already exists returns an error
5. ***Inactive member*** -> If is_active=False — book cannot be borrowed
6. ***Book unavailable*** -> It is not possible to borrow a book that is already borrowed (is_available=False)
7. ***Maximum books*** -> A member cannot hold more than 3 books at a time.
8. ***Returning a book*** -> A book can only be returned if it is lent to the same friend who is returning it.


## API Endpoints

### Books Endpoints

| Method | Endpoint                         | Description | Request Body          | Response                                                                                                                                                 |
|--------|----------------------------------|------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `POST` | `/books`                         | `create book` | `dict(NewBookModel)`  | `201(created) or 422(bad request)`                                                                                                                       |
| `GET`  | `/books`                         |`all books` |     | `200 or 404(not found)`                                                                                                                                  |
| `GET`  | `/books/{id}`                    |`book by id` |   | `200 or 404(not found)`                                                                                                                                  |
| `PUT`  | `/books/{id}`                    |`update book` | `dict(UpdateBookModel)` | `200(ok) or 400`                                                                                                                                         |
| `PUT`  | `/books/{id}/borrow/{member_id}` | `Lending a book to a member`|   | `200(Ok)` ,`404(book or member not found)`, `400(The member is inactive or has borrowed 3 books or the book is borrowed.)`                               |
| `PUT`  | `/books/{id}/return/{member_id}` |`Returning a book from a member` |   | `200(Ok)` ,`404(book or member not found)`, `400(The book is actually currently on loan or is the book on loan to the same friend who is returning it.)` |

### Members Endpoints
| Method | Endpoint                         | Description           | Request Body              | Response                                                                                                                                            |
|--------|----------------------------------|-----------------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `POST` | `/members`                         | `create member`       | `dict(NewMemberModel)`    | `201(created) or 422(bad request)`                                                                                                                  |
| `GET`  | `/members`                         | `all members`         |                           | `200 or 404(not found)`                                                                                                                             |
| `GET`  | `/members/{id}`                    | `member by id`        |                           | `200 or 404(id not found)`                                                                                                                          |
| `PUT`  | `/members/{id}`                    | `update member`       | `dict(UpdateMemberModel)` | `200(ok) or 404(id not found) or 400(Updating an email that already exists in the system)`                                                          |
| `PUT`  | `/members/{id}/deactivate` | `deactivate a member` |                           | `200(Ok)` ,`404(member not found)` |
| `PUT`  | `/members/{id}/activate` | `activate a member`  |                           | `200(Ok)` ,`404(member not found)`|



### Reports Endpoints
| Method | Endpoint                         | Description           | Request Body            | Response|
|--------|----------------------------------|-----------------------|-------------------------|-------------|
| `GET`  | `/reports/summary`| `General report`|  | `200 or 404(not found)`|
| `GET`  | `/reports/books-by-genre`| `Books by genre`|  | `200 or 404(not found)`|
| `GET`  | `/reports/top-member`| `The most active member`|  | `200(ok) or 404(id not found)`|

## System Flow

1. **Server Startup:**
   - The server connects to MySQL
   - Creates tables if they don't exist
   - Starts the FastAPI server

2. **Creating a Member:**
   - User sends POST request to `/members` with name and email
   - System validates the email is unique
   - System creates member with `is_active=True` and `total_borrows=0`
   - Returns the created member

3. **Creating a Book:**
   - User sends POST request to `/books` with title, author, genre
   - System validates the genre 
   - System creates book with `is_available=True` and `borrowed_by=NULL`
   - Returns the created book
   
4. **Borrowing a Book:**
   - User sends PUT request to `/books/{id}/borrow/{member_id}`
   - System checks if book exists
   - System checks if member exists and is active
   - System checks if book is available
   - System checks if member has less than 3 books
   - Updates book: `is_available=False`, `borrowed_by_member_id=member_id`
   - Increments member's `total_borrows` by 1
   - Returns success message