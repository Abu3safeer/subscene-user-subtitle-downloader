import requests
from bs4 import BeautifulSoup
from urllib import parse
import links
from pathlib import Path


# URL goes here
url = input("Pleas type the profile link where you want me to start:\r\n")

# Get data from url
page_link = parse.urlparse(url)
page_query = parse.parse_qs(page_link.query)
profile_id = page_query.get('id')
page_number = page_query.get('page')
page_orderBy = page_query.get('orderBy')


# Check if the url is valid
if not page_link.netloc == 'subscene.com' \
        or not page_link.path.startswith('/u/') \
        or not page_link.path.endswith('/subtitles'):
    input('This is not valid Subscene profile link, press any key to exit...')
    exit()

# Check if url is for first page.
if page_number is not None and int(page_number[0]) > 1:
    print(f"WARNING: You are starting from page {page_number[0]}, this script will not fetch previous pages. ")


print(f'Start Processing link {url}')


# Call a function to fetch all urls
subtitle_urls = links.get_subtitle_urls(url)

# Write urls to text files.
links_file = open('link.txt', 'w', encoding="utf-8")
detailed_file = open('detailed.txt', 'w', encoding="utf-8")

for subtitle in subtitle_urls:
    links_file.write(f"{subtitle.get('link')}\n")
    detailed_file.write(f"{subtitle.get('name')} {subtitle.get('year')}: {subtitle.get('link')}\n")

links_file.close()
detailed_file.close()

# Create download folder if not exists
if not Path(Path('').cwd().__str__() + '/downloads').exists():
    Path(Path('').cwd().__str__() + '/downloads').mkdir()

# Start downloading
for subtitle in subtitle_urls:
    print(f"Downloading {subtitle.get('name')} {subtitle.get('year')}")

    # Get download page content
    file_download_page = requests.get(subtitle.get('link')).text

    # Get download link for file from download page
    file_link = 'https://subscene.com' + BeautifulSoup(file_download_page, features='html.parser').select_one('div.download a').get('href')

    # Download file
    file = requests.get(file_link)

    # Get file name from headers
    file_name = file.headers['content-disposition'][21:]

    # Write file content to the folder
    open('downloads/' + file_name, 'wb').write(file.content)