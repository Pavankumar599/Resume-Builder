from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_skill_gap(profile: dict, jd: dict):
    prompt = f"""You are a career coach. Analyze the skill match:

Student Profile:
Skills: {profile['skills']}
Education: {profile['education']}
Experience: {profile.get('experience', '')}

Job: {jd['title']}
Description: {jd['description']}

Return in this format:
**Matched Skills:** 
**Skill Gaps:** 
**Recommendations:**"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return {"analysis": response.choices[0].message.content}

def generate_resume_content(profile: dict, jd: dict):
    prompt = f"""Write a professional, ATS-friendly resume for this job:

Job Title: {jd['title']}
Job Description: {jd['description']}

Student Info:
Name: {profile['name']}
Education: {profile['education']}
Skills: {profile['skills']}
Projects: {profile.get('projects', 'None')}
Experience: {profile.get('experience', 'None')}

Return in clean Markdown format with proper sections."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content