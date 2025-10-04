import os, json
from io import BytesIO
from openai import AzureOpenAI

def _client():
    return AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_KEY"],
        api_version="2024-08-01-preview",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )

def summarize_text(text: str):
    prompt = "Summarize in JSON with keys: bullets (array of 5), tldr (string). Plain English."
    resp = _client().chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT","gpt-4o-mini"),
        messages=[{"role":"user","content":f"{prompt}\n---\n{text[:6000]}"}],
        temperature=0.2
    )
    content = resp.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        return {"bullets":[content], "tldr":content[:160]}

def extract_text(filename, content: bytes):
    name = filename.lower()
    if name.endswith((".txt",".md")):
        return content.decode(errors="ignore")
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        pdf = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if name.endswith(".docx"):
        import docx
        d = docx.Document(BytesIO(content))
        return "\n".join(p.text for p in d.paragraphs)
    return "Unsupported file; provide txt/pdf/docx."
