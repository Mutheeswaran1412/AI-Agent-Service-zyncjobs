from typing import Optional
from .base import Document
from .vector_store import VectorStore
from .retriever import Retriever


_DEFAULT_KNOWLEDGE = [
    Document(
        id="resume_best_practices",
        source="career_guide",
        text="""Resume Best Practices:
- Use strong action verbs (led, developed, implemented, optimized)
- Quantify achievements with numbers (% improvement, $ saved, team size)
- Keep to 1-2 pages maximum
- Use bullet points, not paragraphs
- Include a professional summary at the top
- List skills relevant to the target role
- Use consistent formatting and dates
- Optimize for ATS with relevant keywords from the job description
- Include LinkedIn profile and portfolio links""",
        metadata={"category": "resume", "importance": "high"},
    ),
    Document(
        id="ats_tips",
        source="career_guide",
        text="""ATS (Applicant Tracking System) Tips:
- Use standard section headings (Experience, Education, Skills)
- Include keywords from the job description naturally
- Avoid tables, columns, and graphics
- Use .docx or .pdf format as requested
- Spell out acronyms at least once
- List skills in a dedicated skills section
- Match the exact phrasing used in the job description""",
        metadata={"category": "ats", "importance": "high"},
    ),
    Document(
        id="interview_preparation",
        source="career_guide",
        text="""Interview Preparation Tips:
- Research the company thoroughly before the interview
- Prepare stories using the STAR method (Situation, Task, Action, Result)
- Practice common technical questions for your role
- Prepare 3-5 questions to ask the interviewer
- Follow up with a thank-you email within 24 hours
- Dress appropriately for the company culture
- Test your technology setup for virtual interviews""",
        metadata={"category": "interview", "importance": "medium"},
    ),
    Document(
        id="career_growth",
        source="career_guide",
        text="""Career Growth Strategies:
- Set clear short-term and long-term career goals
- Build a personal brand on LinkedIn
- Network with professionals in your target industry
- Continuously learn new skills through courses and certifications
- Seek mentorship from senior professionals
- Take on stretch assignments at work
- Document your achievements regularly""",
        metadata={"category": "career", "importance": "medium"},
    ),
    Document(
        id="skill_development",
        source="career_guide",
        text="""Skill Development Framework:
- Identify skills gap between current and target role
- Focus on both technical and soft skills
- Use online platforms (Coursera, Udemy, Pluralsight) for structured learning
- Build portfolio projects to demonstrate skills
- Contribute to open source for practical experience
- Get certified in relevant technologies
- Practice consistently with real-world projects""",
        metadata={"category": "skills", "importance": "medium"},
    ),
]


class KnowledgeBase:
    def __init__(self):
        self.store = VectorStore()
        self.retriever = Retriever(self.store)
        self._load_defaults()

    def _load_defaults(self):
        self.store.add_many(_DEFAULT_KNOWLEDGE)

    def add_document(self, doc: Document):
        self.store.add(doc)

    def add_documents(self, docs: list[Document]):
        self.store.add_many(docs)

    def remove_document(self, doc_id: str):
        self.store.remove(doc_id)

    def query(self, query: str, top_k: int = 3) -> list[Document]:
        return self.retriever.retrieve(query, top_k=top_k, min_score=0.05)

    def query_by_source(self, query: str, source: str, top_k: int = 3) -> list[Document]:
        return self.retriever.retrieve_by_source(query, source, top_k=top_k)

    def build_context(self, query: str, max_chars: int = 2000) -> str:
        docs = self.query(query, top_k=3)
        if not docs:
            return ""
        parts = []
        used = 0
        for doc in docs:
            chunk = f"[{doc.source}] {doc.text}"
            if used + len(chunk) > max_chars:
                remaining = max_chars - used
                if remaining > 100:
                    parts.append(chunk[:remaining])
                break
            parts.append(chunk)
            used += len(chunk)
        return "\n\n".join(parts)

    @property
    def document_count(self) -> int:
        return self.store.count


knowledge_base = KnowledgeBase()
