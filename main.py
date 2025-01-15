import scrape
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from data_models import Course
from txt_message import MessageManager

COLLECTION = "courses"
CRN_KEY = 'crn'
SECRETS_FILE = "secrets.json"
URL_PATH = "https://registration.wm.edu/?details&srcdb=202520&crn="


def format_course_data(course: Course) -> str:
    return f'''Name: {course.name}
Instructor: {course.instructor}
Seats avail: {course.seats_avail}/{course.enroll_max}
Waitlist: {course.waitlist_total}/{course.waitlist_max}'''


def new_course(course: Course, message_manager: MessageManager):
    message = f'Subject: Course Tracking Update\n\nTracking new course with CRN {course.crn}.\n{format_course_data(course)}'
    print(message + '\n\n\n')
    message_manager.send_message(message)


def update_course(course: Course, message_manager: MessageManager):
    message = f'Subject: Course Tracking Update\n\nUpdate to course with CRN {course.crn}.\n{format_course_data(course)}'
    print(message + '\n\n\n')
    message_manager.send_message(message)


def main():
    # Initialize text message sender
    message_manager = MessageManager()

    # Initialize firebase service account connection
    cred = credentials.Certificate(SECRETS_FILE)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Read from firestore
    courses_ref = db.collection(COLLECTION)
    docs = courses_ref.stream()

    # Iterate through all documents in a Firestore collection
    for doc in docs:
        # Get the unique course identifier
        crn = int(doc.id)

        # Current data we have on a particular course
        existing_data = doc.to_dict()

        # Get the most current data for that course
        updated_course = scrape.get_course(URL_PATH, crn)

        # For each course, compare to previous data from Firebase on this course.
        updated_course_dict = updated_course.model_dump()
        updated_course_dict.pop(CRN_KEY)  # Remove the CRN for comparison

        # If this is the first time getting data on that course, make a new entry.
        doc_ref = db.collection(COLLECTION).document(str(crn))

        if existing_data != updated_course_dict:
            doc_ref.set(updated_course_dict)
            if existing_data == {}:
                new_course(updated_course, message_manager)
            else:
                update_course(updated_course, message_manager)

            # Wait a bit before updating more
            time.sleep(10)


if __name__ == "__main__":
    main()
