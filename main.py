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

    # ToDo: Update document_type and sender based on your data
    # All existing property IDs can be found at: https://ai-mailroom.d-velop.cloud/dms/r/0188b03e-e468-46f9-a534-a48d3faafe88/source
    document_type = "Auftrag" # one of: [Angebot, Auftrag, Auftragsbestätigung, Lieferschein, Rechnung, Schriftwechsel, Vertrag, sonstiges]
    sender = "The Best Company GmbH"

    update_properties = [
        {
            "key": "a1a1dad4-dc9e-434c-bfc0-074cbabe0c13",
            "values": [document_type]
        },
        {
            "key":  "c3d93524-db1f-4d09-bbdb-d94fe3980abe",
            "values": [sender]
        }
    ]
    update_category = "ee98deea-7674-4692-89f3-31cc57c5dee3"  # 02 Eingangspost (klassifiziert)
    update_document_metadata(request, hook, repo_uuid, update_category, update_properties)

app.include_router(router)
