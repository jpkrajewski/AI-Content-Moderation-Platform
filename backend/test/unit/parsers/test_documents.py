from moderation.parsers.documents import extract_text_from_document


def test_extract_docx(test_folder):
    text = extract_text_from_document(str(test_folder / "example.docx"))
    assert text

def test_extract_pdf(test_folder):
    text = extract_text_from_document(str(test_folder / "file-example_PDF_1MB.pdf"))