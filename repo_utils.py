import sys
from multiprocessing import Pool

import requests
from tqdm import tqdm

from core.constants import API_KEY, EDITOR

BASE_URI = "https://ai-contracts.d-velop.cloud"
REPO_ID = "befa2a91-fe9f-41b9-a098-e51d64c03805"
SOURCE_CATEGORY = "645fb"  # objectIdentifier
TARGET_CATEGORY = "ad7a1"  # objectIdentifier

SEARCH_URL = f"/dms/r/{REPO_ID}/srm?pagesize=1000&sourceid=/dms/r/{REPO_ID}/source"
DOCUMENT_URL = f"{BASE_URI}/dms/r/{REPO_ID}/o2m/"
DOWNLOAD_PREFIX = f"/dms/r/{REPO_ID}/o2/"
DOWNLOAD_SUFFIX = "{doc_id}/v/current/b/main/c"
SOURCE_ID = f"/dms/r/{REPO_ID}/source"


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Origin": BASE_URI,
    "Accept": "application/hal+json",
    "Content-Type": "application/hal+json"
}


def _upload_document(doc_id: str):
    response = requests.post(DOCUMENT_URL, headers=headers, json={
        "filename": f"{doc_id}.pdf",
        "sourceId": SOURCE_ID,
        "sourceCategory": TARGET_CATEGORY,
        "contentUri": DOWNLOAD_PREFIX + DOWNLOAD_SUFFIX.format(doc_id=doc_id),
        "sourceProperties": {
            "properties": [{
                    "key": "property_state",
                    "values": ["Processing"]
            }, {
                "key": "property_editor",
                "values": [EDITOR]
            }
            ]
        }
    })
    response.raise_for_status()


def start_analysis():
    response = requests.get(BASE_URI + SEARCH_URL + f"&sourcecategories=\"{SOURCE_CATEGORY}\"", headers=headers)
    doc_ids = [doc["id"] for doc in response.json()["items"]]
    with Pool(8) as p:
        list(tqdm(p.imap(_upload_document, doc_ids), total=len(doc_ids)))


def _set_editor(doc_id: str):
    response = requests.put(DOCUMENT_URL + doc_id + "/v/current", headers=headers, json={
        "sourceId": SOURCE_ID,
        "sourceProperties": {
            "properties": [{
                "key": "property_state",
                "values": ["Processing"]
            }, {
                "key": "property_editor",
                "values": [EDITOR]
            }
            ]
        }
    })
    response.raise_for_status()


def _delete_doc(doc_id: str):
    _set_editor(doc_id)
    response = requests.delete(DOCUMENT_URL + doc_id, headers=headers)
    response.raise_for_status()


def reset_repo():
    doc_ids = []
    next_url = SEARCH_URL
    while True:
        search_response = requests.get(BASE_URI + next_url, headers=headers).json()
        doc_ids.extend([doc["id"] for doc in search_response["items"] if doc["sourceCategories"][0] != SOURCE_CATEGORY])
        if not (next_url := search_response["_links"].get("next", {}).get("href")):
            break

    with Pool(8) as p:
        list(tqdm(p.imap(_delete_doc, doc_ids), total=len(doc_ids)))


if __name__ == "__main__":
    if sys.argv[1].lower() == "reset":
        reset_repo()
    elif sys.argv[1].lower() == "upload":
        start_analysis()
