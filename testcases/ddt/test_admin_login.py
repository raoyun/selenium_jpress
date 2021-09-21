from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pytest
from util import util

class TestAdminLogin(object):

    login_data = [
        ('admin', '123456', '666', '验证码不正确，请重新输入'),
        ('admin', '123456', '666', 'JPress后台'),
    ]

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8081/jpress/admin/login')
        self.driver.maximize_window()

    @pytest.mark.parametrize('username, pwd, captcha, expected', login_data)
    @pytest.mark.dependency(name='admin_login')
    def test_admin_login_code(self, username, pwd, captcha, expected):

        self.driver.find_element_by_name('user').clear()
        self.driver.find_element_by_name('user').send_keys(username)
        self.driver.find_element_by_name('pwd').clear()
        self.driver.find_element_by_name('pwd').send_keys(pwd)
        if expected == 'JPress后台':
            captcha = util.get_code(self.driver, 'captchaImg')

            self.driver.find_element_by_name('captcha').clear()
            self.driver.find_element_by_name('captcha').send_keys(captcha)
            self.driver.find_element_by_class_name('btn').click()

            WebDriverWait(self.driver, 5).until(EC.title_is(expected))

            assert expected == self.driver.title
        else:
            self.driver.find_element_by_name('captcha').clear()
            self.driver.find_element_by_name('captcha').send_keys(captcha)
            self.driver.find_element_by_class_name('btn').click()

            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert

            assert alert.text == expected
            alert.accept()

if __name__ == '__main__':
    pytest.main(['test_admin_login.py'])

