import time
import selenium.common.exceptions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver = None


def get_driver():
    global driver
    
    try:            
        driver = webdriver.Chrome(ChromeDriverManager().install())
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


# 유저가 로그인할 때까지 대기
def wait_for_login_completed():
    global driver
    
    login = driver.find_element(By.CSS_SELECTOR, 'input#user_id')
    try:
        WebDriverWait(driver, timeout=120).until(EC.staleness_of(login))
    except selenium.common.exceptions.NoSuchElementException:
        driver.implicitly_wait(1)
    return


# 포털에서 웹정보 페이지로 이동
def go_to_webinfo_page():
    find_outer_link_on_portal()
    find_inner_link_on_portal()
    return


# 바깥쪽 배너 접근하여 웹정보 바로가기 배너 찾기
def find_outer_link_on_portal():
    global driver
    
    outer_banner = driver.find_elements(By.CSS_SELECTOR, '#top_wrap > div.major_menu_area > ul > li')
    outer_link = None
    for banner in outer_banner:
        if banner.find_element(By.TAG_NAME, 'a').text == '학사서비스':
            outer_link = banner.find_element(By.TAG_NAME, 'a')
            driver.implicitly_wait(0.5)
            break
        
    if outer_link != None:
        outer_link.click()
        driver.implicitly_wait(0.5)
    else:
        raise selenium.common.exceptions.NoSuchElementException("Failed to find outer_link: No DOM found what you want.")


# 웹정보 바로가기 배너 접근하여 웹정보 탭 새로 열기
def find_inner_link_on_portal():
    global driver
    
    inner_banner = driver.find_elements(By.CSS_SELECTOR, '#header > div.nav_layer > ul > li:nth-child(2) > ul > li')
    inner_link = None
    for banner in inner_banner:
        if banner.find_element(By.TAG_NAME, 'a').text == '웹정보':
            inner_link = banner.find_element(By.TAG_NAME, 'a')
            driver.implicitly_wait(0.5)
            break
        
    if inner_link != None:
        inner_link.click()  # 탭 새로 생성하고 웹정보 페이지 열기
        driver.implicitly_wait(0.5)
        driver.switch_to.window(driver.window_handles[-1])  # 새로 열린 탭으로 전환
        driver.implicitly_wait(0.5)
    else:
        raise selenium.common.exceptions.NoSuchElementException("Failed to find inner_link: No DOM found what you want.")


def go_to_survey_manage_page():
    global driver    
    obj = driver.find_element(By.CSS_SELECTOR, "#WSURV")
    
    btn = obj.find_element(By.TAG_NAME, "a")
    btn.click()
    driver.implicitly_wait(0.5)
    
    link = driver.find_element(By.CSS_SELECTOR, "#WSURV > ul > li > a")
    link.click()
    driver.implicitly_wait(0.5)


# 콘솔창에 입력받은 설문조사 이름으로 설문조사 페이지에서 해당 설문조사로 이동
def go_to_survey(decision):
    global driver
    
    survey_table = driver.find_elements(By.CSS_SELECTOR, 'table.tbl_striped > tbody > tr')
    driver.implicitly_wait(0.5)

    survey_link = None
    index_num = 0

    for row in survey_table:
        index_num += 1
        if decision == row.find_element(By.CLASS_NAME, 'ta_l').text:
            survey_link = row
            break

    try:
        survey_link_btn = survey_link.find_element(By.CSS_SELECTOR, f'button#joinBtn{index_num}')
        survey_link_btn.click()
    except:
        return

    driver.implicitly_wait(0.5)
    return


# 설문조사 문항에 자동 답변
def reply_to_survey_questions():
    global driver
    
    # 부정 질문 문항 리스트
    negative_question_number_list = ['문항5.', '문항6.', '문항13.', '문항34.', '문항35.']
    form = driver.find_elements(By.CSS_SELECTOR, 'form#surpListWrapper > div.items_wrap')
    # driver.implicitly_wait(1)

    # 단일 문항과 테이블을 구별한다.
    # 부정적인 내용 질문 및 주관식 문항에 유의하여 자동으로 체크박스에 번호를 체크한다.
    for item in form:
        table = None
        answer_list = []
        text_form = None

        # 단일 문항과 테이블을 구별한다.
        try:
            table = item.find_element(By.CSS_SELECTOR, 'div.tbl_row > table > thead')
            # print(table)
        except selenium.common.exceptions.NoSuchElementException:
            pass

        # 단일 항목 체크
        if table is None:
            # 체크박스 목록을 가져옴
            try:
                answer_list = item.find_elements(By.CSS_SELECTOR, 'div > div.form_inline')
                text_form = item.find_element(By.CSS_SELECTOR, 'div.form_text > textarea')
                # print(text_form)
            except:
                pass

            if text_form is None:
                # 문항 번호를 가져옴
                try:
                    current_question_number = item.find_element(By.CSS_SELECTOR, 'p.tit_q > strong').text
                except selenium.common.exceptions.NoSuchElementException:
                    continue

                if len(answer_list) > 0:  # 주관식 문항 및 지시문이 아닐 때 맨 아래 항목에 체크
                    if current_question_number not in negative_question_number_list:
                        answer_list[-1].find_element(By.CSS_SELECTOR, "div.form_chck > input").click()
                    else:
                        answer_list[0].find_element(By.CSS_SELECTOR, "div.form_chck > input").click()

            else:
                # 주관식 답안에 . 적기
                text_form.click()
                text_form.send_keys('.')

        # 테이블 항목 내용 한번에 체크
        else:
            try:
                rows = table.find_elements(By.CSS_SELECTOR, 'td')
                for row in rows:
                    btn = row.find_elements(By.CSS_SELECTOR, 'div.form_chck > input')
                    # click the rightest answer
                    driver.execute_script("arguments[arguments.length - 1].click();", btn[-1])
                # driver.implicitly_wait(0.05)

            except selenium.common.exceptions.NoSuchElementException:
                pass

        # driver.implicitly_wait(0.05)

    return


def subroutines(decision):
    wait_for_login_completed()  # 로그인 창으로 이동
    go_to_webinfo_page()
    go_to_survey_manage_page()
    go_to_survey(decision)      # 역량조사 페이지 열기
    reply_to_survey_questions()


def main():
    # 입력받기
    print("응답하고자 하는 설문조사명을 정확히 입력하세요. 취소를 원하시면 'q'를 입력하세요.")
    decision: str = input()
    if decision == 'q' or decision == 'Q':
        return

    get_driver()  # 크롬 창을 열고 포털 로그인창에 접속

    if driver != None:
        try:
            subroutines(decision)
        except selenium.common.exceptions.NoSuchElementException as e:
            print(e.msg, e.stacktrace)
            print('탐색에 실패하였습니다. 다시 시도하겠습니까?')
            print('r을 누르면 다시 시작하고, 아무 키나 입력하면 프로그램을 종료합니다.')
            if input().lower() == 'r':
                subroutines(decision)
            else:
                return

        # 모든 항목 체크 완료 시 5분 대기
        timeout_after_checking: int = 300
        print(f"모든 항목을 체크하였습니다. {int(timeout_after_checking / 60)}분 간 현재 창에서 대기합니다.")
        time.sleep(timeout_after_checking)  # wait for 3000 secs
        print(f"자동 체크 후 {int(timeout_after_checking / 60)}분의 시간이 지나 프로그램을 종료합니다.")    
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
