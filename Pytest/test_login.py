import pytest
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


@pytest.fixture(scope="module")  # this used for initializing webdriver
def driver():
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # Create a Chrome WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def login(driver):
    driver.get("https://beta.peerprofiler.com/login")
    time.sleep(10)
    yield driver

def test_navigate_to_login(login):
    assert "login" in login.current_url

def test_validate_logo(login):
    logo = login.find_element(By.XPATH, "//img[@alt='Logo']")
    assert logo.is_displayed()
    

def test_fill_login_credentials(login):
    username_field = WebDriverWait(login, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")))
    password_field = WebDriverWait(login, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))
    username_field.send_keys("Pgadmin2020")
    password_field.send_keys("PG@AdminKoLsNew")
    time.sleep(10)
    assert username_field.get_attribute('placeholder') == 'Username'
    assert password_field.get_attribute('placeholder') == 'Password'

def test_validate_eye_button(login):
    eye_button = login.find_elements(By.XPATH, "//span[@class='material-icons-round notranslate MuiIcon-root MuiIcon-fontSizeSmall d-flex align-items-center css-mbs4uh']//*[name()='svg']")
    assert len(eye_button) > 0

def test_select_dashboard(login):
    dropdown = WebDriverWait(login, 10).until(EC.presence_of_element_located((By.ID, "demo-simple-select")))
    dropdown.click()
    DD = Select(dropdown)
    DD.select_by_visible_text("Dashboard")
    time.sleep(3)
    selected_text = DD.first_selected_option.text
    assert selected_text == "Dashboard"

def test_submit_login_form(login):
    login_button = WebDriverWait(login, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()
    WebDriverWait(login, 10).until(EC.url_to_be("https://beta.peerprofiler.com/dashboard"))
    assert "dashboard" in login.current_url


