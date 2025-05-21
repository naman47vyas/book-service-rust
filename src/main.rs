mod models;
mod storage;
mod handlers;

use actix_web::{web, App, HttpServer};
use storage::BookRepository;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Create the repository instance
    let repo = BookRepository::new();
    
    println!("Server starting at http://127.0.0.1:8080");
    
    // Start the HTTP server
    HttpServer::new(move || {
        App::new()
            // Share the repository with all handlers
            .app_data(web::Data::new(repo.clone()))
            // Define API routes
            .service(
                web::scope("/books")
                    .route("", web::get().to(handlers::get_books))
                    .route("", web::post().to(handlers::create_book))
                    .route("/{id}", web::get().to(handlers::get_book))
                    .route("/{id}", web::put().to(handlers::update_book))
                    .route("/{id}", web::delete().to(handlers::delete_book))
            )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
