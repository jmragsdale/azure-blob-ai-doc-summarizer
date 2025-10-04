terraform {
  required_providers { azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" } }
}
provider "azurerm" { features {} }

resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.location
}

resource "azurerm_storage_account" "sa" {
  name                     = var.storage_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "incoming" {
  name                  = "incoming"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

resource "azurerm_service_plan" "plan" {
  name                = "${var.project}-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "func" {
  name                       = "${var.project}-func"
  location                   = var.location
  resource_group_name        = azurerm_resource_group.rg.name
  storage_account_name       = azurerm_storage_account.sa.name
  service_plan_id            = azurerm_service_plan.plan.id
  site_config { application_stack { python_version = "3.11" } }
  app_settings = {
    "BLOB_CONN_STR"            = azurerm_storage_account.sa.primary_connection_string
    "CONTAINER_OUT"            = "summary"
    "AZURE_OPENAI_ENDPOINT"    = var.azure_openai_endpoint
    "AZURE_OPENAI_KEY"         = var.azure_openai_key
    "AZURE_OPENAI_DEPLOYMENT"  = var.azure_openai_deployment
    "AzureWebJobsStorage"      = azurerm_storage_account.sa.primary_connection_string
    "FUNCTIONS_WORKER_RUNTIME" = "python"
  }
}
