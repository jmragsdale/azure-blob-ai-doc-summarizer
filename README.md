# Blob → AI Doc Summarizer (Azure OpenAI + Blob + Functions)

Upload `.pdf/.txt/.docx/.md` into container `incoming`. An Azure Function (Blob Trigger) extracts text, calls Azure OpenAI for a 5-bullet summary + TL;DR, then writes `summary/<file>.json` back to the same container and tags the original blob.

## Quick start
1. Set Azure OpenAI endpoint/deployment/key in Function App app settings (see `infra/main.tf`).
2. Deploy the function (zip deploy or `func azure functionapp publish`).
3. Upload a doc to `incoming/` and check `incoming/summary/<file>.json`.

> Use Managed Identity in production; this sample uses a connection string for simplicity.

