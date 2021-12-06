# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_driver():
    edge_options = webdriver.EdgeOptions()
    driver = webdriver.ChromiumEdge(options=edge_options)
    driver.implicitly_wait(0.5)
    driver.get('https://webinfo.dankook.ac.kr/tiac/comm/surv/surp/views/findSurvQuesBasList.do')
    return driver


def try_login(driver):
    login = driver.find_element(By.CSS_SELECTOR, 'input#username')

    try:
        WebDriverWait(driver, timeout=120).until(EC.staleness_of(login))
    except StaleElementReferenceException:
        driver.implicitly_wait(1)
        try_login(driver)

    return


def assure_able_to_enter_attendance(driver):
    driver.implicitly_wait(0.5)

    # 메인화면 -> 학사정보
    link = driver.find_element(By.CSS_SELECTOR, '#WUNIV > .ico_school')
    link.click()
    driver.implicitly_wait(0.5)

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
        return

    driver.implicitly_wait(0.5)
    return


def go_to_ability_survey(driver):
    survey_table = driver.find_elements(By.CSS_SELECTOR, 'table.tbl_striped > tbody > tr')
    driver.implicitly_wait(0.5)

    survey_link = None
    index_num = 0

    for row in survey_table:
        index_num += 1
        if row.find_element(By.CLASS_NAME, 'ta_l').text == '2021학년도 역량진단검사(2학기)':
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
    driver = get_driver() # edge 창을 열고 포털 로그인창에 접속

    try_login(driver) # 사용자가 로그인할 때까지 대기

    assure_able_to_enter_attendance(driver) # 출석확인 조회 페이지 열기
    
    go_to_ability_survey(driver) # 역량조사 페이지 열기

    reply_to_survey_questions(driver)