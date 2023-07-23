"""
OpenSCAD Examples Scraper
Author: OpenAI's ChatGPT
Date: July 23, 2023

Description:
This script is a web scraper designed to download OpenSCAD example code files from the OpenSCAD examples website.
It uses BeautifulSoup and requests libraries to parse HTML and fetch content. The scraper fetches code content
from the ".html" files using specific "<pre><code data-language="javascript">" structure. The code content is then
saved as separate ".scad" files in a directory structure similar to the HTML structure of the website. The script
utilizes the tqdm library to display a progress bar during the scraping process.

Prompts:
- Write a scraper for https://files.openscad.org/examples/ that extracts the <pre> code sections as files in a
  directory structure similar to the HTML structure.
- Add Google docstrings and type hints to the scraper.
- Wrap the scraper in a class called OpenScadExampleScraper.
- Ensure the code is ready for cut & paste and remove any unnecessary ellipsis ("...").
- The scraper should work with the provided HTML index structure.
- Fix the FileNotFoundError issue when downloading files by ensuring the output directory is set correctly.
- Add a tqdm progress bar to show the scraping progress.
- Include docstrings for each method in the class.
- Include a header with the author, date, and description of the script.
- Add the gist of the prompts that lead to this code in the header.
- The resulting files need to be .scad files
- we want a tqdm progress bar on file level 
- add a result message with total directories files and time the scraping took
"""

import os
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from typing import Optional

class OpenScadExampleScraper:
    """
    A web scraper to download OpenSCAD example code files from the website.

    Attributes:
        base_url (str): The base URL of the OpenSCAD examples website.
        output_directory (str): The directory to save the downloaded files.
    """

    def __init__(self):
        """
        Initialize the OpenScadExampleScraper.
        """
        self.base_url: str = "https://files.openscad.org/examples/"
        self.output_directory: str = "openscad_examples"

    def get_soup(self, url: str) -> BeautifulSoup:
        """
        Fetch the BeautifulSoup object for a given URL.

        Args:
            url (str): The URL to fetch and parse.

        Returns:
            BeautifulSoup: The BeautifulSoup object representing the parsed HTML content.
        """
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")

    def create_directory_if_not_exists(self, directory: str) -> None:
        """
        Create a directory if it does not exist.

        Args:
            directory (str): The path of the directory to create.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    def download_code_file(self, url: str, output_path: str) -> None:
        """
        Download a code file from a URL and save it to the specified output path.

        Args:
            url (str): The URL of the code file to download.
            output_path (str): The path to save the downloaded code file.
        """
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)

    def scrape_subdirectories(self, url: str) -> list:
        """
        Scrape subdirectories from the OpenSCAD examples website and return their names and URLs.

        Args:
            url (str): The URL of the main index page.

        Returns:
            list: A list of tuples containing the subdirectory name and URL.
        """
        soup = self.get_soup(url)
        links = soup.find_all("a")
        subdirectories = []
        for link in links:
            href = link.get("href")
            if href.endswith("/"):  # Subdirectory link
                subdir_url = url + href
                subdir_name = href.rstrip("/")
                subdirectories.append((subdir_name, subdir_url))
        return subdirectories

    def scrape_directory(self, url: str, current_directory: Optional[str] = "") -> int:
        """
        Scrape pre code sections from the OpenSCAD examples website and save them as files.

        Args:
            url (str): The URL of the page to scrape.
            current_directory (str, optional): The current directory path. Defaults to "".

        Returns:
            int: The number of files scraped in the current directory.
        """
        soup = self.get_soup(url)
        links = soup.find_all("a")
        file_links = [link for link in links if link.get("href").endswith(".html")]
        file_links_count = len(file_links)

        file_count = 0

        with tqdm(total=file_links_count, desc=f"Scraping {current_directory}", leave=False) as file_progress:
            for link in file_links:
                href = link.get("href")
                code_url = url + href
                code_content = self.get_code_content(code_url)
                if code_content:
                    file_name = href.split("/")[-1]
                    # Adjust file extension to .scad
                    file_name = file_name.replace(".html", ".scad")
                    file_path = os.path.join(self.output_directory, current_directory, file_name)
                    self.create_directory_if_not_exists(os.path.join(self.output_directory, current_directory))
                    with open(file_path, "w") as f:
                        f.write(code_content.strip())
                    file_count += 1
                file_progress.update(1)

        return file_count

    def get_code_content(self, url: str) -> str:
        """
        Fetch the content of a code file from a given URL.

        Args:
            url (str): The URL of the code file.

        Returns:
            str: The content of the code file.
        """
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        content_div = soup.find("div", id="content")
        code_pre = content_div.find("pre")
        code_content = code_pre.get_text() if code_pre else ""
        return code_content

    def run(self) -> None:
        """
        Run the scraping process.
        """
        index_url = self.base_url
        self.create_directory_if_not_exists(self.output_directory)
        subdirectories = self.scrape_subdirectories(index_url)

        total_directories = len(subdirectories)
        total_files = 0

        start_time = time.time()

        for subdir_name, subdir_url in tqdm(subdirectories, desc="Scraping"):
            self.create_directory_if_not_exists(os.path.join(self.output_directory, subdir_name))
            files_scraped = self.scrape_directory(subdir_url, subdir_name)
            total_files += files_scraped

        end_time = time.time()
        elapsed_time = end_time - start_time

        print("\nScraping Complete!")
        print(f"Total Directories: {total_directories}")
        print(f"Total Files Scraped: {total_files}")
        print(f"Time Taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    scraper = OpenScadExampleScraper()
    scraper.run()
