from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cookie_page = "https://orteil.dashnet.org/cookieclicker/"

driver = webdriver.Chrome()
driver.get(cookie_page)

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)
element.click()

cookie_id = "bigCookie"
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)
bigCookie = driver.find_element(By.ID, cookie_id)

while 1:
    bigCookie.click()
    cookies_count = driver.find_element(By.ID, "cookies").text.split(" ")[0]
    cookies_count = int(cookies_count.replace(",", ""))
    # print(f'cookies_count = {cookies_count}')

    for i in range(4):
        product_price = driver.find_element(By.ID, "productPrice" + str(i)).text

        if product_price == "":
            continue

        # print(f'product_price = {product_price}')

        product_price = int(product_price.replace(",",""))

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