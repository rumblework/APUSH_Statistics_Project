import pandas as pan
import matplotlib.pyplot as m
import urllib.request as req
from PyPDF2 import PdfReader
import io
import re

linkData = []
linkDataHTML = []
# year_pattern = r'\b\d{4}\b'
# years = re.findall(year_pattern, text)



categories = {
    "Document Based Questions": ["Document-Based Question", "DBQ", "Documents"],
    "Long Essay Question": ["LEQ", "Long Essay", "Long-Answer", "Long-Essay", "Question 2 "],
    "Short Answer Questions": ["SAQ", "Short-response", "Short-answer", "SECTION I, Part B"]
}

year_ranges = [(1491, 1607), (1607, 1754), (1754, 1800), (1800, 1848), (1844, 1877), (1865, 1898), (1890, 1945), (1945,
                1980),(1980, 2050)]  # Define year ranges

def plot_results(occurrences):
    # Convert the nested dictionary into a flat structure for a DataFrame
    data = []
    for keyword, ranges in occurrences.items():
        for year_range, count in ranges.items():
            data.append({"Keyword": keyword, "Year Range": f"{year_range[0]}-{year_range[1]}", "Count": count})

    # Create a DataFrame
    df = pan.DataFrame(data)

    # Pivot the DataFrame to prepare for plotting
    pivot_df = df.pivot(index="Year Range", columns="Keyword", values="Count").fillna(0)

    # Plot the data
    pivot_df.plot(kind="bar", stacked=True, figsize=(10, 6))
    m.title("Keyword Occurrences by Year Range")
    m.xlabel("Year Range")
    m.ylabel("Count")
    m.legend(title="Keyword")
    m.tight_layout()
    m.show()

def search_keywords_in_pdf(text, categories, ranges):
    """
    Counts occurrences of years within specific ranges for each category of keywords.

    :param text: The input text to search.
    :param categories: Dictionary where keys are category names and values are lists of keywords.
    :param ranges: List of tuples defining year ranges (e.g., [(1900, 1999), (2000, 2099)]).
    :return: Nested dictionary mapping categories to range counts.
    """
    # Flatten categories into a keyword-to-category map
    keyword_to_category = {
        keyword: category for category, keywords in categories.items() for keyword in keywords
    }
    keyword_pattern = '|'.join(map(re.escape, keyword_to_category.keys()))  # Build regex for all keywords
    combined_pattern = rf"({keyword_pattern})|(\b\d{{4}}\b)"  # Match keywords or four-digit years

    # Initialize nested counters for each category and range
    category_range_counts = {category: {r: 0 for r in ranges} for category in categories}

    for page in text:
        matches = list(re.finditer(combined_pattern, page))


        last_category = None

        for match in matches:
            if match.group(1):  # Match is a keyword
                keyword = match.group(1)
                last_category = keyword_to_category[keyword]  # Map keyword to its category
            elif match.group(2):  # Match is a four-digit year
                year = int(match.group(2))
                if last_category:
                    # Determine which range the year falls into and increment the corresponding category count
                    for r in ranges:
                        if r[0] <= year <= r[1]:
                            category_range_counts[last_category][r] += 1
                            break  # Only increment one range for a given year

    return category_range_counts

def main():
    fileData = open("urls").readlines()  # List of PDF URLs

    with open("output", "w") as outputFile:  # Open output file for writing
        for url in fileData:
            try:
                # Fetch the PDF from the URL
                pdf_response = req.urlopen(
                    req.Request(url.strip(), headers={"User-Agent": "Mozilla/5.0"})
                ).read()

                pdf_reader = PdfReader(io.BytesIO(pdf_response))  # Load PDF into reader

                pdf = []

                for i, page in enumerate(pdf_reader.pages):
                    pdf.append(page.extract_text())

                # Search for keywords in the PDF
                keyword_occurrences = search_keywords_in_pdf(pdf, categories, year_ranges)

                # Log results
                print(f"Results for {url.strip()}:", file=outputFile)
                for keyword, count in keyword_occurrences.items():
                    print(f"  {keyword}: {count} occurrences", file=outputFile)
                print(f"Processed {url.strip()} successfully.")

            except Exception as e:
                print(f"Error processing URL {url.strip()}: {e}")

            plot_results(keyword_occurrences)


main()