from fastapi import APIRouter
from pydantic import BaseModel
from app.knowledge.knowledge_base import knowledge_base
from app.knowledge.base import Document

router = APIRouter()


class AddKnowledgeRequest(BaseModel):
    id: str
    text: str
    source: str = "custom"
    category: str = "general"


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("/add")
def add_knowledge(request: AddKnowledgeRequest):
    doc = Document(
        id=request.id,
        text=request.text,
        source=request.source,
        metadata={"category": request.category},
    )
    knowledge_base.add_document(doc)
    return {"success": True, "total_docs": knowledge_base.document_count}


@router.post("/query")
def query_knowledge(request: QueryRequest):
    docs = knowledge_base.query(request.query, top_k=request.top_k)
    return {
        "results": [
            {"id": d.id, "source": d.source, "text": d.text[:200], "score": round(d.score, 3)}
            for d in docs
        ],
        "count": len(docs),
    }


@router.get("/stats")
def knowledge_stats():
    return {"document_count": knowledge_base.document_count}
