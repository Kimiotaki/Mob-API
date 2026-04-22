from datetime import date, datetime

from pydantic import BaseModel, Field, model_validator

from models.user_model import UserRole


class QualificationDetails(BaseModel):
    highest_qualification: str | None = None
    field_of_study: str | None = None
    institution_name: str | None = None
    completion_year: int | None = None
    grade_or_percentage: str | None = None
    certifications: list[str] = Field(default_factory=list)


class CommonProfileFields(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    alternate_phone_number: str | None = None
    gender: str | None = None
    date_of_birth: date | None = None
    bio: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    qualification: QualificationDetails = Field(default_factory=QualificationDetails)


class StudentProfileDetails(BaseModel):
    current_course: str | None = None
    current_institution: str | None = None
    year_of_study: int | None = None
    expected_graduation_year: int | None = None
    enrollment_number: str | None = None
    skills: list[str] = Field(default_factory=list)


class EducatorProfileDetails(BaseModel):
    designation: str | None = None
    department: str | None = None
    total_experience_years: float | None = None
    expertise_subjects: list[str] = Field(default_factory=list)
    employee_code: str | None = None
    previous_organizations: list[str] = Field(default_factory=list)


class ProfileUpsertRequest(CommonProfileFields):
    student_details: StudentProfileDetails | None = None
    educator_details: EducatorProfileDetails | None = None

    @model_validator(mode="after")
    def validate_role_specific_payload(self):
        if self.student_details and self.educator_details:
            raise ValueError("Provide either student_details or educator_details, not both")
        return self


class ProfileResponse(CommonProfileFields):
    id: str
    user_id: str
    role: int
    student_details: StudentProfileDetails | None = None
    educator_details: EducatorProfileDetails | None = None
    created_at: datetime
    modified_at: datetime
    created_by: str
    modified_by: str

    @model_validator(mode="after")
    def validate_role_specific_response(self):
        if self.role == UserRole.STUDENT and self.educator_details is not None:
            raise ValueError("Student profile cannot include educator_details")
        if self.role == UserRole.EDUCATOR and self.student_details is not None:
            raise ValueError("Educator profile cannot include student_details")
        return self
