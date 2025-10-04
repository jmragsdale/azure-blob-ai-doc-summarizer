import os, json, logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from shared_openai import summarize_text, extract_text

BLOB_CONN = os.environ["BLOB_CONN_STR"]
CONTAINER_OUT = os.environ.get("CONTAINER_OUT","summary")

def main(myblob: func.InputStream):
    filename = myblob.name.split("/")[-1]
    content = myblob.read()
    text = extract_text(filename, content)
    summary = summarize_text(text)

    # output summary JSON
    container = myblob.name.split("/",1)[0]
    out_blob = f"{CONTAINER_OUT}/{filename}.json"
    bsc = BlobServiceClient.from_connection_string(BLOB_CONN)
    out_client = bsc.get_blob_client(container=container, blob=out_blob)
    out_client.upload_blob(json.dumps(summary, indent=2), overwrite=True)

    # tag input blob
    try:
        in_blob = myblob.name.split("/",1)[1]
        in_client = bsc.get_blob_client(container=container, blob=in_blob)
        in_client.set_blob_tags({"ai":"summarized","length":str(len(text))})
    except Exception as e:
        logging.warning(f"Tagging failed: {e}")

    logging.info(f"Wrote {out_blob}")
