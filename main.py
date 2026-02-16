from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from database import SessionLocal, PDFLink, PDFLog
import uuid
import os


app = FastAPI()

@app.get("/create-link")
def create_link():

    db = SessionLocal()

    token = str(uuid.uuid4())
    file_name = "sample.pdf"

    new_link = PDFLink(token=token, file_name=file_name)
    db.add(new_link)
    db.commit()
    db.close()

    return {"tracking_url": f"http://127.0.0.1:8000/view/{token}"}


@app.get("/view/{token}")
async def view_pdf(token: str, request: Request):

    db = SessionLocal()

    link = db.query(PDFLink).filter(PDFLink.token == token).first()

    if not link:
        db.close()
        return {"error": "Invalid link"}

    # ✅ Extract data BEFORE closing session
    file_name = link.file_name

    # Log entry
    log = PDFLog(
        token=token,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    db.add(log)
    db.commit()
    db.close()   # now safe to close

    # File path
    file_path = os.path.join("pdfs", file_name)

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    return FileResponse(file_path, media_type="application/pdf")