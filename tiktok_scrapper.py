import sys
import requests 
import wget
import json 
from tqdm import tqdm

class TikTokScraper:
    def __init__(self, query='drones in the sky', max_count=1000, file_output='tiktok.json'):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Host': 'www.tiktok.com',
        }
        self.cookies = {
            'ttwid' : '1|WMK4Zd2oG1nlVkvFbuGX0-2yFx4JojDbcEj5A0Hg1js|1674462622|688263138a2d29724aa73b4e5fc291d9b1b8f326c100b9af6fc0ad9f31d1db00',
        }
        self.params = {
            'aid': '1988',
            'app_language': 'en',
            'app_name': 'tiktok_web',
            'browser_language': 'en-US',
            'browser_name': 'Mozilla',
            'browser_online': 'true',
            'browser_platform': 'Linux x86_64',
            'browser_version': '5.0 (X11)',
            'channel': 'tiktok_web',
            'cookie_enabled': 'true',
            'device_id': '7190082068487243265',
            'device_print(1)visible': 'true',
            'keyword': query,
            'os': 'linux',
            'priority_region': '',
            'referer': '',
            'region': 'KZ',
            'screen_height': '1080',
            'screen_width': '1920',
            'tz_name': 'Asia/Almaty',
            'webcast_language': 'en',
            '_signature' : '_02B4Z6wo00001tes2sgAAIDCmgpGlwoTHcLXrd5AANYy2d',
            'X-Bogus': 'DFSzsIVLiksANVXMSZOkrSax3cug',
            'msToken': 'DoHDHw8F4v0eys04htiQU702iJiuzLFXOg9k3yVfmqJx46KX01D3noghLdtBQpjWDv68Ifg0F3n9Fy6bCvTIFOEla45UDFL_auEo4GdOc2tkB-McQ-7M7cfcnkTImFC4sM7WSphbM3azoA=='
        }
        self.max_count = max_count
        self.file_output = file_output

    def _scrape_from_tiktok(self, tiktok_range):
        self.params['offset'] = tiktok_range
        tiktok_request = requests.get('https://www.tiktok.com/api/search/general/full/',
                        headers=self.headers,
                        cookies=self.cookies,
                        params=self.params,
                        )
        return tiktok_request.json()

    def scrape_video_urls(self):
        objects = []
        for i in range(0, self.max_count, 12):
            try:
                tiktok_json = self._scrape_from_tiktok(i)
            except:
                print('Error with scraping, range: ', i)
                break
            items = self.get_items(tiktok_json)
            video_urls = self.get_video_urls(items)
            objects.extend(video_urls) 
        return objects
    
    def download_videos(self, video_urls):
        print("Downloading videos...")
        for video_url in tqdm(video_urls):
            try:
                wget.download(video_url, f'videos/{video_urls.index(video_url)}.mp4')
            except:
                print('Error with downloading video, link: ', video_url)
                continue
    
    def save_objects(self, objects, file_output='tiktok.json'):
        with open(file_output, 'w') as f:
            json.dump(objects, f)

    def get_items(self, tiktok_json):
        items = tiktok_json['data']
        return items
    
    def get_video_urls(self, items):
        video_urls = []
        for item in items:
            try:
                if len(video_urls) < self.max_count:
                    video_url = item['item']['video']['playAddr']
                    video_urls.append(video_url)
                else:
                    break
            except:
                print('Video url not found, item: ')
                continue    
        return video_urls

def main(query: str, max_count: int):
    tiktok_scraper = TikTokScraper(query, max_count)
    video_urls = tiktok_scraper.scrape_video_urls()
    tiktok_scraper.download_videos(video_urls)
    print('Done!')


if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print('Usage: python tiktok_scrapper.py <query: string> <max_count: int>')
        exit(0)
    main(sys.argv[1], int(sys.argv[2]))
