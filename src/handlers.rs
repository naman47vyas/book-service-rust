use actix_web::{web, HttpResponse, Responder};
use crate::models::{CreateBookDto, UpdateBookDto};
use crate::storage::BookRepository;

// Get all books
pub async fn get_books(repo: web::Data<BookRepository>) -> impl Responder {
    let books = repo.get_all();
    HttpResponse::Ok().json(books)
}

// Get book by ID
pub async fn get_book(
    repo: web::Data<BookRepository>,
    path: web::Path<u32>,
) -> impl Responder {
    let id = path.into_inner();
    
    match repo.get_by_id(id) {
        Some(book) => HttpResponse::Ok().json(book),
        None => HttpResponse::NotFound().body(format!("Book with ID {} not found", id)),
    }
}

// Create a new book
pub async fn create_book(
    repo: web::Data<BookRepository>,
    book_dto: web::Json<CreateBookDto>,
) -> impl Responder {
    let book = repo.create(book_dto.into_inner());
    HttpResponse::Created().json(book)
}

// Update a book
pub async fn update_book(
    repo: web::Data<BookRepository>,
    path: web::Path<u32>,
    book_dto: web::Json<UpdateBookDto>,
) -> impl Responder {
    let id = path.into_inner();
    
    match repo.update(id, book_dto.into_inner()) {
        Some(book) => HttpResponse::Ok().json(book),
        None => HttpResponse::NotFound().body(format!("Book with ID {} not found", id)),
    }
}

// Delete a book
pub async fn delete_book(
    repo: web::Data<BookRepository>,
    path: web::Path<u32>,
) -> impl Responder {
    let id = path.into_inner();
    
    if repo.delete(id) {
        HttpResponse::NoContent().finish()
    } else {
        HttpResponse::NotFound().body(format!("Book with ID {} not found", id))
    }
}
