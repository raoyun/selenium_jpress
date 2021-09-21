from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from util import util

class TestUserLogin(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8081/jpress/user/login')
        self.driver.maximize_window()

    # 测试用户登录密码错误
    def test_admin_login_error(self):
        username = 'rryy'
        pwd = '1234567'
        expected = '用户名或密码不正确'

        self.driver.find_element_by_name('user').send_keys(username)
        self.driver.find_element_by_name('pwd').send_keys(pwd)
        self.driver.find_element_by_class_name('btn').click()

        WebDriverWait(self.driver,5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert

        assert alert.text == expected
        alert.accept()


    def test_user_login__ok(self):
        username = 'rryy'
        pwd = '123456'
        expected = '用户中心'

        self.driver.find_element_by_name('user').send_keys(username)
        self.driver.find_element_by_name('pwd').send_keys(pwd)


        self.driver.find_element_by_class_name('btn').click()

        WebDriverWait(self.driver, 5).until(EC.title_is(expected))

        assert expected == self.driver.title



