import datetime

from pydantic import BaseModel


class Document(BaseModel):
    id: str
    dateCreated: datetime.datetime
    fileExtension: str
    size: int

class DocType(BaseModel):
    id: str
    name: str
    type: str

class DocumentCreatedWebhook(BaseModel):
    doc: Document
    docType: DocType