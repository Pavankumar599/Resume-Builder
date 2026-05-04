from pydantic import BaseModel
from typing import List, Optional

class StudentProfile(BaseModel):
    name: str
    email: str
    education: List[dict]
    skills: List[str]
    projects: List[dict]
    experiences: List[dict]
    certifications: List[str]
    achievements: List[str]

class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: List[str]

class ResumeRequest(BaseModel):
    profile: StudentProfile
    job_description: JobDescription