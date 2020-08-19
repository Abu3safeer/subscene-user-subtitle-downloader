import requests
from bs4 import BeautifulSoup


def get_subtitle_urls(url, subtitle_urls=[], base_url='https://subscene.com'):
    # Get page content
    data = requests.get(url).text

    # Prepare the parser
    html = BeautifulSoup(data, features='html.parser')

    # Get current page number, and links for previous and next pages.
    current_page_number = html.select_one('li.active a')
    prev_page_url = html.select_one('li.PagedList-skipToPrevious a')
    next_page_url = html.select_one('li.PagedList-skipToNext a')

    if current_page_number is not None:
        current_page_number = current_page_number.text
        print(f'Processing page {current_page_number}...')
    else:
        input('No subtitles. Press any key to exit...')
        exit()

    # Get previous page link
    if prev_page_url.get('href') is not None:
        prev_page_url = base_url + prev_page_url.get('href')
    else:
        prev_page_url = None

    # Get next page link
    if next_page_url.get('href') is not None:
        next_page_url = base_url + next_page_url.get('href')
    else:
        next_page_url = None

    # Get profile name
    profile_title = html.select_one('div.box.subtitles h2')
    profile_name = [name_part.strip() for name_part in profile_title.text.split()[2:-1]]
    profile_name = str.join(' ', profile_name)

    # Get profile subtitles count
    profile_subtitles_count = profile_title.text.split()[-1]

    print(f'Start fetching links from {profile_name}...')

    # Scrape the page and get all main subtitle sections
    subtitle_result = html.find_all('td', attrs={'class', 'a1'})

    for subtitle in subtitle_result:
        # Get subtitle link
        link = subtitle.find('a').get('href')

        # Get subtitle name
        name = str.strip(subtitle.find('span', class_='new').contents[0])

        # Get year
        year = str.strip(subtitle.find('div', class_='subtle').text)

        subtitle_urls.append({
            'name': name,
            'year': year,
            'link': link
        })

    print(f'{len(subtitle_urls)} links collected')

    if next_page_url:
        get_subtitle_urls(next_page_url, subtitle_urls)

    return subtitle_urls
