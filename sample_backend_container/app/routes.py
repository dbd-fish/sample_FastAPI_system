from fastapi import APIRouter
from app.controller.sample_controller import sample_endpoint

router = APIRouter()

router.get("/hello")(sample_endpoint)
