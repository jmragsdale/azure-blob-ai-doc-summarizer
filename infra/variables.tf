variable "project"               { type = string  default = "blob-ai-doc-summarizer" }
variable "rg_name"               { type = string  default = "rg-ai-summarizer" }
variable "location"              { type = string  default = "eastus" }
variable "storage_name"          { type = string  default = "jraisummarizerstore" }
variable "azure_openai_endpoint" { type = string }
variable "azure_openai_key"      { type = string }
variable "azure_openai_deployment" { type = string  default = "gpt-4o-mini" }
