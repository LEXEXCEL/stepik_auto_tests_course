from math import log
from time import time
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


result = exceptions = []
urls = [
    'https://stepik.org/lesson/236895/step/1',
    'https://stepik.org/lesson/236896/step/1',
    'https://stepik.org/lesson/236897/step/1',
    'https://stepik.org/lesson/236898/step/1',
    'https://stepik.org/lesson/236899/step/1',
    'https://stepik.org/lesson/236903/step/1',
    'https://stepik.org/lesson/236904/step/1',
    'https://stepik.org/lesson/236905/step/1',
]


@pytest.fixture
def browser_connection():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


@pytest.mark.parametrize('url', urls)
def test_solution_to_stepik(browser_connection, url):
    browser_connection.implicitly_wait(15)
    browser_connection.get(url)

    # Ожидание кнопки "Войти"
    login_button = WebDriverWait(browser_connection, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.navbar__auth_login'))
    )
    login_button.click()

    # Авторизация
    input_email = WebDriverWait(browser_connection, 20).until(
        EC.visibility_of_element_located((By.ID, 'id_login_email'))
    )
    input_email.send_keys('hilnur@bk.ru')

    input_password = browser_connection.find_element(By.ID, 'id_login_password')
    input_password.send_keys('8-cV-)L6tr!7HEK')

    login_button = browser_connection.find_element(By.CSS_SELECTOR, '[class="sign-form__btn button_with-loader "]')
    login_button.click()

    # Проверка успешной авторизации
    WebDriverWait(browser_connection, 20).until(
        EC.invisibility_of_element_located((By.ID, 'id_login_email'))
    )

    try:

        solution_again_button = browser_connection.find_element(By.CSS_SELECTOR, '[class="again-btn white"]')
    except TimeoutException:
        ...
    else:
        solution_again_button.click()
    finally:
        result_area = WebDriverWait(browser_connection, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.string-quiz__textarea'))
        )
        result_area.send_keys(str(log(int(time()))))



    # Ожидание поля для ответа

    # Ожидание кнопки "Отправить"
    send_result_button = WebDriverWait(browser_connection, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit-submission'))
    )
    send_result_button.click()

    # Ожидание и вывод сообщения
    feedback_text = WebDriverWait(browser_connection, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.smart-hints__hint'))
    ).text

    assert feedback_text == 'Correct!', f'{feedback_text}'

