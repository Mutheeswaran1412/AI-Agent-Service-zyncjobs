import os
import tempfile
from .base_tool import BaseTool


class PDFTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="pdf_tool",
            description="Extracts text from PDF files using PyMuPDF (fallback: pdfminer)",
        )
        self._parser = None

    def run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF not found: {file_path}")

        return self._extract(file_path)

    def run_from_bytes(self, data: bytes) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            return self._extract(tmp_path)
        finally:
            os.unlink(tmp_path)

    def _extract(self, path: str) -> str:
        try:
            import fitz
            text = []
            with fitz.open(path) as doc:
                for page in doc:
                    text.append(page.get_text())
            return "\n".join(text)
        except ImportError:
            pass

        try:
            from pdfminer.high_level import extract_text
            return extract_text(path)
        except ImportError:
            pass

        raise ImportError(
            "No PDF library found. Install one:\n"
            "  pip install PyMuPDF\n"
            "  or\n"
            "  pip install pdfminer.six"
        )
