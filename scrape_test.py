import requests
import re
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 'Accept-Encoding': 'gzip', 'Accept-Language': 'en-US,en;q=0.9,es;q=0.8', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://www.google.com/', 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
#result = requests.get("https://www.handbook.unsw.edu.au/", headers=headers)

'''Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'''
'''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'''
handbook_url = "https://www.handbook.unsw.edu.au/"
url = "https://www.handbook.unsw.edu.au"
subject_links = []
course_links = []
pre_reqs = []
courses = []



#Chrome driver
driver = webdriver.Chrome('/opt/homebrew/bin/chromedriver') 
driver.maximize_window()
driver.get(handbook_url)
soup = BeautifulSoup(driver.page_source, features = "html.parser")
driver.close()


# print(soup.prettify())
# print("---------------!!!!!!!!!--------------")

def urlify(in_string):
    return "%20".join(in_string.split())

def delay():
    time.sleep(random.randint(3, 10))

def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    passed_in_driver.execute_script(scroll_by_coord)
    delay()
    # _nav_out_of_way = 'window.scrollBy(0, -120);'
    # passed_in_driver.execute_script(scroll_nav_out_of_way)

# get all subject links by subject area
subject_codes = soup.find_all('a', href = re.compile(r'/browse/By Subject Area/'))
for subject in subject_codes:
    new_url = ""
    title = subject.get('href')
    new_url = url + title
    subject_links.append(urlify(new_url))

# get each course list page in subject area
driver = webdriver.Chrome('/opt/homebrew/bin/chromedriver') 
for subject_link in subject_links:
    print("subject link: ", subject_link)
    driver.maximize_window()
    driver.get(subject_link)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    delay()
    scrape_flag = True

    # for all under undergrad courses (for now)
    while (scrape_flag):
        subject_soup = BeautifulSoup(driver.page_source, features="html.parser")
        course_codes = subject_soup.find_all('a', href = re.compile(r'/undergraduate/courses/2022/'))
        
        for course in course_codes:
            course_url = ""
            href = course.get('href')
            course_url = url + href
            print("  course link: ", course_url)
            course_links.append(course_url)

        try:    
            next_button = driver.find_element_by_id("pagination-page-next")
            prop = next_button.get_property('enabled')
            if next_button.is_enabled():
                scroll_shim(driver, next_button)
                actions = ActionChains(driver)
                actions.move_to_element(next_button).click().perform()
                delay()
            else:
                scrape_flag = False
        except NoSuchElementException:
            scrape_flag = False


driver.close()
