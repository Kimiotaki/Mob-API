from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    EDUCATOR = "educator"
    ADMIN = "admin"
    EXTERNAL = "external"