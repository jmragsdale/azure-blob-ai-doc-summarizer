![Azure](https://img.shields.io/badge/Azure-Functions-blue?logo=microsoft-azure)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)
![OpenAI](https://img.shields.io/badge/Azure-OpenAI-green)
![License](https://img.shields.io/badge/License-MIT-green)

# Azure Blob AI Document Summarizer

Automatically generate AI-powered summaries for documents uploaded to Azure Blob Storage using Azure OpenAI.

## Overview

This serverless application monitors an Azure Blob Storage container for new documents, extracts text content, generates concise summaries using Azure OpenAI, and stores the results as JSON files with metadata tags. Perfect for automating document processing workflows.

## Architecture

```
┌─────────────┐
│   Upload    │
│  Document   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Blob Storage           │
│  Container: incoming    │
└──────┬──────────────────┘
       │ (Blob Trigger)
       ▼
┌─────────────────────────┐
│  Azure Function         │
│  - Extract Text         │
│  - Call OpenAI          │
│  - Generate Summary     │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Azure OpenAI           │
│  (GPT-4/GPT-3.5)        │
└──────┬──────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  Blob Storage Outputs            │
│  - incoming/summary/<file>.json  │
│  - Blob Metadata Tags Applied    │
└──────────────────────────────────┘
```

## Features

- **Automated Document Processing**: Monitors `incoming` container for new documents
- **Multi-Format Support**: Handles PDF, TXT, DOCX, and Markdown files
- **AI-Powered Summaries**: Generates 5-bullet summaries + TL;DR using Azure OpenAI
- **Metadata Tagging**: Applies summary metadata as blob tags for searchability
- **Infrastructure as Code**: Complete Terraform configuration
- **Serverless Architecture**: Cost-effective Azure Functions-based solution

## Prerequisites

- Azure Subscription with appropriate permissions
- Terraform installed (v1.0+)
- Azure CLI installed and configured
- Azure Functions Core Tools (for local development)
- Azure OpenAI Service with deployed model

## Supported Document Formats

- **PDF** (`.pdf`) - Extracted using PyPDF2
- **Text** (`.txt`) - Plain text
- **Word** (`.docx`) - Extracted using python-docx
- **Markdown** (`.md`) - Plain text

## Setup

### 1. Deploy Azure OpenAI

First, create an Azure OpenAI resource and deploy a model:

```bash
# Create Azure OpenAI resource
az cognitiveservices account create \
  --name my-openai-resource \
  --resource-group my-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Deploy a model (e.g., GPT-4)
az cognitiveservices account deployment create \
  --name my-openai-resource \
  --resource-group my-rg \
  --deployment-name gpt-4 \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --scale-settings-scale-type "Standard"
```

### 2. Configure Terraform Variables

Edit `infra/variables.tf` or create `terraform.tfvars`:

```hcl
storage_account_name = "mydocsummarizer"
location            = "eastus"
openai_endpoint     = "https://my-openai-resource.openai.azure.com/"
openai_deployment   = "gpt-4"
```

### 3. Set Azure OpenAI Key

The OpenAI API key should be set as a Function App setting. Add it to `infra/main.tf`:

```hcl
app_settings = {
  AZURE_OPENAI_ENDPOINT    = var.openai_endpoint
  AZURE_OPENAI_DEPLOYMENT  = var.openai_deployment
  AZURE_OPENAI_API_KEY     = var.openai_api_key  # Or use Key Vault reference
}
```

### 4. Deploy Infrastructure

```bash
cd infra
terraform init
terraform apply
```

Review and confirm the deployment.

### 5. Deploy the Function App

**Option A: Zip Deploy**
```bash
cd function
pip install -r requirements.txt -t .
zip -r ../function.zip .
az functionapp deployment source config-zip \
  --resource-group my-rg \
  --name my-function-app \
  --src ../function.zip
```

**Option B: Azure Functions Core Tools**
```bash
cd function
func azure functionapp publish my-function-app
```

### 6. Test the Application

Upload a document:

```bash
az storage blob upload \
  --account-name mydocsummarizer \
  --container-name incoming \
  --name test-document.pdf \
  --file ./test-document.pdf
```

Check the summary:

```bash
# Download summary JSON
az storage blob download \
  --account-name mydocsummarizer \
  --container-name incoming \
  --name summary/test-document.json \
  --file ./summary.json

# View blob metadata
az storage blob metadata show \
  --account-name mydocsummarizer \
  --container-name incoming \
  --name test-document.pdf
```

## How It Works

1. **Document Upload**: User uploads a document to `incoming` container
2. **Trigger Activation**: Blob trigger activates the Azure Function
3. **Text Extraction**: Function extracts text based on file type
4. **AI Summarization**: Text is sent to Azure OpenAI for summarization
5. **Summary Generation**: OpenAI generates:
   - 5 key bullet points
   - A concise TL;DR
6. **Storage**:
   - Summary saved as `incoming/summary/<filename>.json`
   - Metadata tags applied to original blob

## Example Output

**Input**: `quarterly-report.pdf`

**Summary JSON** (`incoming/summary/quarterly-report.json`):
```json
{
  "filename": "quarterly-report.pdf",
  "tldr": "Q3 revenue increased 15% YoY to $2.3M with strong growth in enterprise segment, though operating expenses rose 8%.",
  "bullet_points": [
    "Total revenue reached $2.3M, representing 15% year-over-year growth",
    "Enterprise segment grew 22% and now accounts for 65% of total revenue",
    "Operating expenses increased 8% due to expanded sales team",
    "Customer retention rate improved to 94%, up from 89% in Q2",
    "Net profit margin decreased slightly to 12% from 14% previous quarter"
  ],
  "word_count": 3247,
  "processing_timestamp": "2025-10-03T10:30:00Z",
  "model_used": "gpt-4"
}
```

**Blob Metadata Tags**:
- `ai-processed`: "true"
- `summary-available`: "true"
- `word-count`: "3247"

## Cost Considerations

### Azure Functions
- **Consumption Plan**: 1M executions free/month, then $0.20 per million
- **Memory**: First 400,000 GB-s free, then $0.000016/GB-s

### Azure Blob Storage
- **Storage**: ~$0.018/GB/month (hot tier)
- **Operations**: Minimal cost for read/write operations

### Azure OpenAI
- **GPT-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **GPT-3.5 Turbo**: ~$0.0015 per 1K input tokens, ~$0.002 per 1K output tokens

**Estimated cost for 100 documents/month (avg 5 pages each)**: $5-15 USD

## Security Best Practices

### Use Managed Identity (Production)

Replace connection strings with Managed Identity:

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=credential
)
```

Update Terraform:
```hcl
resource "azurerm_role_assignment" "function_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_function_app.main.identity[0].principal_id
}
```

### Store Secrets in Key Vault

```hcl
resource "azurerm_key_vault_secret" "openai_key" {
  name         = "azure-openai-api-key"
  value        = var.openai_api_key
  key_vault_id = azurerm_key_vault.main.id
}

# Reference in Function App
app_settings = {
  AZURE_OPENAI_API_KEY = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.openai_key.id})"
}
```

### Enable Network Security

```hcl
resource "azurerm_storage_account_network_rules" "main" {
  storage_account_id = azurerm_storage_account.main.id
  default_action     = "Deny"
  
  ip_rules = ["YOUR_IP_ADDRESS"]
  virtual_network_subnet_ids = [azurerm_subnet.function.id]
}
```

## Customization

### Modify Summary Format

Edit the OpenAI prompt in the function code:

```python
prompt = f"""Summarize the following document in this exact format:

TL;DR: [One sentence summary, max 30 words]

KEY POINTS:
- [Point 1]
- [Point 2]
- [Point 3]
- [Point 4]
- [Point 5]

SENTIMENT: [Positive/Negative/Neutral]
TOPICS: [Comma-separated list]

Document:
{text_content}
"""
```

### Add Language Detection

```python
from azure.ai.textanalytics import TextAnalyticsClient

# Detect language before summarization
detected_language = text_analytics_client.detect_language(text_content)
```

### Process Images in PDFs

Add OCR capability using Azure Computer Vision:

```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

# Extract text from images in PDF
cv_client = ComputerVisionClient(endpoint, credential)
```

## Troubleshooting

### Function Timeout
Increase timeout in `host.json`:
```json
{
  "functionTimeout": "00:10:00"
}
```

### Large Document Processing
For documents >10MB, consider:
- Increasing function memory allocation
- Chunking text before sending to OpenAI
- Using GPT-3.5-turbo for cost efficiency

### OpenAI Rate Limits
Implement retry logic with exponential backoff:
```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def call_openai(prompt):
    # Your OpenAI call here
```

## Monitoring

### Enable Application Insights

```hcl
resource "azurerm_application_insights" "main" {
  name                = "doc-summarizer-insights"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
}
```

### Key Metrics to Monitor
- Function execution time
- OpenAI API latency
- Error rate
- Token usage costs
- Documents processed per day

## Cleanup

Remove all resources:

```bash
cd infra
terraform destroy
```

**⚠️ Warning**: This deletes the storage account and all documents. Backup important data first.

## Contributing

Contributions welcome! Please submit pull requests or open issues for bugs and feature requests.

## License

MIT License - see LICENSE file for details

## Related Projects

- [aws-s3-ai-image-tagger](https://github.com/jmragsdale/aws-s3-ai-image-tagger) - Similar serverless AI image processing for AWS

## Acknowledgments

- Powered by [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Infrastructure managed with [Terraform](https://www.terraform.io/)
