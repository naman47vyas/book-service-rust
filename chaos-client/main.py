#!/usr/bin/env python3
import requests
import random
import json
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SERVER_URL = "http://localhost:8080"

# Sample book data for creating new books
SAMPLE_BOOKS = [
    {"title": "The Rust Programming Language", "author": "Steve Klabnik", "published_year": 2018, "genre": "Programming", "isbn": "978-1718500440"},
    {"title": "Eloquent JavaScript", "author": "Marijn Haverbeke", "published_year": 2018, "genre": "Programming", "isbn": "978-1593279509"},
    {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "published_year": 1979, "genre": "Science Fiction", "isbn": "978-0345391803"},
    {"title": "1984", "author": "George Orwell", "published_year": 1949, "genre": "Dystopian", "isbn": "978-0451524935"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "published_year": 1960, "genre": "Fiction", "isbn": "978-0061120084"},
]

# Tracking book IDs we've created
book_ids = []

def get_all_books():
    """Get all books - simple GET request"""
    try:
        response = requests.get(f"{SERVER_URL}/books")
        if response.status_code == 200:
            logger.info(f"Successfully retrieved all books ({len(response.json())} books)")
            # Update our known book IDs
            global book_ids
            book_ids = [book["id"] for book in response.json()]
        else:
            logger.warning(f"Failed to get books: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while getting books: {e}")

def get_book_by_id(book_id=None):
    """Get a specific book by ID"""
    # If no ID provided and we know about some books, use one of those
    if book_id is None and book_ids:
        book_id = random.choice(book_ids)
    # If we still don't have an ID, use 1 (which may or may not exist)
    if book_id is None:
        book_id = 1
    
    try:
        response = requests.get(f"{SERVER_URL}/books/{book_id}")
        if response.status_code == 200:
            logger.info(f"Successfully retrieved book {book_id}: {response.json()['title']}")
        else:
            logger.warning(f"Failed to get book {book_id}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while getting book {book_id}: {e}")

def create_book(valid=True):
    """Create a new book - POST request"""
    if valid:
        # Create a valid book
        book_data = random.choice(SAMPLE_BOOKS).copy()
        # Add some randomness to the title
        book_data["title"] = f"{book_data['title']} - {random.randint(1000, 9999)}"
    else:
        # Create an invalid book (missing required fields)
        book_data = {
            "title": "Incomplete Book"
            # Missing required author field
        }
    
    try:
        response = requests.post(f"{SERVER_URL}/books", json=book_data)
        if response.status_code == 201:  # Created
            new_book = response.json()
            book_ids.append(new_book["id"])
            logger.info(f"Successfully created book: {new_book['title']} with ID {new_book['id']}")
        else:
            logger.warning(f"Failed to create book: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while creating book: {e}")

def update_book(valid=True):
    """Update a book - PUT request"""
    if not book_ids:
        logger.warning("No books to update, skipping update operation")
        return
    
    book_id = random.choice(book_ids)
    
    if valid:
        # Valid update data
        update_data = {
            "title": f"Updated Title - {datetime.now().strftime('%H:%M:%S')}"
        }
    else:
        # Send malformed JSON to trigger error
        try:
            response = requests.put(
                f"{SERVER_URL}/books/{book_id}", 
                data="This is not valid JSON",
                headers={"Content-Type": "application/json"}
            )
            logger.warning(f"Sent invalid JSON to update book {book_id}: {response.status_code} - {response.text}")
            return
        except Exception as e:
            logger.error(f"Exception while sending invalid update: {e}")
            return
    
    try:
        response = requests.put(f"{SERVER_URL}/books/{book_id}", json=update_data)
        if response.status_code == 200:
            logger.info(f"Successfully updated book {book_id}")
        else:
            logger.warning(f"Failed to update book {book_id}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while updating book {book_id}: {e}")

def delete_book(valid=True):
    """Delete a book - DELETE request"""
    if not book_ids:
        logger.warning("No books to delete, skipping delete operation")
        return
    
    if valid and book_ids:
        # Delete a book we know exists
        book_id = random.choice(book_ids)
    else:
        # Try to delete a non-existent book
        book_id = max(book_ids) + 100 if book_ids else 9999
    
    try:
        response = requests.delete(f"{SERVER_URL}/books/{book_id}")
        if response.status_code == 204:  # No Content
            logger.info(f"Successfully deleted book {book_id}")
            if book_id in book_ids:
                book_ids.remove(book_id)
        else:
            logger.warning(f"Failed to delete book {book_id}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while deleting book {book_id}: {e}")

def send_wrong_method():
    """Send a request with the wrong HTTP method"""
    try:
        response = requests.patch(f"{SERVER_URL}/books/1", json={"title": "This won't work"})
        logger.warning(f"Sent PATCH request (should fail): {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while sending wrong method: {e}")

def request_nonexistent_endpoint():
    """Request a non-existent endpoint"""
    try:
        response = requests.get(f"{SERVER_URL}/not_books")
        logger.warning(f"Requested non-existent endpoint: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while requesting non-existent endpoint: {e}")

def send_request():
    """Send a random request, 75% valid, 25% erroneous"""
    get_all_books()  # Always update our known book IDs first
    
    # Determine if this should be a valid request (75%) or an error (25%)
    valid = random.random() < 0.75
    
    # Pick a random operation
    operations = []
    
    # Valid operations
    if valid:
        operations = [
            lambda: get_book_by_id(),
            lambda: create_book(True),
            lambda: update_book(True),
            lambda: delete_book(True)
        ]
    # Error-inducing operations
    else:
        operations = [
            lambda: get_book_by_id(999999),  # Non-existent ID
            lambda: create_book(False),      # Invalid book data
            lambda: update_book(False),      # Malformed JSON
            lambda: delete_book(False),      # Delete non-existent book
            send_wrong_method,              # Wrong HTTP method
            request_nonexistent_endpoint    # Non-existent endpoint
        ]
    
    # Execute a random operation
    operation = random.choice(operations)
    operation()

def main():
    """Main function to continuously send requests"""
    logger.info("Starting chaos client for Book Library API")
    
    # Create a few books to start with
    for _ in range(3):
        create_book(True)
    
    request_count = 0
    try:
        while True:
            send_request()
            request_count += 1
            
            # Log a summary every 20 requests
            if request_count % 20 == 0:
                logger.info(f"Sent {request_count} requests so far. Currently tracking {len(book_ids)} books.")
            
            # Random delay between 0.5 and 2 seconds
            time.sleep(random.uniform(0.5, 2))
    except KeyboardInterrupt:
        logger.info("Chaos client stopped by user. Exiting.")

if __name__ == "__main__":
    main()
