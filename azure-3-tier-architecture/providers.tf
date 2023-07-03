terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.20.0"
    }
  }
}

provider "azurerm" {
  features {}
    subscription_id = "c61ea177-3092-49b2-b416-2742300b59fd"
    client_id       = "f50455de-3896-4ad5-ad2a-b7909786e4d7"
    client_secret   = "tdC8Q~JmK2MgF6Ul.~65j00Y4UYNy.cjXyet5bm0"
    tenant_id       = "d7d3f2c0-a6ee-4480-8526-ea05647335b3"
}
