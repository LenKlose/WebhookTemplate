from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from core.constants import APP_NAME
from core.models import DocumentCreatedWebhook
from core.utils import download_document, update_document_metadata

app = FastAPI(title="Webhook App")
router = APIRouter(prefix=f"/{APP_NAME}")


@router.get('/')
async def root():
    return JSONResponse({"app": "webhooktemplate"}, status_code=200)


@router.post('/predict_document/{repo_uuid}')
async def document_created(request: Request, hook: DocumentCreatedWebhook, repo_uuid: str):
    file = download_document(request, hook, repo_uuid)

    # ToDo: Call your ai service
    print(len(file))

    # ToDo: Update properties based on your data
    # list of properties under https://ai-carfile.d-velop.cloud/dms/r/1332a60a-46e2-47f8-826c-d572e27576ae/source
    update_properties = [
        {
            "key": "943ac291-179e-48d0-9c21-ef738181a645",  # Property: Kategorie Verkaufsdokument
            "values": ["Fahrzeugbrief"]
        }
    ]

    # ToDo: Update category based on your data
    # list of categories under https://ai-carfile.d-velop.cloud/dms/r/1332a60a-46e2-47f8-826c-d572e27576ae/source
    update_category = "f26bea76-7dbf-4e53-9169-81ddb3e2f8c4"  # Category: Fahrzeug - Verkaufsdokument

    update_document_metadata(request, hook, repo_uuid, update_category, update_properties)

app.include_router(router)
