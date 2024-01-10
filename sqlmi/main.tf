terraform {


  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0, < 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}


provider "azurerm" {
  features {}
  #subscription_id            = "b47f25f7-e6f4-4860-a93c-5848c0fe3373"
  #client_id                  = "ddce80fb-e1f2-4fc6-8813-3b00542506d7"
  #client_secret              = "jvD8Q~Ni4.4XkI3RV.4eB0PTdx_LiaNVyRmmSbiY"
  #tenant_id                  = "315e797d-2296-4233-8e57-2661418a3615"

  subscription_id = "c61ea177-3092-49b2-b416-2742300b59fd"
  client_id       = "15d69253-0408-46ff-9976-700421817840"
  client_secret   = "URE8Q~90JMoYEHQHxmo8XNk6c13ye8w20obGWcIB"
  tenant_id       = "d7d3f2c0-a6ee-4480-8526-ea05647335b3"

}

#variables

variable "prefix" {
  type        = string
  default     = "mi"
  description = "Prefix of the resource name"
}

variable "location" {
  type        = string
  description = "Enter the location where you want to deploy the resources"
  default     = "australiaeast"
}

variable "sku_name" {
  type        = string
  description = "Enter SKU"
  default     = "GP_Gen5"
}

variable "license_type" {
  type        = string
  description = "Enter license type"
  default     = "BasePrice"
}

variable "vcores" {
  type        = number
  description = "Enter number of vCores you want to deploy"
  default     = 8
}

variable "storage_size_in_gb" {
  type        = number
  description = "Enter storage size in GB"
  default     = 32
}

variable "password" {
  description = "Password"
  type        = string
  default     = "P@ssw0rd"
}

# Create resource group
resource "azurerm_resource_group" "example" {
  name     = "${random_pet.prefix.id}-rg"
  location = var.location
}

# Create security group
resource "azurerm_network_security_group" "example" {
  name                = "${random_pet.prefix.id}-nsg"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

# Create a virtual network
resource "azurerm_virtual_network" "example" {
  name                = "${random_pet.prefix.id}-vnet"
  resource_group_name = azurerm_resource_group.example.name
  address_space       = ["10.0.0.0/24"]
  location            = azurerm_resource_group.example.location
}

# Create a subnet
resource "azurerm_subnet" "example" {
  name                 = "${random_pet.prefix.id}-subnet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.0.0/27"]

  delegation {
    name = "managedinstancedelegation"

    service_delegation {
      name = "Microsoft.Sql/managedInstances"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action"
      ]
    }
  }
}

# Associate subnet and the security group
resource "azurerm_subnet_network_security_group_association" "example" {
  subnet_id                 = azurerm_subnet.example.id
  network_security_group_id = azurerm_network_security_group.example.id
}

# Create a route table
resource "azurerm_route_table" "example" {
  name                          = "${random_pet.prefix.id}-rt"
  location                      = azurerm_resource_group.example.location
  resource_group_name           = azurerm_resource_group.example.name
  disable_bgp_route_propagation = false
}

# Associate subnet and the route table
resource "azurerm_subnet_route_table_association" "example" {
  subnet_id      = azurerm_subnet.example.id
  route_table_id = azurerm_route_table.example.id

  depends_on = [azurerm_subnet_network_security_group_association.example]
}




resource "random_pet" "prefix" {
  prefix = var.prefix
  length = 1
}

