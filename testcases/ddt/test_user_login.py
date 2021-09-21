from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from util import util
import pytest

class TestUserLogin(object):

    login_data = [
        ('rryy', '1234567', '用户名或密码不正确'),
        ('rryy', '123456', '用户中心'),
    ]

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8081/jpress/user/login')
        self.driver.maximize_window()

    # 测试用户登录密码错误
    @pytest.mark.parametrize('username,pwd, expected', login_data)
    def test_user_login(self, username, pwd, expected):

        self.driver.find_element_by_name('user').clear()
        self.driver.find_element_by_name('user').send_keys(username)

        self.driver.find_element_by_name('pwd').clear()
        self.driver.find_element_by_name('pwd').send_keys(pwd)
        self.driver.find_element_by_class_name('btn').click()

        if pwd != '123456':
            WebDriverWait(self.driver,5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert

            assert alert.text == expected
            alert.accept()
        else:
            WebDriverWait(self.driver, 5).until(EC.title_is(expected))
            assert expected == self.driver.title



if __name__ == '__main__':
    pytest.main(['test_user_login.py'])