
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("APP_URL", "http://localhost:5000")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # Headless mode allows tests to run without opening a browser window.
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


def get_message(driver):
    return WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "message").text
    )


def test_registration_page_opens(driver):
    driver.get(BASE_URL)

    assert driver.title == "Student Registration"
    assert driver.find_element(By.ID, "name").is_displayed()
    assert driver.find_element(By.ID, "email").is_displayed()
    assert driver.find_element(By.ID, "password").is_displayed()


def test_empty_fields(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "submit").click()

    assert get_message(driver) == "All fields are required"


def test_invalid_email(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "name").send_keys("Prathibha")
    driver.find_element(By.ID, "email").send_keys("wrong-email")
    driver.find_element(By.ID, "password").send_keys("test123")
    driver.find_element(By.ID, "submit").click()

    assert get_message(driver) == "Invalid email address"


def test_valid_registration(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "name").send_keys("Prathibha")
    driver.find_element(By.ID, "email").send_keys(
        "prathibha.test@example.com"
    )
    driver.find_element(By.ID, "password").send_keys("test123")
    driver.find_element(By.ID, "submit").click()

    assert get_message(driver) == "Registration successful"


def test_health_endpoint(driver):
    driver.get(BASE_URL + "/health")

    assert "healthy" in driver.find_element(
        By.TAG_NAME, "body"
    ).text
