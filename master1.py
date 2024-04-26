from fastapi import FastAPI
from fastapi.routing import APIRouter
from modelisation1 import router as modelisation1_router
from utils22 import router1 as utils_router

router = APIRouter()
router.include_router(modelisation1_router)
router.include_router(utils_router, prefix="/utils", tags=["utils"])

app = FastAPI()
app.include_router(router)
