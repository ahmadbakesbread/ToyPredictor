import random
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

Different_Agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1']

random_agents = random.choice(Different_Agents)

def get_driver(random_agents):
    headers = {
        'User-Agent': random_agents,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',  # Do Not Track Request Header
        'referer': 'https://stockx.com'
    }

    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={headers['User-Agent']}")
    options.chrome_version = '116'
    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
    return driver