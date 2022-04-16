from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import logger

class Subcat:
    def __init__(self,sub_urls):
        self.log = logger.Logger()
        self.log.INFO("Subcategory_url module initiated")
        self.sub_urls = sub_urls
        chrome_option = Options()
        chrome_option.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
        chrome_option.add_argument("--no-sandbox")
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--disable-dev-shm-usage")
        self.driver_path = os.environ.get("CHROMEDRIVER_PATH")
        #self.driver_path = "E:\Shivansh\iNeuron\Projects\iNeuron_course_Scrapper\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_option)

    def url_parser(self,url):
        """Sets the page url for the driver to scrap"""
        self.driver.get(url)
        self.log.INFO(f'Parsing Page Title: {self.driver.title}')

    def courses_url(self):
        """Returns the list of courses url after scrapping from each subcategory"""
        self.courses = []
        self.log.INFO(f'Extracting Course URLS from each Subcategory')
        try:
            for url in self.sub_urls:
                self.url_parser(url)

                SCROLL_PAUSE_TIME = 0.5
                last_height = self.driver.execute_script("return document.body.scrollHeight")

                while True:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                course_class = self.driver.find_elements(By.CLASS_NAME, "Course_course-card__1_V8S.Course_card__2uWBu.card")

                for i in course_class:
                    course_page = i.find_elements(By.TAG_NAME, 'h5')
                    d = "-".join((course_page[0].text).split(" "))
                    if d == "":
                        continue
                    else:
                        self.courses.append("https://courses.ineuron.ai/" + d)
        except:
            self.log.WARN("Error ocuured while extracting subcategories")
            self.log.WARN("Continuing with the subcategories found")
            self.log.ERROR("Error ocuured while extracting subcategories")
            self.log.INFO("Continuing with the subcategories found")
        self.log.INFO(f"Found {len(self.courses)} courses")
        return self.courses
