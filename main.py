from uuid import uuid4

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
    # All existing IDs can be found at: https://ai-contracts.d-velop.cloud/dms/r/befa2a91-fe9f-41b9-a098-e51d64c03805/source
    contract_number = str(uuid4()) # UUID or consecutive number
    contract_partner_1 = "Frankfurt Future AG"
    contract_partner_2 = "d.velop AG"
    contract_type = "Rahmenvertrag" # one of: [Rahmenvertrag, Mietvertrag, NDA, ...]
    contract_date = "2023-04-28"
    contract_deadline = "Text in which the deadlines are described."
    object_of_agreement = f"{contract_partner_1} {contract_type}"
    
    update_properties = [
        {
            "key": "d8bc07c6-addd-4dd8-a251-f0b8fbb75746", # Property: Vertragsnummer
            "values": [contract_number]
        },
        {
            "key": "b8408c1a-0e07-4fb0-a490-5e0aed82755e", # Property: Vertragspartner 1
            "values": [contract_partner_1]
        },
        {
            "key": "d68dc5eb-316e-4c79-80a0-6c36b8f1d118", # Property: Vertragspartner 2
            "values": [contract_partner_2]
        },
        {
            "key": "4b4d0a42-5876-48fd-b5ef-92fa0ab81552", # Property: Vertragstyp
            "values": [contract_type]
        },
        {
            "key": "f16ae0a2-2d79-40c2-a020-a70d0c3993a1", # Property: Vertragsgegenstand
            "values": [object_of_agreement]
        },
        {
            "key": "52271d2d-0354-4e7b-852e-30e70531dc84", # Property: Vertragsdatum
            "values": [contract_date]
        },
        {
            "key": "8ae93468-0ac0-4659-b7a4-f1858bf9fc85", # Property: Fristen
            "values": [contract_deadline]
        },
        {
            "key": "06c6b34f-c8e2-4d52-bed6-db8130e9e7d9", # Property: Vertragsstatus
            "values": ["Entwurf"]
        },
    ]
    update_category = "540aa199-0ef7-412a-9a99-3ccfbc27fb23"  # Vertragsdokument
    update_document_metadata(request, hook, repo_uuid, update_category, update_properties)

app.include_router(router)
