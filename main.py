import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# преобразует сложную строку типа "1.3 миллион" в "1300000"
def convert_to_number(s):
    # Удаляем лишние пробелы и приводим к нижнему регистру
    s = s.strip().lower()

    # Разделяем строку на числовую часть и суффикс
    num_part = ""
    suffix = ""
    for char in s:
        if char.isdigit() or char == '.':
            num_part += char
        else:
            suffix += char

    # Преобразуем числовую часть в float
    num = float(num_part)

    if "quadrillion" in suffix:
        multiplier = 1_000_000_000_000_000
    elif "trillion" in suffix:
        multiplier = 1_000_000_000_000
    elif "billion" in suffix:
        multiplier = 1_000_000_000
    elif "million" in suffix:
        multiplier = 1_000_000
    elif "thousand" in suffix:
        multiplier = 1_000
    else:
        multiplier = 1  # Если суффикс не распознан, считаем как есть

    # Умножаем и возвращаем целое число
    return int(num * multiplier)

# преобразует строку с элемента странциы в число
def convert_price_to_int(price_str):
    # Удаляем лишние пробелы и приводим к нижнему регистру
    price_str = price_str.strip().lower()

    # Проверяем, есть ли запятые (формат "ddd,ddd")
    if "," in price_str:
        # Удаляем запятые и преобразуем в целое число
        return int(price_str.replace(",", ""))

    # Проверяем, есть ли суффикс (например, "million", "thousand")
    if any(word in price_str for word in ["million", "thousand", "billion", "trillion"]):
        return convert_to_number(price_str)  # Используем функцию из предыдущего ответа

    # Если это просто число без запятых и суффиксов
    return int(price_str)

cookiePage = "https://orteil.dashnet.org/cookieclicker/"

driver = webdriver.Chrome()
driver.get(cookiePage)

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)
element.click()

cookieId = "bigCookie"
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, cookieId))
)
bigCookie = driver.find_element(By.ID, cookieId)

while 1:
    bigCookie.click()
    cookies_text = driver.find_element(By.ID, "cookies").text

    # Используем регулярное выражение для извлечения числа
    cookies_count = re.search(r"[\d,]+", cookies_text).group()

    # Удаляем запятые и преобразуем в целое число
    cookies_count = int(cookies_count.replace(",", ""))

    for i in range(10):
        product_price = driver.find_element(By.ID, "productPrice" + str(i)).text

        if product_price == "":
            continue

        product_price = convert_price_to_int(product_price)

        # убирает возможность купить курсор если он стоит больше 6000
        if product_price > 6000 and i == 0:
            continue

        # убирает возможность купить бабущку если она стоит больше 20000
        if product_price > 20000 and i == 1:
            continue

        if cookies_count > product_price:
            product = driver.find_element(By.ID, "product" + str(i))
            product.click()
            break
    
    try:

        div = driver.find_element(By.ID, "upgrades")
        child_elements = div.find_elements(By.CSS_SELECTOR, "*")

        for upgrade in child_elements:
            try:
                class_attribute = upgrade.get_attribute("class")

                if "enabled" in class_attribute:
                    upgrade.click()
            except Exception as e:
                print(f"Ошибка при клике на улучшение: {e}")
    except Exception as e:
        print(f"Ошибка при поиске улучшений: {e}")