from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By


def handler(event=None, context=None):
    try:
        options = webdriver.ChromeOptions()
        service = webdriver.ChromeService("/opt/chromedriver")
    
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
    
        chrome = webdriver.Chrome(options=options, service=service)
        chrome.get('https://duckduckgo.com/?q="test"')
    
        # Извлечение ссылок с результатов поиска
        results = chrome.find_elements(By.CSS_SELECTOR, 'h2')
        links = [result.find_element(By.XPATH, '..').get_attribute('href') for result in results]
    
        chrome.quit()  # Закрытие браузера
    
        # Возвращаем ссылки
        return {
            'statusCode': 200,
            'body': {
            'links': links
            }
        }
     except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'error': str(e)
            }
        }
