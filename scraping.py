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
        self._cnt = 1

    def __del__(self):
        self._cursor.close()
        self._cnx.close()
        self._driver.quit()

    def initialize_variables(self):
        self._nickname = ""
        self._age = ""
        self._blood_type = ""
        self._nth_child = ""
        self._nationality = ""
        self._languages = [""] * 5
        self._residence = ""
        self._home = ""
        self._school_history = ""
        self._school_name = ""
        self._occupation = ""
        self._industry = ""
        self._salary = ""
        self._height = ""
        self._marital_status = ""
        self._child = ""
        self._when_marry = ""
        self._want_child = ""
        self._housework = ""
        self._how_to_meet = ""
        self._cost_of_date = ""
        self._personalities = [""] * 46
        self._sociability = ""
        self._lodger = ""
        self._holiday = ""
        self._drinking = ""
        self._smoking = ""
        self._hobbies = [""] * 40
        self._good = ""
        self._tweet = ""
        self._introduction = ""
        self._pictures = [""] * 100
        self._community = ""
        self._created_date = ""


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

    def set_search_fileter(self):
        #検索フィルター設定
        element = self._driver.find_element_by_id("openSearchConditionBtn")
        self._driver.execute_script("arguments[0].click();", element)
        age_low_element = self._driver.find_element_by_id('select-age-low')
        age_low_select_element = Select(age_low_element)
        age_low_select_element.select_by_value('20')
        age_height_element = self._driver.find_element_by_id('select-age-height')
        age_height_select_element = Select(age_height_element)
        age_height_select_element.select_by_value('20')
        country_element = self._driver.find_element_by_id('select-residence-country-0')
        country_select_element = Select(country_element)
        country_select_element.select_by_value('1')
        state_element = self._driver.find_element_by_id('select-residence-state-0')
        state_select_element = Select(state_element)
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        state_select_element.select_by_value('13')
        lastlogin_element = self._driver.find_element_by_id('select-lastlogin')
        lastlogin_select_element = Select(lastlogin_element)
        lastlogin_select_element.select_by_value('6')
        element = self._driver.find_element_by_id("submitSearchConditionBtn")
        self._driver.execute_script("arguments[0].click();", element)

    def change_grid_to_card(self):
        #表示形式をグリッドからカードに変更
        element = self._driver.find_element_by_xpath("//a[@ng-click='ctrl.transitionToSearchOne(ctrl.pager.offset + 1)']")
        self._driver.execute_script("arguments[0].click();", element)

    def start_scraping(self):
        self.initialize_webdriver()
        self.facebook_login()
        self.close_campaign()
        self.close_recommended_users()
        self.set_search_fileter()
        self.change_grid_to_card()

    def set_value(self):
        self._nickname = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.nickname']").text
        age = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.age']")
        age = re.search(r"^(\d+)", age.text)
        if age is not None:
            self._age = age.group()
        blood_type = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.blood_type']")
        blood_type = re.search(r"^([A-Z]+)", blood_type.text)
        if blood_type is not None:
            self._blood_type = blood_type.group()
        self._nth_child = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.nth_child']").text
        self._nationality = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.nationality']").text
        language_gotten = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.langStr()']")
        if language_gotten is not None:
            for i, value in enumerate(re.split('[、,・ ]', language_gotten.text)):
                self._languages[i] = value
        residence = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.residence_country']")
        residence = re.search(r"（\w+）", residence.text)
        if residence is not None:
            self._residence = residence.group()[1:-1]
        home = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.home_country']")
        home = re.search(r"（\w+）", home.text)
        if home is not None:
            self._home = home.group()[1:-1]
        education = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.education']")
        school_history = re.search(r"^(\w+)", education.text)
        if school_history is not None:
            self._school_history = school_history.group()
        school_name = re.search(r"\(\w+\)", education.text)
        if school_name is not None:
            self._school_name = school_name.group()[1:-1]
        partner_job = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.job']")
        occupation = re.search(r"^(\w+)", partner_job.text)
        if occupation is not None:
            self._occupation = occupation.group()
        industry = re.search(r"\(\w+\)", partner_job.text)
        if industry is not None:
            self._industry = industry.group()[1:-1]
        self._salary = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.hasAnnualIncome()']").text
        height = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.height']")
        height = re.search(r"^(\d+)", height.text)
        if height is not None:
            self._height = height.group()
        self._body_build = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.body_build']").text
        marital_status = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.marital_status']")
        marital_status = re.search(r"\(\w+\)", marital_status.text)
        if marital_status is not None:
            self._marital_status = marital_status.group()[1:-1]
        self._child = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.child']").text
        self._when_marry = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.when_marry']").text
        self._want_child = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.want_child']").text
        self._housework = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.housework']").text
        self._how_to_meet = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.how_to_meet']").text
        self._cost_of_date = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.cost_of_date']").text
        personality_gotten = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.personalitiesStr()']")
        if personality_gotten is not None:
            for i, value in enumerate(re.split('[、,・ ]', personality_gotten.text)):
                self._personalities[i] = value
        sociability = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.sociability']").text
        lodger = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.lodger']").text
        holiday = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.holiday']").text
        drinking = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.drinking']").text
        smoking = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.smoking']").text
        hobby_gotten = self._driver.find_element_by_xpath("//dd[@ng-show='ctrl.pm.partner.hobbiesStr()']")
        if hobby_gotten is not None:
            for i, value in enumerate(re.split('[＊、,・ ]', hobby_gotten.text)):
                self._hobbies[i] = value
        self._good = self._driver.find_element_by_xpath("//p[@class='user_like_count_b']/strong").text
        self._tweet = self._driver.find_element_by_xpath("//p[@class='user_tweet']")
        try:
            self._introduction = self._driver.find_element_by_xpath("//p[@class='introduction_text']").text
        except:
            #自己紹介が書かれていない場合は空白とする
            pass
        pre_picture_page = 1
        while True:
            #写真取得
            picture_gotten = self._driver.find_elements_by_xpath("//ul[@class='user_photo_list four_photos'][*]//img[@class='image-round']")
            #値代入
            start_index = (pre_picture_page - 1) * 4
            for i, value in enumerate(picture_gotten, start_index):
                self._pictures[i] = value.get_attribute("src")
            #写真次ページへ
            element = self._driver.find_element_by_xpath("//div[@class='box_user_photo_pager']/a[@class='pager_next button_c button_white_a']")
            self._driver.execute_script("arguments[0].click();", element)
            #現在ページ確認
            current_picture_page = self._driver.find_element_by_xpath("//div[@class='box_user_photo_pager']/ol[@class='pager_nums']/li[@class='pager_num is_current']/a[@href='']")
            if pre_picture_page == int(current_picture_page.text):
                break
            pre_picture_page = int(current_picture_page.text)
        #参加しているコミュニティの数を抜き取る
        community = self._driver.find_element_by_xpath("//p[@class='title_a']")
        self._community = int(re.sub(r'\D', '', community.text))
        self._created_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    def insert_into_database(self):
        try:
            #tweetのみtweet.textと参照しようとすると、エラーが発生してしまう場合がある。対応策が不明のため、その場合はエラーとし、読み飛ばすこととしている。
            add_user = ("INSERT INTO users "
                   "(nickname, age, tweet, introduction, good, blood_type, nth_child, nationality, language1, language2, language3, language4, language5, residence, home, education, school, occupation, industry, salary, height, body_build, marital_status, child, when_marry, want_child, housework, how_to_meet, cost_of_date, personality1, personality2, personality3, personality4, personality5, personality6, personality7, personality8, personality9, personality10, personality11, personality12, personality13, personality14, personality15, personality16, personality17, personality18, personality19, personality20, personality21, personality22, personality23, personality24, personality25, personality26, personality27, personality28, personality29, personality30, personality31, personality32, personality33, personality34, personality35, personality36, personality37, personality38, personality39, personality40, personality41, personality42, personality43, personality44, personality45, personality46, sociability, lodger, holiday, drinking, smoking, hobby1, hobby2, hobby3, hobby4, hobby5, hobby6, hobby7, hobby8, hobby9, hobby10, hobby11, hobby12, hobby13, hobby14, hobby15, hobby16, hobby17, hobby18, hobby19, hobby20, hobby21, hobby22, hobby23, hobby24, hobby25, hobby26, hobby27, hobby28, hobby29, hobby30, hobby31, hobby32, hobby33, hobby34, hobby35, hobby36, hobby37, hobby38, hobby39, hobby40, picture1, picture2, picture3, picture4, picture5, picture6, picture7, picture8, picture9, picture10, picture11, picture12, picture13, picture14, picture15, picture16, picture17, picture18, picture19, picture20, picture21, picture22, picture23, picture24, picture25, picture26, picture27, picture28, picture29, picture30, picture31, picture32, picture33, picture34, picture35, picture36, picture37, picture38, picture39, picture40, picture41, picture42, picture43, picture44, picture45, picture46, picture47, picture48, picture49, picture50, picture51, picture52, picture53, picture54, picture55, picture56, picture57, picture58, picture59, picture60, picture61, picture62, picture63, picture64, picture65, picture66, picture67, picture68, picture69, picture70 , community, created_date) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data_user = (self._nickname, self._age, self._tweet.text, self._introduction,  self._good, self._blood_type, self._nth_child, self._nationality, self._languages[0], self._languages[1], self._languages[2], self._languages[3], self._languages[4], self._residence, self._home, self._school_history, self._school_name, self._occupation, self._industry, self._salary, self._height, self._body_build, self._marital_status, self._child, self._when_marry, self._want_child, self._housework, self._how_to_meet, self._cost_of_date, self._personalities[0], self._personalities[1], self._personalities[2], self._personalities[3], self._personalities[4], self._personalities[5], self._personalities[6], self._personalities[7], self._personalities[8], self._personalities[9], self._personalities[10], self._personalities[11], self._personalities[12], self._personalities[13], self._personalities[14], self._personalities[15], self._personalities[16], self._personalities[17], self._personalities[18], self._personalities[19], self._personalities[20], self._personalities[21], self._personalities[22], self._personalities[23], self._personalities[24], self._personalities[25], self._personalities[26], self._personalities[27], self._personalities[28], self._personalities[29], self._personalities[30], self._personalities[31], self._personalities[32], self._personalities[33], self._personalities[34], self._personalities[35], self._personalities[36], self._personalities[37], self._personalities[38], self._personalities[39], self._personalities[40], self._personalities[41], self._personalities[42], self._personalities[43], self._personalities[44], self._personalities[45], self._sociability, self._lodger, self._holiday, self._drinking, self._smoking, self._hobbies[0], self._hobbies[1], self._hobbies[2], self._hobbies[3], self._hobbies[4], self._hobbies[5], self._hobbies[6], self._hobbies[7], self._hobbies[8], self._hobbies[9], self._hobbies[10], self._hobbies[11], self._hobbies[12], self._hobbies[13], self._hobbies[14], self._hobbies[15], self._hobbies[16], self._hobbies[17], self._hobbies[18], self._hobbies[19], self._hobbies[20], self._hobbies[21], self._hobbies[22], self._hobbies[23], self._hobbies[24], self._hobbies[25], self._hobbies[26], self._hobbies[27], self._hobbies[28], self._hobbies[29], self._hobbies[30], self._hobbies[31], self._hobbies[32], self._hobbies[33], self._hobbies[34], self._hobbies[35], self._hobbies[36], self._hobbies[37], self._hobbies[38], self._hobbies[39], self._pictures[0], self._pictures[1], self._pictures[2], self._pictures[3], self._pictures[4], self._pictures[5], self._pictures[6], self._pictures[7], self._pictures[8], self._pictures[9], self._pictures[10], self._pictures[11], self._pictures[12], self._pictures[13], self._pictures[14], self._pictures[15], self._pictures[16], self._pictures[17], self._pictures[18], self._pictures[19], self._pictures[20], self._pictures[21], self._pictures[22], self._pictures[23], self._pictures[24], self._pictures[25], self._pictures[26], self._pictures[27], self._pictures[28], self._pictures[29], self._pictures[30], self._pictures[31], self._pictures[32], self._pictures[33], self._pictures[34], self._pictures[35], self._pictures[36], self._pictures[37], self._pictures[38], self._pictures[39], self._pictures[40], self._pictures[41], self._pictures[42], self._pictures[43], self._pictures[44], self._pictures[45], self._pictures[46], self._pictures[47], self._pictures[48], self._pictures[49], self._pictures[50], self._pictures[51], self._pictures[52], self._pictures[53], self._pictures[54], self._pictures[55], self._pictures[56], self._pictures[57], self._pictures[58], self._pictures[59], self._pictures[60], self._pictures[61], self._pictures[62], self._pictures[63], self._pictures[64], self._pictures[65], self._pictures[66], self._pictures[67], self._pictures[68], self._pictures[69], self._community, self._created_date)
            self._cursor.execute(add_user, data_user)
            self._cnx.commit()
            #make_user_invisible()
            #下のメソッドを呼び出すとうまくいかず。。。
            #データを収集したユーザーを非表示に設定
            element = self._driver.find_element_by_xpath("//a[@ng-click='ctrl.showModalHideBlockSelect()']")
            self._driver.execute_script("arguments[0].click();", element)
            #非表示クリック
            element = self._driver.find_element_by_xpath("//label[@ng-click='ctrl.onClickHide()']")
            self._driver.execute_script("arguments[0].click();", element)
            #設定するクリック
            element = self._driver.find_element_by_xpath("//button[@ng-click='ctrl.changeHideBlockState()']")
            self._driver.execute_script("arguments[0].click();", element)
            #閉じるクリック
            element = self._driver.find_element_by_xpath("//button[@ng-click='ctrl.close()']")
            self._driver.execute_script("arguments[0].click();", element)
        except:
            print("{0}, {1}".format(self._nickname, self._age))
    
    def make_user_invisible(self):
        #データを収集したユーザーを非表示に設定
        element = self._driver.find_element_by_xpath("//a[@ng-click='ctrl.showModalHideBlockSelect()']")
        self._driver.execute_script("arguments[0].click();", element)
        #非表示クリック
        element = self._driver.find_element_by_xpath("//label[@ng-click='ctrl.onClickHide()']")
        self._driver.execute_script("arguments[0].click();", element)
        #設定するクリック
        element = self._driver.find_element_by_xpath("//button[@ng-click='ctrl.changeHideBlockState()']")
        self._driver.execute_script("arguments[0].click();", element)
        #閉じるクリック
        element = self._driver.find_element_by_xpath("//button[@ng-click='ctrl.close()']")
        self._driver.execute_script("arguments[0].click();", element)

    def go_into_next_page(self):
        element = self._driver.find_element_by_xpath("//a[@ng-click='ctrl.moveToNext()']")
        self._driver.execute_script("arguments[0].click();", element)
        self._cnt += 1

pairs = Pairs()
pairs.start_scraping()
while True:
    #機械的に見えないよう、ランダムでスリープする秒数を決める
    time.sleep(random.randint(1,5))
    pairs.initialize_variables()
    pairs.set_value()
    pairs.insert_into_database()
    element = pairs._driver.find_element_by_xpath("//a[@ng-click='ctrl.moveToNext()']")
    pairs._driver.execute_script("arguments[0].click();", element)
    pairs._cnt += 1
    #seleniumがメモリリークするため、900件の処理を終えた時点で一度リセットする
    if pairs._cnt == 900:
        print("再起動")
        del pairs
        pairs = Pairs()
        pairs.start_scraping()