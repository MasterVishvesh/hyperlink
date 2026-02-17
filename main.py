from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from database import SessionLocal, PDFLink, PDFLog
import uuid
import os
from datetime import datetime
from fastapi import Response


app = FastAPI()


# -----------------------------
# CREATE TRACKING LINK
# -----------------------------
@app.get("/create-link")
def create_link():

    db = SessionLocal()

    token = str(uuid.uuid4())
    file_name = "sample.pdf"

    new_link = PDFLink(
        token=token,
        file_name=file_name
    )

    db.add(new_link)
    db.commit()
    db.close()

    return {
        "tracking_url": f"http://127.0.0.1:8000/view/{token}"
    }


# -----------------------------
# VIEW PDF + LOG EVERY VISIT
# -----------------------------
@app.get("/view/{token}")
async def view_pdf(token: str, request: Request):

    db = SessionLocal()

    link = db.query(PDFLink).filter(PDFLink.token == token).first()

    if not link:
        db.close()
        return {"error": "Invalid link"}

    # Extract file name BEFORE closing session
    file_name = link.file_name

    # Get request details
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    referer = request.headers.get("referer")

    # Detect traffic source
    source = "Direct"

    if referer:
        if "google.com" in referer:
            source = "Google Search"
        else:
            source = "Other Website"

    # Unique visit ID (new every time)
    visitor_id = str(uuid.uuid4())

    # Create log entry (EVERY TIME)
    log = PDFLog(
        token=token,
        ip_address=ip_address,
        user_agent=user_agent,
        referer=referer,
        source=source,
        visitor_id=visitor_id,
        visit_time=datetime.utcnow()
    )

    db.add(log)
    db.commit()
    db.close()

    # File path
    file_path = os.path.join("pdfs", file_name)

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    return FileResponse(
        file_path,
        media_type="application/pdf"
    )


# -----------------------------
# OPTIONAL: PREVENT GOOGLE INDEXING
# -----------------------------
@app.get("/robots.txt")
def robots():
    return Response(
        content="User-agent: *\nDisallow: /view/",
        media_type="text/plain"
    )




