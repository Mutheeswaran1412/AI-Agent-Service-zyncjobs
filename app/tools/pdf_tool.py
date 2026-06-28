from .base_tool import BaseTool


class PDFTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="pdf_tool",
            description="Extracts text from PDF resumes",
        )

    def run(self, file_path: str) -> str:
        # placeholder — will integrate PyMuPDF / pdfminer later
        raise NotImplementedError("PDF extraction not yet implemented")
