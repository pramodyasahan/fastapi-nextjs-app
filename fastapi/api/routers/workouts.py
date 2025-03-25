from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status
from models import Workout
from dependency import db_dependency, user_dependency

router = APIRouter(prefix="/workouts", tags=["Workouts"])


class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    pass


@router.get("/")
def get_workout(db: db_dependency, user: user_dependency, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()


@router.get("/all")
def get_all_workouts(db: db_dependency, user: user_dependency):
    return db.query(Workout).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_workout(db: db_dependency, user: user_dependency, workout: WorkoutCreate):
    new_workout = Workout(**workout.model_dump(), user_id=user.get("id"))
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout


@router.delete("/")
def delete_workout(db: db_dependency, user: user_dependency, workout_id: int):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if workout:
        db.delete(workout)
        db.commit()
    return workout