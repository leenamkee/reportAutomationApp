from PyPDF2 import PdfReader

def load_files(files):
    texts = []
    for file in files[:5]:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif file.name.endswith(".txt"):
            text = file.read().decode("utf-8")
        else:
            text = ""
        texts.append(text)
    return texts
