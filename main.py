"""
This script converts the Screeps documentation to PDF.
"""
import os
import pdfkit
import requests
from requests_html import HTMLSession
import pyppeteer
import asyncio


async def main(url_async, pdf_dir, file_name):
    """
    This function converts the URL to PDF.
    """
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(url_async)
    html = await page.content()
    # Use `html` instead of `response.html.html` below
    pdfkit.from_string(html, os.path.join(pdf_dir, file_name))
    await browser.close()


class HTML2PDF:
    """
    This class converts the URL to PDF.
    """

    def __init__(self, base_url_init):
        self.base_url = base_url_init
        self.session = HTMLSession()

    def get_response(self):
        """
        Get the getting_response from the base url_async.
        :return: getting_response object or False
        """
        try:
            getting_response = requests.get(self.base_url)
            getting_response.raise_for_status()
            return getting_response
        except requests.exceptions.HTTPError as err_h:
            print("Http Error:", err_h)
        except requests.exceptions.ConnectionError as err_c:
            print("Error Connecting:", err_c)
        except requests.exceptions.Timeout as err_t:
            print("Timeout Error:", err_t)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        return False

    def get_subpage_urls(self):
        """
        Get all subpage urls from the base url_async and convert them to PDF.
        :return: list of subpage URLs
        """
        getting_sub_page_response = self.session.get(self.base_url)
        getting_sub_page_response.html.render()
        subpage_urls = []
        for subpage_url in getting_sub_page_response.html.xpath('//a/@href'):
            if subpage_url.startswith("/docs"):
                subpage_urls.append(self.base_url + subpage_url)
            elif subpage_url.startswith("http") or subpage_url.startswith("www"):
                continue  # Skip external URLs
            else:
                subpage_urls.append(f'{self.base_url}/' + subpage_url.lstrip('/'))
        return subpage_urls

    def convert_to_pdf(self, convert_url, pdf_dir):
        """
        Convert the given url_async to PDF.
        :param convert_url:
        :param pdf_dir:
        """
        try:
            convert_response = self.session.get(convert_url)
            if convert_response.status_code == requests.codes.ok:
                try:
                    convert_response.html.render()
                    file_name = "".join([c for c in convert_url.split('/')[-1] if c.isalpha() or c.isdigit() or c == ' ']).rstrip() + '.pdf'
                    pdfkit.from_string(convert_response.html, os.path.join(pdf_dir, file_name))
                except Exception as e:
                    print(f"PDF conversion failed for {convert_url} with error {str(e)}")
            else:
                print(f"Failed to access (convert_to_url) {convert_url}, status code {convert_response.status_code}")
        except requests.exceptions.RequestException as err:
            print(f"Error occurred during request to {convert_url}: {str(err)}")
        except Exception as e:
            print(f"Failed to convert page {convert_url} to PDF due to error {str(e)}")


if __name__ == "__main__":
    base_url = input("Please enter the base url_async: ")
    html2pdf = HTML2PDF(base_url)
    if response := html2pdf.get_response():
        for url in html2pdf.get_subpage_urls():
            asyncio.run(main(url, "PDFs", f"{url.split('/')[-1]}.pdf"))
    else:
        print(f"Failed to access (main) {base_url}")
