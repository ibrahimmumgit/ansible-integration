# -------------------------------------------------------------
# File Name: tier-2app.tf
# Deploy a new VM from a template.
#
# REQUIREMENTS #1: vsphere_tag_category and vsphere_tag must exist
#                  cd helpers/tags && terraform apply
# REQUIREMENTS #2: deploy_vsphere_folder and deploy_vsphere_sub_folder must exist
#                  cd helpers/folders && terraform apply
#
# Tue Nov 2 12:59:12 BST 2020 - juliusn - initial script
# -------------------------------------------------------------

# -------------------------------------------------------------
# Create web server - tier-2app
# -------------------------------------------------------------

module "tier-2app" {
    source          = "../modules/vsphere-deploy-linux-vm/"
    # -------------------------------------------------------------
    # INFRASTRUCTURE - VMware vSphere vCenter settings 
    # -------------------------------------------------------------
    vsphere_datacenter   = "c3"
    vsphere_cluster      = "dojo9-vmware"
    vsphere_datastore    = "datastore3-1"


    # -------------------------------------------------------------
    # GUEST - VMware vSphere VM settings 
    # -------------------------------------------------------------
    guest_template          = "tierubuntu"
    guest_template_folder   = "Templates"
    guest_vm_name           = "tier-app01"
    guest_vcpu              = "1"
    guest_memory            = "4096"
    guest_disk0_size        = "80"
    guest_network           = "MGMT-PG"
    guest_ipv4_address      = "192.168.9.22"
    guest_ipv4_netmask      = "24"
    guest_ipv4_gateway      = "192.168.9.254"
    guest_dns_servers       = "8.8.8.8"
    guest_dns_suffix        = "test.local"
    guest_domain            = "test.local"
    shell                   = "app.sh"

}

output "tier-2app-VM-ip" {
	value = module.tier-2app.VM-ip
}
output "tier-2app-VM-guest-ip" {
	value = module.tier-2app.VM-guest-ip
}
