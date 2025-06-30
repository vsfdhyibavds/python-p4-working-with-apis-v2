import requests
import json


class Search:
    """
    A class to interact with the Open Library Search API.
    """

    def get_search_results(self, search_term="the lord of the rings", fields=None, limit=1):
        """
        Get raw content response from the Open Library API for a given search term.

        Args:
            search_term (str): The book title to search for.
            fields (list): List of fields to include in the response.
            limit (int): Number of results to limit the response to.

        Returns:
            bytes: Raw content of the response.
        """
        if fields is None:
            fields = ["title", "author_name"]

        search_term_formatted = search_term.replace(" ", "+")
        fields_formatted = ",".join(fields)

        URL = f"https://openlibrary.org/search.json?title={search_term_formatted}&fields={fields_formatted}&limit={limit}"

        try:
            response = requests.get(URL)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error fetching data from Open Library API: {e}")
            return None

    def get_search_results_json(self, search_term="the lord of the rings", fields=None, limit=1):
        """
        Get JSON response from the Open Library API for a given search term.

        Args:
            search_term (str): The book title to search for.
            fields (list): List of fields to include in the response.
            limit (int): Number of results to limit the response to.

        Returns:
            dict or None: Parsed JSON response or None if error occurs.
        """
        if fields is None:
            fields = ["title", "author_name"]

        search_term_formatted = search_term.replace(" ", "+")
        fields_formatted = ",".join(fields)

        URL = f"https://openlibrary.org/search.json?title={search_term_formatted}&fields={fields_formatted}&limit={limit}"
        print(f"Requesting URL: {URL}")

        try:
            response = requests.get(URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from Open Library API: {e}")
            return None

    def get_user_search_results(self, search_term, fields=None, limit=1):
        """
        Get formatted search result string for a user-provided search term.

        Args:
            search_term (str): The book title to search for.
            fields (list): List of fields to include in the response.
            limit (int): Number of results to limit the response to.

        Returns:
            str: Formatted string with title and author or error message.
        """
        if fields is None:
            fields = ["title", "author_name"]

        response = self.get_search_results_json(search_term, fields, limit)
        if response is None:
            return "Failed to retrieve data from the API."

        docs = response.get("docs")
        if not docs:
            return "No results found."

        try:
            title = docs[0].get("title", "N/A")
            author = docs[0].get("author_name", ["N/A"])[0]
            return f"Title: {title}\nAuthor: {author}"
        except (IndexError, KeyError, TypeError):
            return "Error processing the API response."


if __name__ == "__main__":
    search_term = input("Enter a book title: ")
    searcher = Search()
    result = searcher.get_user_search_results(search_term)
    print("Search Result:\n")
    print(result)
