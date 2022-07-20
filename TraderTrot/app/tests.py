from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class TraderTrotTest(LiveServerTestCase):
    def testform(self):
        selenium = webdriver.Chrome()

        selenium.get('http://127.0.0.1:8000/login') # url to visit

        uname = selenium.find_element('id','uname')
        pswd = selenium.find_element('id','pswd')

        submit = selenium.find_element('id','submit')

        uname.send_keys('a@gmail.com')
        pswd.send_keys('10101010')
        submit.send_keys(Keys.RETURN)

        assert 'JOICE JOHN' in selenium.page_source
