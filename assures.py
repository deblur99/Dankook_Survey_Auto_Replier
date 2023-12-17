# 웹정보 내 설문조사 항목으로 이동
def assure_able_to_enter_attendance():
    global driver
    
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


# 최종성적 조회 페이자에 접근하여 현재 설문조사 강제 중인지 여부 확인
def assure_able_to_enter_final_grade():
    global driver

    # 메인화면 -> 학사정보
    try:
        link = driver.find_element(By.CSS_SELECTOR, '#WUNIV > .ico_school')
        link.click()
        driver.implicitly_wait(0.5)
    except selenium.common.exceptions.NoSuchElementException:
        try_login(driver)
        assure_able_to_enter_attendance(driver)
        return

    # 학사정보 -> 성적관리 -> 최종성적 조회
    side_link = driver.find_element(By.CSS_SELECTOR, '#WGDMG > a')
    side_link.click()
    driver.implicitly_wait(0.5)

    side_link2 = driver.find_element(By.ID, '4023')
    side_link2_link = side_link2.find_element(By.CSS_SELECTOR, 'a')
    side_link2_link.click()

    driver.implicitly_wait(0.5)

    try:
        if EC.alert_is_present():
            alert = driver.switch_to.alert
            alert.accept()
    except:
        return False  # 만족도조사 기간이 아닌 경우 False 리턴

    driver.implicitly_wait(0.5)
    return True  # 만족도조사 기간일 경우 True 리턴