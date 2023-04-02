
import pytest_selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

from config import email, password


def test_cards():
    selenium = webdriver.Chrome()
    selenium.get('https://petfriends.skillfactory.ru/')

    # click registration button
    btn_new_user = selenium.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_new_user.click()

    # click existing user button
    btn_exist_acc = selenium.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # add email
    field_email = selenium.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("max1@gmail.com")

    # add password
    field_pass = selenium.find_element(By.CSS_SELECTOR, "input#pass")
    field_pass.clear()
    field_pass.send_keys("123pass")

    # click submit button
    btn_submit = selenium.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # go to my pets page
    btn_submit = selenium.find_element(By.XPATH, "//*[@href='/my_pets']")
    btn_submit.click()


    # find statistics about pets count of user
    pets_count_xpath = list(selenium.find_element(By.XPATH, "//div[@class='.col-sm-4 left']").text.split('\n'))
    pets_count = int(pets_count_xpath[1].split(': ')[-1])

    # find all tag <img> on page
    images = WebDriverWait(selenium, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "th[scope='row'] img")))

    images_count = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            images_count += 1

    assert images_count >= pets_count / 2, 'less then 50% of pets have photo'

    descriptions = WebDriverWait(selenium, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
    for i in range(len(list(descriptions))):
        for y in range(2):
            assert list(re.split(" |\n", descriptions[i].text[y])) != "" or " " or "None", "Some pets don't have some description"

    selenium.quit()

def test_table_of_pets():
    selenium = webdriver.Chrome()
    selenium.implicitly_wait(10)
    selenium.get('https://petfriends.skillfactory.ru/')

    # click registration button
    btn_new_user = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]"))
    )
    btn_new_user.click()

    # click existing user button
    btn_exist_acc = selenium.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # add email
    field_email = selenium.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("max1@gmail.com")

    # add password
    field_pass = selenium.find_element(By.CSS_SELECTOR, "input#pass")
    field_pass.clear()
    field_pass.send_keys("123pass")

    # click submit button
    btn_submit = selenium.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # go to /my_pets page
    btn_submit = selenium.find_element(By.XPATH, "//*[@href='/my_pets']")
    btn_submit.click()


    # find statistics about count of pets of user
    pets_count_xpath = list(selenium.find_element(By.XPATH, "//div[@class='.col-sm-4 left']").text.split('\n'))
    pets_count = int(pets_count_xpath[1].split(': ')[-1])


    # count of my_pet cards on page
    cards_count = selenium.find_elements(By.CSS_SELECTOR, '.table-hover tbody tr')
    assert len(cards_count) == pets_count, 'count of cards equally with statistics of pets of user'

    selenium.quit()