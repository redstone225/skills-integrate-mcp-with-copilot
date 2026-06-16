"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from . import db

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=current_dir / "static"), name="static")

# Initialize database if necessary
db.initialize_db()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return db.fetch_activities()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if not db.activity_exists(activity_name):
        raise HTTPException(status_code=404, detail="Activity not found")

    if db.participant_exists(activity_name, email):
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    db.add_participant(activity_name, email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if not db.activity_exists(activity_name):
        raise HTTPException(status_code=404, detail="Activity not found")

    if not db.participant_exists(activity_name, email):
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    db.remove_participant(activity_name, email)
    return {"message": f"Unregistered {email} from {activity_name}"}
