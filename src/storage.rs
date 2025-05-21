use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use crate::models::{Book, CreateBookDto, UpdateBookDto};

// Our database type
pub type DbType = Arc<RwLock<HashMap<u32, Book>>>;

// BookRepository manages all operations on our book storage
#[derive(Clone)]
pub struct BookRepository {
    // The database instance
    db: DbType,
    // Counter for generating unique IDs
    next_id: Arc<RwLock<u32>>,
}

impl BookRepository {
    // Create a new repository instance
    pub fn new() -> Self {
        BookRepository {
            db: Arc::new(RwLock::new(HashMap::new())),
            next_id: Arc::new(RwLock::new(1)),
        }
    }

    // Get all books
    pub fn get_all(&self) -> Vec<Book> {
        // Acquire a read lock
        let db_read = self.db.read().unwrap();
        // Clone and collect all books into a vector
        db_read.values().cloned().collect()
    }

    // Get book by ID
    pub fn get_by_id(&self, id: u32) -> Option<Book> {
        let db_read = self.db.read().unwrap();
        db_read.get(&id).cloned()
    }

    // Create a new book
    pub fn create(&self, create_dto: CreateBookDto) -> Book {
        // Generate a new ID
        let mut id_write = self.next_id.write().unwrap();
        let id = *id_write;
        *id_write += 1;
        
        // Create the new book
        let book = Book {
            id,
            title: create_dto.title,
            author: create_dto.author,
            published_year: create_dto.published_year,
            genre: create_dto.genre,
            isbn: create_dto.isbn,
        };
        
        // Store the book
        let mut db_write = self.db.write().unwrap();
        db_write.insert(id, book.clone());
        
        book
    }

    // Update an existing book
    pub fn update(&self, id: u32, update_dto: UpdateBookDto) -> Option<Book> {
        let mut db_write = self.db.write().unwrap();
        
        if let Some(book) = db_write.get_mut(&id) {
            // Update fields if provided
            if let Some(title) = update_dto.title {
                book.title = title;
            }
            if let Some(author) = update_dto.author {
                book.author = author;
            }
            book.published_year = update_dto.published_year;
            book.genre = update_dto.genre;
            book.isbn = update_dto.isbn;
            
            Some(book.clone())
        } else {
            None
        }
    }

    // Delete a book
    pub fn delete(&self, id: u32) -> bool {
        let mut db_write = self.db.write().unwrap();
        db_write.remove(&id).is_some()
    }
}
