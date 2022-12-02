# This is a sample Python script.

import os
import time

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import selenium.common.exceptions
import sys
from selenium import webdriver
import webbrowser
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_driver():
    try:
        # if getattr(sys, 'frozen', False):
        #     if os.name == 'nt':
        #         chromedriver_path = os.path.join(sys._MEIPASS, driver_filename+".exe")
        #         driver = webdriver.Chrome(chromedriver_path)
        #     elif os.name == 'posix':
        #         driver = webdriver.Chrome(driver_filename)
        # else:
        #     driver = webdriver.Chrome()

        if os.name == 'nt':
            chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
            driver = webdriver.Chrome(chromedriver_path)
        elif os.name == 'posix':
            chromedriver_path = "./chromedriver"
            driver = webdriver.Chrome(chromedriver_path)

        survey_url = 'https://webinfo.dankook.ac.kr/comm/surv/surp/views/findSrvshInfoBasList.do?_view=ok'
        driver.get(survey_url)
        driver.implicitly_wait(0.5)
        return driver

    except FileNotFoundError:
        print('Chromedriver를 찾을 수 없습니다.')
        print('웹사이트에 접속합니다. 이 사이트에서 프로그램과 같은 디렉토리에 다운로드하세요.')
        print('현재 Chrome의 버전과 일치한 Chromedriver를 다운로드해야 합니다.')
        webbrowser.open("https://chromedriver.chromium.org/downloads")

    return


def try_login(driver):
    login = driver.find_element(By.CSS_SELECTOR, 'input#username')

    try:
        WebDriverWait(driver, timeout=120).until(EC.staleness_of(login))
    except selenium.common.exceptions.NoSuchElementException:
        driver.implicitly_wait(1)
        try_login(driver)


def assure_able_to_enter_attendance(driver):
    driver.implicitly_wait(0.5)

    # 메인화면 -> 학사정보
    try:
        link = driver.find_element(By.CSS_SELECTOR, '#WUNIV > .ico_school')
        link.click()
        driver.implicitly_wait(0.5)
    except selenium.common.exceptions.NoSuchElementException:
        try_login(driver)
        assure_able_to_enter_attendance(driver)
        return

    # 학사정보 -> 수업관리 -> 출강관리 -> 출석확인 조회
    side_link = driver.find_element(By.CSS_SELECTOR, '#WLSSN > a')
    side_link.click()
    driver.implicitly_wait(0.5)

    side_link2 = driver.find_element(By.CSS_SELECTOR, '#WBZTM')
    side_link2_link = side_link2.find_element(By.CSS_SELECTOR, 'a')
    side_link2_link.click()

    driver.implicitly_wait(0.5)

    side_link3_list = driver.find_elements(By.CSS_SELECTOR, '#WBZTM > ul > li')
    side_link3_link = side_link3_list[0]
    side_link3_link.click()

    driver.implicitly_wait(0.5)

    try:
        if EC.alert_is_present():
            alert = driver.switch_to.alert
            alert.accept()
    except:
        return False  # 역량진단검사 기간이 아닌 경우 False 리턴

    driver.implicitly_wait(0.5)
    return True  # 역량진단검사 기간일 경우 True 리턴


def go_to_ability_survey(driver):
    survey_table = driver.find_elements(By.CSS_SELECTOR, 'table.tbl_striped > tbody > tr')
    driver.implicitly_wait(0.5)

    survey_link = None
    index_num = 0

    for row in survey_table:
        index_num += 1
        if '역량진단검사' in row.find_element(By.CLASS_NAME, 'ta_l').text:
            survey_link = row
            break

    try:
        survey_link_btn = survey_link.find_element(By.CSS_SELECTOR, f'button#joinBtn{index_num}')
        survey_link_btn.click()
    except:
        return

    driver.implicitly_wait(0.5)
    return


def reply_to_survey_questions(driver):
    # 부정 질문 문항 리스트
    negative_question_number_list = ['문항6.', '문항7.', '문항14.', '문항35.', '문항36.']
    current_question_number = ''

    form = driver.find_elements(By.CSS_SELECTOR, 'form#surpListWrapper > div.items_wrap')

    driver.implicitly_wait(1)

    # 부정적인 내용 질문 및 주관식 문항에 유의하여 자동으로 체크박스에 번호를 체크한다.
    for item in form:
        # 체크박스 목록을 가져옴
        answer_list = item.find_elements(By.CSS_SELECTOR, 'div > div.form_inline > div.form_chck')

        # 문항 번호를 가져옴
        try:
            current_question_number = item.find_element(By.CSS_SELECTOR, 'p.tit_q > strong').text
        except selenium.common.exceptions.NoSuchElementException:
            continue

        if len(answer_list) > 0:  # 주관식 문항 및 지시문이 아닐 때 맨 아래 항목에 체크
            if current_question_number not in negative_question_number_list:
                answer_list[-1].click()

            else:
                answer_list[0].click()

        driver.implicitly_wait(0.05)

    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = get_driver()  # 크롬 창을 열고 포털 로그인창에 접속

    if driver != None:
        try_login(driver)  # 사용자가 로그인할 때까지 대기

        isTestDate: bool = assure_able_to_enter_attendance(driver)  # 출석확인 조회 페이지 열기
        if isTestDate is False:
            print("현재 역량진단검사 기간이 아닙니다. 프로그램을 종료합니다.")

        go_to_ability_survey(driver)  # 역량조사 페이지 열기
        reply_to_survey_questions(driver)

        # 모든 항목 체크 완료 시 5분 대기
        timeout_after_checking: int = 300
        print(f"모든 항목을 체크하였습니다. {int(timeout_after_checking / 60)}분 간 현재 창에서 대기합니다.")
        time.sleep(timeout_after_checking)  # wait for 3000 secs
        print(f"자동 체크 후 {int(timeout_after_checking / 60)}분의 시간이 지나 프로그램을 종료합니다.")
