from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By


def handler(event=None, context=None):
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
    chrome.get('https://www.google.com/search?q="test"')

    # Ожидание, пока не исчезнет баннер с cookies (если он появляется)
    try:
        # Ожидание, пока кнопка "Согласиться с cookies" станет доступной и нажать ее
        accept_cookies_button = WebDriverWait(chrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Согласиться с условиями"]'))
        )
        accept_cookies_button.click()
    except:
        pass  # Если кнопка не появляется, продолжаем без ее нажатия

    # Ожидаем загрузки результатов поиска
    WebDriverWait(chrome, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h3'))
    )

    # Извлекаем ссылки с результатов поиска
    results = chrome.find_elements(By.CSS_SELECTOR, 'h3')
    links = [result.find_element(By.XPATH, '..').get_attribute('href') for result in results]

    chrome.quit()  # Закрытие браузера

    # Возвращаем ссылки
    return {
        'statusCode': 200,
        'body': {
            'links': links
        }
    }
