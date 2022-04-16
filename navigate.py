import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import os
import logger

class Navigate:
    def __init__(self):
        self.main_url = "https://ineuron.ai"
        self.log = logger.Logger()
        self.log.INFO("Initiating navigate module for collecting subcategories urls")
        chrome_option = Options()
        chrome_option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_option.add_argument("--no-sandbox")
        #chrome_option.add_argument("--headless")
        chrome_option.add_argument("--disable-dev-shm-usage")
        chrome_option.add_argument("start-maximized")
        self.driver_path = os.environ.get("CHROMEDRIVER_PATH")
        #self.driver_path = "E:\Shivansh\iNeuron\Projects\iNeuron_course_Scrapper\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_option)
        self.driver.maximize_window()
        self.driver.get(self.main_url)
        self.actions = ActionChains(self.driver)
        time.sleep(2)
        self.log.INFO(f'Page Title: {self.driver.title}')

    def popup_close(self):
        """Closes the popup appears on main screen"""
        pop_close = self.driver.find_elements(By.CLASS_NAME, "fas.fa-times")
        self.actions.click(pop_close[0]).perform()
        self.log.INFO("Home Page Pop up closed successfully")

    def course_category(self):
        """ Returns tags containing urls for each Course Category """
        try:
            time.sleep(5)
            self.popup_close()
            course_tag = self.driver.find_elements(By.CLASS_NAME, "dropdown-chevron-down")
            time.sleep(2)
            self.actions.move_to_element(course_tag[0]).perform()
            self.category_list_tags = self.driver.find_elements(By.ID, "categories-list")
            self.category_tags = self.category_list_tags[0].find_elements(By.TAG_NAME, "a")
            self.log.INFO("Tags of Subcategories collected successfully")
        except Exception as e:
            self.log.WARN("Error occured while collecting subcategories Tags")
            self.log.ERROR("Error occured while collecting subcategories Tags")
            self.log.ERROR(e)

    def course_subcategory(self):
        """Returns list containing urls of all the Courses subcategory"""
        self.course_category()
        self.courses_subcategory_url = []
        try:
            for i in self.category_tags:
                time.sleep(1)
                self.actions.move_to_element(i).perform()
                self.subcategory_list_tags = self.category_list_tags[0].find_elements(By.ID, "subcategories-list")
                self.subcategory_tags = self.subcategory_list_tags[0].find_elements(By.TAG_NAME, "a")
                for j in self.subcategory_tags:
                    self.courses_subcategory_url.append(j.get_attribute("href"))

            self.driver.close()
            self.log.INFO("Successfully Extracted all the urls for the subcategories")
            self.log.INFO(f"Found {len(self.courses_subcategory_url)} subcategories")
            return self.courses_subcategory_url
        except Exception as e:
            self.log.WARN("Error occured while collecting subcategories URL")
            self.log.ERROR("Error occured while collecting subcategories URL")
            self.log.ERROR(e)


