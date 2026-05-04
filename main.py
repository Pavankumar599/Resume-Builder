from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from services.llm import analyze_skill_gap, generate_resume_content
from services.renderer import save_resume_as_pdf, save_resume_as_docx

load_dotenv()

app = FastAPI(title="AI Resume Builder")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

os.makedirs("generated_resumes", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"request": request}
)
@app.post("/generate")
async def generate_resume(
    name: str = Form(...),
    email: str = Form(...),
    education: str = Form(...),
    skills: str = Form(...),
    projects: str = Form(...),
    experience: str = Form(...),
    jd_title: str = Form(...),
    jd_description: str = Form(...)
):
    # Prepare profile
    profile = {
        "name": name,
        "email": email,
        "education": education,
        "skills": [s.strip() for s in skills.split(",") if s.strip()],
        "projects": projects,
        "experience": experience
    }

    jd = {
        "title": jd_title,
        "description": jd_description,
        "required_skills": ["Python", "FastAPI", "SQL", "Machine Learning"]  # Example
    }

    # AI Processing
    analysis = analyze_skill_gap(profile, jd)
    resume_content = generate_resume_content(profile, jd)

    filename_base = f"{name.replace(' ', '_')}_{jd_title.replace(' ', '_')}"

    pdf_path = save_resume_as_pdf(resume_content, filename_base)
    docx_path = save_resume_as_docx(resume_content, filename_base)

    return {
        "status": "success",
        "analysis": analysis["analysis"],
        "resume_preview": resume_content,
        "download_pdf": f"/download/{filename_base}.pdf",
        "download_docx": f"/download/{filename_base}.docx",
        "filename": filename_base
    }

@app.get("/download/{filename}")
async def download_file(filename: str):
    path = f"generated_resumes/{filename}"
    if os.path.exists(path):
        return FileResponse(path, filename=filename)
    return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)