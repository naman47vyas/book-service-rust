use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Book {
    pub id: u32,
    pub title: String,
    pub author: String,
    pub published_year: Option<u16>,
    pub genre: Option<String>,
    pub isbn: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct CreateBookDto {
    pub title: String,
    pub author: String,
    pub published_year: Option<u16>,
    pub genre: Option<String>,
    pub isbn: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct UpdateBookDto {
    pub title: Option<String>,
    pub author: Option<String>,
    pub published_year: Option<u16>,
    pub genre: Option<String>,
    pub isbn: Option<String>,
}
