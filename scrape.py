import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from data_models import Course


def get_course(url_path: str, crn: int) -> Course:
    url = url_path + str(crn)

    # Initialize the WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening the browser
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the page
        driver.get(url)

        # Get the seat information
        course_name_html = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dtl-course-code"))
        )

        # Get the instructor information
        instructor_html = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "instructor-detail"))
        )

        # Get the seat information
        seats_html = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text.detail-seats"))
        )

        seats_text = seats_html.text

        # Regex patterns
        max_enrollment_pattern = r"Maximum Enrollment:\s*(\d+)"
        seats_available_pattern = r"Seats Avail:\s*(\d+)"
        waitlist_total_pattern = r"Waitlist Total:\s*(\d+)\s*of\s*(\d+)"

        # Extract data
        course_name = course_name_html.text
        instructor_info = instructor_html.text
        max_enrollment = re.search(max_enrollment_pattern, seats_text)
        seats_available = re.search(seats_available_pattern, seats_text)
        waitlist_total = re.search(waitlist_total_pattern, seats_text)

        # Get results in an integer format, -1 for no results
        max_enroll_num = -1
        if max_enrollment:
            max_enroll_num = int(max_enrollment.group(1))

        seats_available_num = -1
        if seats_available:
            seats_available_num = int(seats_available.group(1))

        waitlist_total_num = -1
        waitlist_available_num = -1
        if waitlist_total:
            waitlist_total_num = int(waitlist_total.group(1))
            waitlist_available_num = int(waitlist_total.group(2))

        return Course(
            crn=crn,
            name=course_name,
            instructor=instructor_info,
            enroll_max=max_enroll_num,
            seats_avail=seats_available_num,
            waitlist_total=waitlist_total_num,
            waitlist_max=waitlist_available_num)

    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    URL_PATH = "https://registration.wm.edu/?details&srcdb=202520&crn="

    course = get_course(URL_PATH, 20514)
    print(course)
