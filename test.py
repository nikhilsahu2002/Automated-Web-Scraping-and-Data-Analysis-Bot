import aiohttp
import asyncio
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

async def fetch_quotes(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching quotes from {url}: {e}")
        return None

async def get_quotes_async(url):
    async with aiohttp.ClientSession() as session:
        html_content = await fetch_quotes(session, url)

        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            quotes = [quote.text for quote in soup.find_all('span', class_='text')]
            return quotes
        else:
            return None

async def clean_and_transform_quotes_async(quotes):
    try:
        # Simulate some asynchronous processing
        await asyncio.sleep(1)

        # Remove leading and trailing whitespaces from each quote
        cleaned_quotes = [quote.strip() for quote in quotes]

        # Remove empty quotes
        cleaned_quotes = [quote for quote in cleaned_quotes if quote]

        return cleaned_quotes
    except Exception as e:
        print(f"Error cleaning and transforming quotes: {e}")
        return None

async def get_dynamic_quotes_async(url):
    quotes = []

    # Load the initial page
    async with aiohttp.ClientSession() as session:
        response = await fetch_quotes(session, url)
        if not response:
            return None

        soup = BeautifulSoup(response, 'html.parser')
        quotes.extend([quote.text.strip() for quote in soup.find_all('span', class_='text')])

        # Simulate AJAX requests to load more quotes
        page = 1  # Assuming there are multiple pages, adjust as needed
        while True:
            ajax_url = f"{url}/page/{page}/"
            ajax_response = await fetch_quotes(session, ajax_url)

            if not ajax_response:
                break

            ajax_soup = BeautifulSoup(ajax_response, 'html.parser')
            new_quotes = [quote.text.strip() for quote in ajax_soup.find_all('span', class_='text')]
            if not new_quotes:
                break  # No more quotes to load
            quotes.extend(new_quotes)
            page += 1

    return quotes

def generate_wordcloud(quotes):
    text = " ".join(quotes)
    wordcloud = WordCloud(width=800, height=400, max_words=200, background_color="white").generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def save_to_csv(quotes, filename='quotes_dataset.csv'):
    dates = [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(len(quotes))]
    df = pd.DataFrame({'Date': dates, 'Quote': quotes})
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")

async def main():
    target_url = "http://quotes.toscrape.com"

    try:
        # Using asyncio to fetch quotes asynchronously
        regular_quotes_task = get_quotes_async(target_url)

        # Dynamic approach without Selenium
        dynamic_quotes_task = get_dynamic_quotes_async(target_url)

        # Wait for all tasks to complete
        regular_quotes = await regular_quotes_task
        dynamic_quotes = await dynamic_quotes_task

        if regular_quotes:
            # Clean and transform quotes asynchronously
            cleaned_regular_quotes_task = clean_and_transform_quotes_async(regular_quotes)
            cleaned_regular_quotes = await cleaned_regular_quotes_task

            if cleaned_regular_quotes:
                print("\nCleaned and Transformed Quotes using regular approach:")
                for i, quote in enumerate(cleaned_regular_quotes, 1):
                    print(f"{i}. {quote}")

                # Generate word cloud
                generate_wordcloud(cleaned_regular_quotes)

                # Save dataset to CSV
                save_to_csv(cleaned_regular_quotes, 'regular_quotes_dataset.csv')

        if dynamic_quotes:
            # Clean and transform quotes asynchronously
            cleaned_dynamic_quotes_task = clean_and_transform_quotes_async(dynamic_quotes)
            cleaned_dynamic_quotes = await cleaned_dynamic_quotes_task

            if cleaned_dynamic_quotes:
                print("\nCleaned and Transformed Quotes using dynamic approach without Selenium:")
                for i, quote in enumerate(cleaned_dynamic_quotes, 1):
                    print(f"{i}. {quote}")

                # Generate word cloud
                generate_wordcloud(cleaned_dynamic_quotes)

                # Save dataset to CSV
                save_to_csv(cleaned_dynamic_quotes, 'dynamic_quotes_dataset.csv')

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
