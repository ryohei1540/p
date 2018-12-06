import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import mysql.connector
import datetime
import random

class Pairs:

    def __init__(self):
        self._driver = self.initialize_webdriver()
        self._cnx = mysql.connector.connect(user='xxx', password='xxx', database='pairs')
        self._cursor = self._cnx.cursor()

    def __del__(self):
        self._cursor.close()
        self._cnx.close()
        self._driver.quit()

    def initialize_webdriver(self):
        #Chrome用
        chrome_options = Options()
        chrome_options.add_argument("headless")

        driver_path = "/usr/bin/chromedriver"
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(str(driver_path), chrome_options=chrome_options)
        driver.get("https://www.pairs.lv/")
        driver.implicitly_wait(10)
        return driver

    def facebook_login(self):
        window_before = self._driver.window_handles[0]
        self._driver.find_element_by_class_name("top_direct_btn").click()
        window_after = self._driver.window_handles[1]
        self._driver.switch_to.window(window_after)

        id = "xxx"
        password = "xxx"
        self._driver.find_element_by_id("email").send_keys(id)
        self._driver.find_element_by_id("pass").send_keys(password)
        self._driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
        self._driver.switch_to.window(window_before)

    def close_campaign(self):
        #キャンペーンウィンドウを閉じる
        element = self._driver.find_element_by_id("welcome_close_button")
        self._driver.execute_script("arguments[0].click();", element)

    def close_recommended_users(self):
        #おすすめユーザーを閉じる
        element = self._driver.find_element_by_xpath("//div[@class='box_modal_window modal_animation pickup_modal']/div[@class='box_modal_window_inner']/a[@class='modal_close']")
        self._driver.execute_script("arguments[0].click();", element)

    def open_invisible_and_block_list(self):
        #非表示・ブロックを開く
        element = self._driver.find_element_by_xpath("//div[@class='side_contents']/div/nav[@class='box_gnavi']/div[@class='box_gnavis04'][4]/ul[@id='sidemenu_settings']/li[@class='gnavi_item'][3]/a")
        self._driver.execute_script("arguments[0].click();", element)

    def open_invisible_list(self):
        #非表示ユーザーリスト
        element = self._driver.find_element_by_xpath("//div[@class='common_box_inner']/div[@class='common_button_area mb10']/p[@class='button_item'][1]/a[@class='button_a button_white_a']")
        self._driver.execute_script("arguments[0].click();", element)

    def remove_invisible_users(self):
        pre_block_users_left = 0
        #非表示を解除
        while True:
            current_block_users_left = self._driver.find_element_by_xpath("//div[@class='common_box_inner']/div[@id='pagination_box']/p[@class='common_text text_center pager_info']/span[@id='max_count']").text
            #対象がいなくなったら終了
            if current_block_users_left == "0":
                break
            print("残り:{}人".format(current_block_users_left))
            #非表示を解除したはずのユーザーがリストに残ってしまう場合がある。その場合、上から2つ目のユーザーの非表示を解決する
            if pre_block_users_left != current_block_users_left:
                element = self._driver.find_element_by_xpath("//li[@class='user_item'][1]/a[@id='cancel_dislike_button']")
            else:
                element = self._driver.find_element_by_xpath("//li[@class='user_item'][2]/a[@id='cancel_dislike_button']")
            self._driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
            element = self._driver.find_element_by_xpath("//div[@class='modal_button_area text_center mt30']/button[@class='button_a button_white_a w30p modal-ok']")
            self._driver.execute_script("arguments[0].click();", element)
            pre_block_users_left = current_block_users_left
            self._driver.save_screenshot("/tmp/1.png")

    def start_removing_invisible_users(self):
        self.initialize_webdriver()
        self.facebook_login()
        self.close_campaign()
        self.close_recommended_users()
        self.open_invisible_and_block_list()
        self.open_invisible_list()
        self.remove_invisible_users()

pairs = Pairs()
pairs.start_removing_invisible_users()
