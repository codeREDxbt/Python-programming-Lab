"""
Project: Library Inventory Manager (Single File)
Author: Vinayak [2501730150]
Course: Programming for Problem Solving using Python

Features:
- Book class with issue/return and dict conversion
- LibraryInventory with add/search/display and JSON persistence
- Robust CLI with input validation
- Logging with INFO/ERROR
- Saves catalog to library_catalog.json alongside this file
"""

import json
import logging
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CATALOG_FILE = Path(__file__).parent / "library_catalog.json"

class Book:
    def __init__(self, title: str, author: str, isbn: str, status: str = "available"):
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.status = status.strip().lower() if status else "available"
        if self.status not in {"available", "issued"}:
            self.status = "available"

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    def issue(self) -> bool:
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self) -> bool:
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self) -> bool:
        return self.status == "available"


class LibraryInventory:
    def __init__(self, filepath: Path = CATALOG_FILE):
        self.filepath = Path(filepath)
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        try:
            if not self.filepath.exists():
                logging.info("Catalog file not found. Starting with empty inventory.")
                self.books = []
                return
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise json.JSONDecodeError("Catalog root is not a list", doc=str(data), pos=0)
                self.books = [Book(**item) for item in data]
                logging.info("Catalog loaded: %d books", len(self.books))
        except (json.JSONDecodeError, OSError) as e:
            logging.error("Failed to load catalog: %s. Starting empty.", e)
            self.books = []

    def save_books(self) -> None:
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
            logging.info("Catalog saved (%d books).", len(self.books))
        except OSError as e:
            logging.error("Failed to save catalog: %s", e)

    def add_book(self, title: str, author: str, isbn: str) -> Optional[Book]:
        title, author, isbn = title.strip(), author.strip(), isbn.strip()
        if not title or not author or not isbn:
            logging.error("All fields (title, author, isbn) are required.")
            return None
        if any(b.isbn == isbn for b in self.books):
            logging.error("Book with ISBN %s already exists.", isbn)
            return None
        book = Book(title, author, isbn)
        self.books.append(book)
        self.save_books()
        logging.info("Added book: %s", book)
        return book

    def search_by_title(self, title: str) -> List[Book]:
        t = title.strip().lower()
        return [b for b in self.books if t in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        i = isbn.strip()
        for b in self.books:
            if b.isbn == i:
                return b
        return None

    def display_all(self) -> None:
        if not self.books:
            print("The library is empty.")
            return
        print("\n=== All Books ===")
        for b in self.books:
            print(b)


def prompt_non_empty(label: str) -> str:
    while True:
        s = input(f"{label}: ").strip()
        if s:
            return s
        print(f"{label} cannot be empty.")


def main() -> None:
    inventory = LibraryInventory()
    while True:
        print("\n--- Library Inventory Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search by Title")
        print("6. Search by ISBN")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == '1':
                title = prompt_non_empty("Enter title")
                author = prompt_non_empty("Enter author")
                isbn = prompt_non_empty("Enter ISBN")
                inventory.add_book(title, author, isbn)
            elif choice == '2':
                isbn = prompt_non_empty("Enter ISBN to issue")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_books()
                    print(f"Issued: {book.title}")
                else:
                    print("Book not found or already issued.")
            elif choice == '3':
                isbn = prompt_non_empty("Enter ISBN to return")
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    inventory.save_books()
                    print(f"Returned: {book.title}")
                else:
                    print("Book not found or not issued.")
            elif choice == '4':
                inventory.display_all()
            elif choice == '5':
                title = prompt_non_empty("Enter title to search")
                results = inventory.search_by_title(title)
                if results:
                    print("\n=== Search Results ===")
                    for b in results:
                        print(b)
                else:
                    print("No books match that title.")
            elif choice == '6':
                isbn = prompt_non_empty("Enter ISBN to search")
                book = inventory.search_by_isbn(isbn)
                if book:
                    print(book)
                else:
                    print("No book found with that ISBN.")
            elif choice == '7':
                print("Goodbye.")
                break
            else:
                print("Invalid choice. Please select 1-7.")
        except Exception as e:
            logging.error("Unexpected error: %s", e)


if __name__ == "__main__":
    main()
