
# import requests
# from bs4 import BeautifulSoup

# def get_quotes(url):
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         quotes = []

#         for quote in soup.find_all('span', class_='text'):
#             quotes.append(quote.text)

#         return quotes
#     else:
#         print(f"Failed to retrieve quotes. Status code: {response.status_code}")
#         return None

# if __name__ == "__main__":
#     target_url = "http://quotes.toscrape.com"
#     result = get_quotes(target_url)

#     if result:
#         for i, quote in enumerate(result, 1):
#             print(f"{i}. {quote}")

# /////////////////////////////////////////////////////////// Ajax
# import requests
# from bs4 import BeautifulSoup

# def get_dynamic_quotes(url):
#     quotes = []

#     # Load the initial page
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Failed to retrieve quotes. Status code: {response.status_code}")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')
#     quotes.extend([quote.text.strip() for quote in soup.find_all('span', class_='text')])

#     # Simulate AJAX requests to load more quotes
#     page = 1  # Assuming there are multiple pages, adjust as needed
#     while True:
#         ajax_url = f"{url}/page/{page}/"
#         ajax_response = requests.get(ajax_url)

#         if ajax_response.status_code == 200:
#             ajax_soup = BeautifulSoup(ajax_response.text, 'html.parser')
#             new_quotes = [quote.text.strip() for quote in ajax_soup.find_all('span', class_='text')]
#             if not new_quotes:
#                 break  # No more quotes to load
#             quotes.extend(new_quotes)
#             page += 1
#         else:
#             print(f"Failed to retrieve additional quotes. Status code: {ajax_response.status_code}")
#             break

#     return quotes

# if __name__ == "__main__":
#     target_url = "http://quotes.toscrape.com"
#     result = get_dynamic_quotes(target_url)

#     if result:
#         for i, quote in enumerate(result, 1):
#             print(f"{i}. {quote}")

# /////////////////////////////////////////////////////////////

