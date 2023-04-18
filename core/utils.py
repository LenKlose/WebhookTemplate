from functools import cache

import requests
from fastapi import Request

from core.constants import APP_NAME, DEFAULT_MAPPING_URL, DOC_DETAILS_URL
from core.models import DocumentCreatedWebhook


@cache
def get_session(request: Request) -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Origin": request.headers["Origin"],
        "x-dv-baseuri": request.headers["x-dv-baseuri"],
        "x-dv-tenant-id": request.headers["x-dv-tenant-id"],
        "x-dv-request-id": request.headers["x-dv-request-id"],
        "Authorization": request.headers["Authorization"],
        "Accept": "application/json",
    })
    return session


@cache
def get_link_relations(request: Request, repo_uuid: str, doc_id: str) -> dict:
    base_uri = request.headers["x-dv-baseuri"]
    session = get_session(request)
    doc_details = session.get(DOC_DETAILS_URL.format(base_uri=base_uri, repo_uuid=repo_uuid, doc_id=doc_id))
    return doc_details.json()["_links"]


def download_document(request: Request, hook: DocumentCreatedWebhook, repo_uuid: str) -> bytes:
    base_uri = request.headers["x-dv-baseuri"]
    download_url = get_link_relations(request, repo_uuid, hook.doc.id)["mainblobcontent"]["href"]
    doc_response = get_session(request).get(base_uri + download_url)
    return doc_response.content


def update_document_metadata(request: Request, hook: DocumentCreatedWebhook, repo_uuid: str, category: str, properties: list[dict]):
    base_uri = request.headers["x-dv-baseuri"]
    update_url = get_link_relations(request, repo_uuid, hook.doc.id)["update"]["href"]

    update_data = {
        "alterationText": f"updated properties by {APP_NAME}",
        "sourceCategory": category,
        "sourceId": DEFAULT_MAPPING_URL.format(repo_uuid=repo_uuid),
        "sourceProperties": {
            "properties": properties
        }
    }

    get_session(request).put(base_uri + update_url, json=update_data).raise_for_status()
