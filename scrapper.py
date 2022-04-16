from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import logger

class Scrapper:
    def __init__(self,course_urls):
        self.Log = logger.Logger()
        self.Log.INFO("Scrapper module initiated")
        self.course_urls = course_urls
        chrome_option = Options()
        chrome_option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_option.add_argument("--no-sandbox")
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--disable-dev-shm-usage")
        self.driver_path = os.environ.get("CHROMEDRIVER_PATH")
        #self.driver_path = "E:\Shivansh\iNeuron\Projects\iNeuron_course_Scrapper\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_option)
        self.actions = ActionChains(self.driver)

    def details_scrap(self):
        """Returns the dictionary of all details scrapped from the course URL"""
        course_title = self.driver.find_elements(By.TAG_NAME, 'h3')[0].text
        course_desc = self.driver.find_elements(By.CLASS_NAME, 'Hero_course-desc__26_LL')[0].text

        try:
            course_price_tag = self.driver.find_elements(By.CLASS_NAME,
                                                 "CoursePrice_price-card__1_Bx-.CoursePrice_card__C2Lr_.card")
            course_price = course_price_tag[0].find_elements(By.TAG_NAME, "span")[0].text
        except:
            course_price= "Free"
            

        try:
            course_timings = self.driver.find_elements(By.CLASS_NAME, "CoursePrice_time__1I6dT")[0].text
            doubt_timings = self.driver.find_elements(By.CLASS_NAME, "CoursePrice_time__1I6dT")[1].text
        except:
            course_timings = "Recorded Course"
            doubt_timings = "Recorded Course"

        try:
            course_brief = self.driver.find_elements(By.TAG_NAME, "ul")[1].text
            course_brief = ", ".join(course_brief.split("\n"))
        except:
            course_brief = "NA"

        try:
            course_req_tag = self.driver.find_elements(By.CLASS_NAME, "CourseRequirement_card__3g7zR.requirements.card")
            course_req = course_req_tag[0].find_elements(By.TAG_NAME, "ul")[0].text
            course_req = ", ".join(course_req.split("\n"))
        except:
            course_req ="NA"

        try:
            course_feat_tag = self.driver.find_elements(By.CLASS_NAME, "CoursePrice_course-features__2qcJp")
            course_feat = course_feat_tag[0].find_elements(By.TAG_NAME, "ul")[0].text.strip()
            course_feat = ", ".join(course_feat.split("\n"))
        except:
            course_feat ="NA"

        mentor_name_tag = self.driver.find_elements(By.CLASS_NAME,
                                            "InstructorDetails_mentor__2hmG8.InstructorDetails_card__14MoH.InstructorDetails_flex__2ePsQ.card.flex")
        mentor = []
        for i in mentor_name_tag:
            mentor_name = i.find_elements(By.TAG_NAME, "h5")[0].text
            mentor.append(mentor_name)
        mentors = ", ".join(mentor)

        curriculam_class = self.driver.find_elements(By.CLASS_NAME,
                                                "CurriculumAndProjects_curriculum-accordion__2pppc.CurriculumAndProjects_card__7HqQx.card")
        curriculam = []
        for j in curriculam_class:
            curriculam.append(j.find_elements(By.TAG_NAME, "span")[0].text)
        curriculam_str = ", ".join(curriculam)

        self.details = { "Title" : course_title,
                         "Course Description" : course_desc,
                         "Price" : course_price,
                         "Class Timings" : course_timings,
                         "Doubt-class Timings" : doubt_timings,
                         "Course Overview" : course_brief,
                         "Features" : course_feat,
                         "Instructors" : mentors,
                         "Requirements": course_req,
                         "Syllabus" : curriculam_str
        }
        return self.details

    def course_page(self):
        count = 1
        ineuron_course = []
        self.Log.INFO(f"Starting scrapping of {len(self.course_urls)} courses")
        try:
            for page in self.course_urls:
                self.driver.get(page)
                time.sleep(5)
                # Closing the pop-up which appears on opening the page
                pop_close = self.driver.find_elements(By.CLASS_NAME, "fas.fa-times")
                self.actions.click(pop_close[0]).perform()
                """pop_up = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'fas.fa-times')))
                pop_up.click()"""

                """view_more = self.driver.find_elements(By.CLASS_NAME, "fas.fa-angle-down")
                self.actions.click(view_more[0]).perform()"""
                try:
                    # Clicking on view more on curricullam to extract entire syllabus
                    view_more = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'fas.fa-angle-down')))
                    view_more.click()

                    view_less = WebDriverWait(self.driver,2).until(
                        EC.presence_of_element_located((By.CLASS_NAME,'CurriculumAndProjects_view-more-btn__3ggZL')))
                except:
                    self.Log.ERROR(f"Error occured in view more for {page}")

                # Calling scrapper function to scrap details of page
                ineuron_course.append(self.details_scrap())
                self.Log.INFO(f"successfully scrapped page {count}. {page}")
                count+=1
        except Exception as e:
            self.Log.WARN(f"Warning!! Problem Occured {e}")
            self.Log.ERROR(f"Error occured : {e}")
        finally:
            return ineuron_course
