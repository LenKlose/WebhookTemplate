from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from core.constants import APP_NAME
from core.models import DocumentCreatedWebhook
from core.utils import download_document, update_document_metadata

app = FastAPI(title="Webhook App")
router = APIRouter(prefix=f"/{APP_NAME}")


@router.get('')
async def root():
    return JSONResponse({"app": "webhooktemplate"}, status_code=200)


@router.post('/predict_document/{repo_uuid}')
async def document_created(request: Request, hook: DocumentCreatedWebhook, repo_uuid: str):
    file = download_document(request, hook, repo_uuid)

    # ToDo: Call your ai service
    print(len(file))

    # ToDo: Update properties based on your data
    # list of properties under /dms/r/{repo_uuid}/source
    update_properties = [
        {
            "key": "dv.folder.customer.rf.SalesOrderNumber",
            "values": [hook.doc.id]
        },
        {
            "key":  "dv.folder.customer.example.change",
            "values": [1234]
        }
    ]

    # ToDo: Update category based on your data
    # list of categories under /dms/r/{repo_uuid}/source
    update_category = "dv.folder.customer.dt.CustomerOrder"  # or hook.docType.id

    update_document_metadata(request, hook, repo_uuid, update_category, update_properties)

app.include_router(router)
