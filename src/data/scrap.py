import yaml
import csv
import requests
import logging
import tempfile
import warnings
from pathlib import Path

from tqdm import tqdm
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

logging.basicConfig(
    format= "%(asctime)s [%(levelname)s] \
				%(funcName)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger()

# get configurations from config.yml
config_file_path = Path(__file__).parents[2]/ "config.yml"
with open(config_file_path) as config_file:
    configurations = yaml.safe_load(config_file)

# yoruba alphabets
alphabet = [
    "a", "b", "d", "e", "ẹ", "f", "g", "gb", "h", "i", "j", "k", "l",
    "m", "n", "o", "ọ", "p", "r", "s", "ṣ", "t", "u", "w", "y"
            ]


def get_page(url: str):
    """Gets the url page requested for"""
    page = ""
    try:
        page = requests.get(url, verify=False)
        logger.info(f"{url} retreived successfully")
    except requests.ConnectionError as err:
        logger.error(f"A connection Error occured: {err}")
    except requests.HTTPError as err:
        logger.error(f"An HTTP error occured: {err}")
    except requests.Timeout:
        logger.error(f"Connection timed out")
    except requests.RequestException as err:
        logger.error(f"An unknown error occured: {err}")
    return page


def save_file(web_page: str):
    """Create a temp file to save the content retrieved from the internet"""

    file = tempfile.NamedTemporaryFile("w+", delete=False)
    file.write(web_page)
    file.seek(0)
    logger.info(f"page saved as temporary file to {file.name}")
    return file


def extract_info(page: str, csv_writer: object):
    """Extracts and returns the desired information only"""
    # define soup object
    soup = BeautifulSoup(page, "html.parser")
    # get page title
    logger.info(f"Page title: {soup.title}")
    # get the content of the page
    content_n = soup.select(".alphabet-listing")[0].find_all("a")
    # print(content_n, "Len of content: ", len(content_n))
    for i, p in enumerate(content_n):
        # write down the name and it meaning
        csv_writer.writerow([p.string, p.get("title")])
    logger.info("Page completely written...")
    

def create_csv(file_address: str, header=None):
    """Create a csv file to save the hymns content into"""
    file = open(file_address, "w+")
    csv_writer = csv.writer(file)
    if header != None:
        csv_writer.writerow(header)
    logger.info("File and csv_writer created successfully")
    return file, csv_writer



def main():
    file, csv_writer = create_csv(configurations["file_name"], ["Name", "Meaning"])
    for alpha in alphabet:
        try:
            address = configurations['url']
            page = get_page(f"{address}/{alpha}")
            # file = save_file(page.text)
            hymn = extract_info(file, csv_writer=csv_writer)
        except Exception as err:
            logger.error(f"An error occured at iteration. Error message: {err}")

if __name__ == "__main__":
    main()
