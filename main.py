import json

# --- Trie for searching book titles ---
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.titles = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, title):
        node = self.root
        for char in title.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.titles.append(title)
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        return list(set(node.titles))


# --- Book System ---
class BookRecommender:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = []
        self.ratings = {}
        self.trie = Trie()
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.books = data.get("books", [])
                self.ratings = data.get("ratings", {})
                for book in self.books:
                    self.trie.insert(book["title"])
        except FileNotFoundError:
            self.books = []
            self.ratings = {}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump({"books": self.books, "ratings": self.ratings}, file, indent=4)

    def add_book(self):
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        genre = input("Enter book genre: ")
        book = {"title": title, "author": author, "genre": genre}
        self.books.append(book)
        self.trie.insert(title)
        self.save_data()
        print("Book added.")

    def view_books(self):
        if not self.books:
            print("No books available.")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")

    def rate_book(self):
        username = input("Enter your username: ")
        self.view_books()
        if not self.books:
            return
        try:
            choice = int(input("Enter the number of the book you want to rate: ")) - 1
            rating = int(input(f"Enter your rating for {self.books[choice]['title']} (1–5): "))
            if username not in self.ratings:
                self.ratings[username] = {}
            self.ratings[username][self.books[choice]['title']] = rating
            self.save_data()
            print("Rating submitted.")
        except (IndexError, ValueError):
            print("Invalid selection.")

    def recommend_books(self):
        username = input("Enter your username: ")
        if username not in self.ratings:
            print("No ratings found. Please rate books first.")
            return

        rated_titles = set(self.ratings[username].keys())
        preferred_genres = [book["genre"] for book in self.books if book["title"] in rated_titles]
        genre_counts = {g: preferred_genres.count(g) for g in set(preferred_genres)}

        recommended = []
        for book in self.books:
            if book["title"] not in rated_titles and genre_counts.get(book["genre"], 0) > 0:
                recommended.append(book)

        if recommended:
            print("Recommendations:")
            for book in recommended:
                print(f"Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")
        else:
            print("No recommendations available.")

    def search_books(self):
        prefix = input("Enter book title prefix: ")
        results = self.trie.search_prefix(prefix)
        if results:
            print("Search Results:")
            for title in results:
                for book in self.books:
                    if book["title"] == title:
                        print(f"Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")
        else:
            print("No matches found.")

    def run(self):
        while True:
            print("\nOptions:")
            print("1. Add Book")
            print("2. View Books")
            print("3. Rate Book")
            print("4. Get Recommendations")
            print("5. Search Books")
            print("6. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.view_books()
            elif choice == "3":
                self.rate_book()
            elif choice == "4":
                self.recommend_books()
            elif choice == "5":
                self.search_books()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


# --- Run the app ---
if __name__ == "__main__":
    app = BookRecommender()
    app.run()
