# -------------------------------------------------------------
# File Name: tier-1db.tf
# Deploy a new VM from a template.
#
#
# -------------------------------------------------------------

# -------------------------------------------------------------
# Create web server - tier-1db
# -------------------------------------------------------------

module "tier-1db" {
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
    guest_vm_name           = "tier-db01"
    guest_vcpu              = "1"
    guest_memory            = "4096"
    guest_disk0_size        = "80"
    guest_network           = "MGMT-PG"
    guest_ipv4_address      = "192.168.9.21"
    guest_ipv4_netmask      = "24"
    guest_ipv4_gateway      = "192.168.9.254"
    guest_dns_servers       = "8.8.8.8"
    guest_dns_suffix        = "test.local"
    guest_domain            = "test.local"
    shell                   = "db.sh"

}

output "tier-1db-VM-ip" {
	value = module.tier-1db.VM-ip
}
output "tier-1db-VM-guest-ip" {
	value = module.tier-1db.VM-guest-ip
}
