from fastapi import FastAPI
from fastapi.routing import APIRouter
from api_rest.en_plus.modelisation_rapart import router as modelisation1_router   # mettre modelisation_csv avant > modelisation_true now: restart maybe/ au pire copier modelisation_true, coller dans modelisation1
from securite import router1 as utils_router

router = APIRouter()
router.include_router(modelisation1_router)
router.include_router(utils_router, prefix="/utils", tags=["utils"])
#alphonse#
app = FastAPI()
app.include_router(router)
