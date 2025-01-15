from pydantic import BaseModel


class Course(BaseModel):
    crn: int
    name: str
    instructor: str
    enroll_max: int
    seats_avail: int
    waitlist_total: int
    waitlist_max: int
