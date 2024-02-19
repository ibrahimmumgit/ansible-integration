# -------------------------------------------------------------
# File Name: main.tf
# Deploy a new VM from a template.
#
# REQUIREMENTS #1: vsphere_tag_category and vsphere_tag must exist
#                  cd helpers/tags && terraform apply
# REQUIREMENTS #2: deploy_vsphere_folder and deploy_vsphere_sub_folder must exist
#                  cd helpers/folders && terraform apply
#
# Tue Nov 2 12:59:12 BST 2020 - juliusn - initial script
# -------------------------------------------------------------

# -- Provider
provider "vsphere" {
    user                    = var.user
    password                = var.password
    vsphere_server          = var.vsphere_server
    allow_unverified_ssl    = true
}

# -------------------------------------------------------------
# VM deployment - VM configuration files
# -------------------------------------------------------------

module "vm-dbdeployment" {
    source = "./vm-dbdeployment"
}

 module "vm-appdeployment" {
    source = "./vm-appdeployment"
    depends_on = [module.vm-dbdeployment]
} 


# -------------------------------------------------------------
# Example - output files
# -------------------------------------------------------------




