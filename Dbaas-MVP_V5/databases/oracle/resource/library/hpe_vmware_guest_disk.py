#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Ansible Project
# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: vmware_guest_disk
short_description: Manage disks related to virtual machine in given vCenter infrastructure
description:
    - This module can be used to add, remove and update disks belonging to given virtual machine.
    - All parameters and VMware object names are case sensitive.
    - This module is destructive in nature, please read documentation carefully before proceeding.
    - Be careful while removing disk specified as this may lead to data loss.
author:
    - Abhijeet Kasurde (@Akasurde) <akasurde@redhat.com>
notes:
    - Tested on vSphere 6.0 and 6.5
requirements:
    - "python >= 2.6"
    - PyVmomi
options:
   name:
     description:
     - Name of the virtual machine.
     - This is a required parameter, if parameter C(uuid) or C(moid) is not supplied.
     type: str
   uuid:
     description:
     - UUID of the instance to gather facts if known, this is VMware's unique identifier.
     - This is a required parameter, if parameter C(name) or C(moid) is not supplied.
     type: str
   moid:
     description:
     - Managed Object ID of the instance to manage if known, this is a unique identifier only within a single vCenter instance.
     - This is required if C(name) or C(uuid) is not supplied.
     type: str
   folder:
     description:
     - Destination folder, absolute or relative path to find an existing guest.
     - This is a required parameter, only if multiple VMs are found with same name.
     - The folder should include the datacenter. ESX's datacenter is ha-datacenter
     - 'Examples:'
     - '   folder: /ha-datacenter/vm'
     - '   folder: ha-datacenter/vm'
     - '   folder: /datacenter1/vm'
     - '   folder: datacenter1/vm'
     - '   folder: /datacenter1/vm/folder1'
     - '   folder: datacenter1/vm/folder1'
     - '   folder: /folder1/datacenter1/vm'
     - '   folder: folder1/datacenter1/vm'
     - '   folder: /folder1/datacenter1/vm/folder2'
     type: str
   datacenter:
     description:
     - The datacenter name to which virtual machine belongs to.
     required: True
     type: str
   use_instance_uuid:
     description:
     - Whether to use the VMware instance UUID rather than the BIOS UUID.
     default: no
     type: bool
   disk:
     description:
     - A list of disks to add.
     - The virtual disk related information is provided using this list.
     - All values and parameters are case sensitive.
     - 'Valid attributes are:'
     - ' - C(size[_tb,_gb,_mb,_kb]) (integer): Disk storage size in specified unit.'
     - '   If C(size) specified then unit must be specified. There is no space allowed in between size number and unit.'
     - '   Only first occurrence in disk element will be considered, even if there are multiple size* parameters available.'
     - ' - C(type) (string): Valid values are:'
     - '     - C(thin) thin disk'
     - '     - C(eagerzeroedthick) eagerzeroedthick disk'
     - '     - C(thick) thick disk'
     - '     Default: C(thick) thick disk, no eagerzero.'
     - ' - C(disk_mode) (string): Type of disk mode. Valid values are:'
     - '     - C(persistent) Changes are immediately and permanently written to the virtual disk. This is default.'
     - '     - C(independent_persistent) Same as persistent, but not affected by snapshots.'
     - '     - C(independent_nonpersistent) Changes to virtual disk are made to a redo log and discarded at power off, but not affected by snapshots.'
     - ' - C(sharing) (bool): The sharing mode of the virtual disk. The default value is no sharing.'
     - '   Setting C(sharing) means that multiple virtual machines can write to the virtual disk.'
     - '   Sharing can only be set if C(type) is C(eagerzeroedthick).'
     - ' - C(datastore) (string): Name of datastore or datastore cluster to be used for the disk.'
     - ' - C(autoselect_datastore) (bool): Select the less used datastore. Specify only if C(datastore) is not specified.'
     - ' - C(scsi_controller) (integer): SCSI controller number. Valid value range from 0 to 3.'
     - '   Only 4 SCSI controllers are allowed per VM.'
     - '   Care should be taken while specifying C(scsi_controller) is 0 and C(unit_number) as 0 as this disk may contain OS.'
     - ' - C(unit_number) (integer): Disk Unit Number. Valid value range from 0 to 15. Only 15 disks are allowed per SCSI Controller.'
     - ' - C(scsi_type) (string): Type of SCSI controller. This value is required only for the first occurrence of SCSI Controller.'
     - '   This value is ignored, if SCSI Controller is already present or C(state) is C(absent).'
     - '   Valid values are C(buslogic), C(lsilogic), C(lsilogicsas) and C(paravirtual).'
     - '   C(paravirtual) is default value for this parameter.'
     - ' - C(destroy) (bool): If C(state) is C(absent), make sure the disk file is deleted from the datastore (default C(yes)).'
     - '   Added in version 2.10.'
     - ' - C(filename) (string): Existing disk image to be used. Filename must already exist on the datastore.'
     - '   Specify filename string in C([datastore_name] path/to/file.vmdk) format. Added in version 2.10.'
     - ' - C(state) (string): State of disk. This is either "absent" or "present".'
     - '   If C(state) is set to C(absent), disk will be removed permanently from virtual machine configuration and from VMware storage.'
     - '   If C(state) is set to C(present), disk will be added if not present at given SCSI Controller and Unit Number.'
     - '   If C(state) is set to C(present) and disk exists with different size, disk size is increased.'
     - '   Reducing disk size is not allowed.'
     suboptions:
       iolimit:
         description:
           - Section specifies the shares and limit for storage I/O resource.
         suboptions:
           limit:
             description:
               - Section specifies values for limit where the utilization of a virtual machine will not exceed, even if there are available resources.
           shares:
             description:
               - Specifies different types of shares user can add for the given disk.
             suboptions:
               level:
                 description:
                   - Specifies different level for the shares section.
                   - Valid values are low, normal, high, custom.
               level_value:
                 description:
                   - Custom value when C(level) is set as C(custom).
                 type: int
             type: list
             elements: dict
       shares:
         description:
           - section for iolimit section tells about what are all different types of shares user can add for disk.
         suboptions:
           level:
             description:
               - tells about different level for the shares section, valid values are low,normal,high,custom.
             type: str
           level_value:
             description:
               - custom value when level is set as custom.
             type: int
         type: list
         elements: dict
     default: []
     type: list
     elements: dict
extends_documentation_fragment:
- community.vmware.vmware.documentation

'''

EXAMPLES = r'''
- name: Add disks to virtual machine using UUID
  community.vmware.vmware_guest_disk:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
    datacenter: "{{ datacenter_name }}"
    validate_certs: no
    uuid: 421e4592-c069-924d-ce20-7e7533fab926
    disk:
      - size_mb: 10
        type: thin
        datastore: datacluster0
        state: present
        scsi_controller: 1
        unit_number: 1
        scsi_type: 'paravirtual'
        disk_mode: 'persistent'
      - size_gb: 10
        type: eagerzeroedthick
        state: present
        autoselect_datastore: True
        scsi_controller: 2
        scsi_type: 'buslogic'
        unit_number: 12
        disk_mode: 'independent_persistent'
      - size: 10Gb
        type: eagerzeroedthick
        state: present
        autoselect_datastore: True
        scsi_controller: 2
        scsi_type: 'buslogic'
        unit_number: 1
        disk_mode: 'independent_nonpersistent'
      - filename: "[datastore1] path/to/existing/disk.vmdk"
  delegate_to: localhost
  register: disk_facts

- name: Add disks with specified shares to the virtual machine
  community.vmware.vmware_guest_disk:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
    datacenter: "{{ datacenter_name }}"
    validate_certs: no
    disk:
      - size_gb: 1
        type: thin
        datastore: datacluster0
        state: present
        scsi_controller: 1
        unit_number: 1
        disk_mode: 'independent_persistent'
        shares:
          level: custom
          level_value: 1300
  delegate_to: localhost
  register: test_custom_shares

- name: create new disk with custom IO limits and shares in IO Limits
  community.vmware.vmware_guest_disk:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
    datacenter: "{{ datacenter_name }}"
    validate_certs: no
    disk:
      - size_gb: 1
        type: thin
        datastore: datacluster0
        state: present
        scsi_controller: 1
        unit_number: 1
        disk_mode: 'independent_persistent'
        iolimit:
            limit: 1506
            shares:
              level: custom
              level_value: 1305
  delegate_to: localhost
  register: test_custom_IoLimit_shares

- name: Remove disks from virtual machine using name
  community.vmware.vmware_guest_disk:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
    datacenter: "{{ datacenter_name }}"
    validate_certs: no
    name: VM_225
    disk:
      - state: absent
        scsi_controller: 1
        unit_number: 1
  delegate_to: localhost
  register: disk_facts

- name: Remove disk from virtual machine using moid
  community.vmware.vmware_guest_disk:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
    datacenter: "{{ datacenter_name }}"
    validate_certs: no
    moid: vm-42
    disk:
      - state: absent
        scsi_controller: 1
        unit_number: 1
  delegate_to: localhost
  register: disk_facts

- name: Remove disk from virtual machine but keep the VMDK file on the datastore
  community.vmware.vmware_guest_disk:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
    datacenter: "{{ datacenter_name }}"
    validate_certs: no
    name: VM_225
    disk:
      - state: absent
        scsi_controller: 1
        unit_number: 2
        destroy: no
  delegate_to: localhost
  register: disk_facts
'''

RETURN = r"""
disk_status:
    description: metadata about the virtual machine's disks after managing them
    returned: always
    type: dict
    sample: {
        "0": {
            "backing_datastore": "datastore2",
            "backing_disk_mode": "persistent",
            "backing_eagerlyscrub": false,
            "backing_filename": "[datastore2] VM_225/VM_225.vmdk",
            "backing_thinprovisioned": false,
            "backing_writethrough": false,
            "backing_uuid": "421e4592-c069-924d-ce20-7e7533fab926",
            "capacity_in_bytes": 10485760,
            "capacity_in_kb": 10240,
            "controller_key": 1000,
            "key": 2000,
            "label": "Hard disk 1",
            "summary": "10,240 KB",
            "unit_number": 0
        },
    }
"""

import re
try:
    from pyVmomi import vim
except ImportError:
    pass

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible_collections.community.vmware.plugins.module_utils.vmware import PyVmomi, vmware_argument_spec, wait_for_task, find_obj, get_all_objs


class PyVmomiHelper(PyVmomi):
    def __init__(self, module):
        super(PyVmomiHelper, self).__init__(module)
        self.desired_disks = self.params['disk']  # Match with vmware_guest parameter
        self.vm = None
        self.scsi_device_type = dict(lsilogic=vim.vm.device.VirtualLsiLogicController,
                                     paravirtual=vim.vm.device.ParaVirtualSCSIController,
                                     buslogic=vim.vm.device.VirtualBusLogicController,
                                     lsilogicsas=vim.vm.device.VirtualLsiLogicSASController)
        self.config_spec = vim.vm.ConfigSpec()
        self.config_spec.deviceChange = []

    def create_scsi_controller(self, scsi_type, scsi_bus_number):
        """
        Create SCSI Controller with given SCSI Type and SCSI Bus Number
        Args:
            scsi_type: Type of SCSI
            scsi_bus_number: SCSI Bus number to be assigned

        Returns: Virtual device spec for SCSI Controller

        """
        scsi_ctl = vim.vm.device.VirtualDeviceSpec()
        scsi_ctl.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        scsi_ctl.device = self.scsi_device_type[scsi_type]()
        scsi_ctl.device.unitNumber = 3
        scsi_ctl.device.busNumber = scsi_bus_number
        scsi_ctl.device.hotAddRemove = True
        #scsi_ctl.device.sharedBus = 'noSharing'
        scsi_ctl.device.sharedBus = 'physicalSharing'
        scsi_ctl.device.scsiCtlrUnitNumber = 7

        return scsi_ctl

    @staticmethod
    def create_scsi_disk(scsi_ctl_key, disk_index, disk_mode, disk_filename, sharing):
        """
        Create Virtual Device Spec for virtual disk
        Args:
            scsi_ctl_key: Unique SCSI Controller Key
            disk_index: Disk unit number at which disk needs to be attached
            disk_mode: Disk mode
            sharing: Disk sharing mode
            disk_filename: Path to the disk file on the datastore

        Returns: Virtual Device Spec for virtual disk

        """
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        disk_spec.device.backing.diskMode = disk_mode
        disk_spec.device.backing.sharing = sharing
        disk_spec.device.controllerKey = scsi_ctl_key
        disk_spec.device.unitNumber = disk_index

        if disk_filename is not None:
            disk_spec.device.backing.fileName = disk_filename
        else:
            disk_spec.fileOperation = vim.vm.device.VirtualDeviceSpec.FileOperation.create

        return disk_spec

    def reconfigure_vm(self, config_spec, device_type):
        """
        Reconfigure virtual machine after modifying device spec
        Args:
            config_spec: Config Spec
            device_type: Type of device being modified

        Returns: Boolean status 'changed' and actual task result

        """
        changed, results = (False, '')
        try:
            # Perform actual VM reconfiguration
            task = self.vm.ReconfigVM_Task(spec=config_spec)
            changed, results = wait_for_task(task)
        except vim.fault.InvalidDeviceSpec as invalid_device_spec:
            self.module.fail_json(msg="Failed to manage %s on given virtual machine due to invalid"
                                      " device spec : %s" % (device_type, to_native(invalid_device_spec.msg)),
                                  details="Please check ESXi server logs for more details.")
        except vim.fault.RestrictedVersion as e:
            self.module.fail_json(msg="Failed to reconfigure virtual machine due to"
                                      " product versioning restrictions: %s" % to_native(e.msg))

        return changed, results

    def get_ioandshares_diskconfig(self, disk_spec, disk):
        io_disk_spec = vim.StorageResourceManager.IOAllocationInfo()
        if 'iolimit' in disk:
            io_disk_spec.limit = disk['iolimit']['limit']
            if 'shares' in disk['iolimit']:
                shares_spec = vim.SharesInfo()
                shares_spec.level = disk['iolimit']['shares']['level']
                if shares_spec.level == 'custom':
                    shares_spec.shares = disk['iolimit']['shares']['level_value']
                io_disk_spec.shares = shares_spec
            disk_spec.device.storageIOAllocation = io_disk_spec
        if 'shares' in disk:
            shares_spec = vim.SharesInfo()
            shares_spec.level = disk['shares']['level']
            if shares_spec.level == 'custom':
                shares_spec.shares = disk['shares']['level_value']
            io_disk_spec.shares = shares_spec
            disk_spec.device.storageIOAllocation = io_disk_spec
        return disk_spec

    def get_sharing(self, disk, disk_type, disk_index):
        """
        Get the sharing mode of the virtual disk
        Args:
            disk: Virtual disk data object
            disk_type: Disk type of the virtual disk
            disk_index: Disk unit number at which disk needs to be attached

        Returns:
            sharing_mode: The sharing mode of the virtual disk

        """
        sharing = disk.get('sharing')
        if sharing and disk_type != 'eagerzeroedthick':
            self.module.fail_json(msg="Invalid 'sharing' mode specified for disk index [%s]. 'disk_mode'"
                                      " must be 'eagerzeroedthick' when 'sharing'." % disk_index)
        if sharing:
            sharing_mode = 'sharingMultiWriter'
        else:
            sharing_mode = 'sharingNone'
        return sharing_mode

    def ensure_disks(self, vm_obj=None):
        """
        Manage internal state of virtual machine disks
        Args:
            vm_obj: Managed object of virtual machine

        """
        # Set vm object
        self.vm = vm_obj
        # Sanitize user input
        disk_data = self.sanitize_disk_inputs()
        # Create stateful information about SCSI devices
        current_scsi_info = dict()
        results = dict(changed=False, disk_data=None, disk_changes=dict())

        # Deal with SCSI Controller
        for device in vm_obj.config.hardware.device:
            if isinstance(device, tuple(self.scsi_device_type.values())):
                # Found SCSI device
                if device.busNumber not in current_scsi_info:
                    device_bus_number = 1000 + device.busNumber
                    current_scsi_info[device_bus_number] = dict(disks=dict())

        scsi_changed = False
        for disk in disk_data:
            scsi_controller = disk['scsi_controller'] + 1000
            if scsi_controller not in current_scsi_info and disk['state'] == 'present':
                scsi_ctl = self.create_scsi_controller(disk['scsi_type'], disk['scsi_controller'])
                current_scsi_info[scsi_controller] = dict(disks=dict())
                self.config_spec.deviceChange.append(scsi_ctl)
                scsi_changed = True
        if scsi_changed:
            self.reconfigure_vm(self.config_spec, 'SCSI Controller')
            self.config_spec = vim.vm.ConfigSpec()
            self.config_spec.deviceChange = []

        # Deal with Disks
        for device in vm_obj.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                # Found Virtual Disk device
                if device.controllerKey not in current_scsi_info:
                    current_scsi_info[device.controllerKey] = dict(disks=dict())
                current_scsi_info[device.controllerKey]['disks'][device.unitNumber] = device

        disk_change_list = []
        for disk in disk_data:
            disk_change = False
            scsi_controller = disk['scsi_controller'] + 1000  # VMware auto assign 1000 + SCSI Controller
            if disk['disk_unit_number'] not in current_scsi_info[scsi_controller]['disks'] and disk['state'] == 'present':
                # Add new disk
                disk_spec = self.create_scsi_disk(scsi_controller, disk['disk_unit_number'], disk['disk_mode'], disk['filename'], disk['sharing'])
                if disk['filename'] is None:
                    disk_spec.device.capacityInKB = disk['size']
                if disk['disk_type'] == 'thin':
                    disk_spec.device.backing.thinProvisioned = True
                elif disk['disk_type'] == 'eagerzeroedthick':
                    disk_spec.device.backing.eagerlyScrub = True
                # get Storage DRS recommended datastore from the datastore cluster
                if disk['datastore_cluster'] is not None:
                    datastore_name = self.get_recommended_datastore(datastore_cluster_obj=disk['datastore_cluster'], disk_spec_obj=disk_spec)
                    disk['datastore'] = find_obj(self.content, [vim.Datastore], datastore_name)
                if disk['filename'] is not None:
                    disk_spec.device.backing.fileName = disk['filename']
                disk_spec.device.backing.datastore = disk['datastore']
                disk_spec.device.backing.sharing = disk['sharing']
                disk_spec = self.get_ioandshares_diskconfig(disk_spec, disk)
                self.config_spec.deviceChange.append(disk_spec)
                disk_change = True
                current_scsi_info[scsi_controller]['disks'][disk['disk_unit_number']] = disk_spec.device
                results['disk_changes'][disk['disk_index']] = "Disk created."
            elif disk['disk_unit_number'] in current_scsi_info[scsi_controller]['disks']:
                if disk['state'] == 'present':
                    disk_spec = vim.vm.device.VirtualDeviceSpec()
                    # set the operation to edit so that it knows to keep other settings
                    disk_spec.device = current_scsi_info[scsi_controller]['disks'][disk['disk_unit_number']]
                    # Edit and no resizing allowed
                    if disk['size'] < disk_spec.device.capacityInKB:
                        self.module.fail_json(msg="Given disk size at disk index [%s] is smaller than found (%d < %d)."
                                                  "Reducing disks is not allowed." % (disk['disk_index'],
                                                                                      disk['size'],
                                                                                      disk_spec.device.capacityInKB))
                    if disk['size'] != disk_spec.device.capacityInKB:
                        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                        disk_spec = self.get_ioandshares_diskconfig(disk_spec, disk)
                        disk_spec.device.capacityInKB = disk['size']
                        self.config_spec.deviceChange.append(disk_spec)
                        disk_change = True
                        results['disk_changes'][disk['disk_index']] = "Disk size increased."
                    else:
                        results['disk_changes'][disk['disk_index']] = "Disk already exists."

                elif disk['state'] == 'absent':
                    # Disk already exists, deleting
                    disk_spec = vim.vm.device.VirtualDeviceSpec()
                    disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                    if disk['destroy'] is True:
                        disk_spec.fileOperation = vim.vm.device.VirtualDeviceSpec.FileOperation.destroy
                    disk_spec.device = current_scsi_info[scsi_controller]['disks'][disk['disk_unit_number']]
                    self.config_spec.deviceChange.append(disk_spec)
                    disk_change = True
                    results['disk_changes'][disk['disk_index']] = "Disk deleted."

            if disk_change:
                # Adding multiple disks in a single attempt raises weird errors
                # So adding single disk at a time.
                self.reconfigure_vm(self.config_spec, 'disks')
                self.config_spec = vim.vm.ConfigSpec()
                self.config_spec.deviceChange = []
            disk_change_list.append(disk_change)

        if any(disk_change_list):
            results['changed'] = True
        results['disk_data'] = self.gather_disk_facts(vm_obj=self.vm)
        self.module.exit_json(**results)

    def sanitize_disk_inputs(self):
        """
        Check correctness of disk input provided by user
        Returns: A list of dictionary containing disk information

        """
        disks_data = list()
        if not self.desired_disks:
            self.module.exit_json(changed=False, msg="No disks provided for virtual"
                                                     " machine '%s' for management." % self.vm.name)

        for disk_index, disk in enumerate(self.desired_disks):
            # Initialize default value for disk
            current_disk = dict(disk_index=disk_index,
                                state='present',
                                destroy=True,
                                filename=None,
                                datastore_cluster=None,
                                datastore=None,
                                autoselect_datastore=True,
                                disk_unit_number=0,
                                scsi_controller=0,
                                disk_mode='persistent',
                                sharing=False)
            # Check state
            if 'state' in disk:
                if disk['state'] not in ['absent', 'present']:
                    self.module.fail_json(msg="Invalid state provided '%s' for disk index [%s]."
                                              " State can be either - 'absent', 'present'" % (disk['state'],
                                                                                              disk_index))
                else:
                    current_disk['state'] = disk['state']

            # By default destroy file from datastore if 'destroy' parameter is not provided
            if current_disk['state'] == 'absent':
                current_disk['destroy'] = disk.get('destroy', True)
            elif current_disk['state'] == 'present':
                # Select datastore or datastore cluster
                if 'datastore' in disk:
                    if 'autoselect_datastore' in disk:
                        self.module.fail_json(msg="Please specify either 'datastore' "
                                                  "or 'autoselect_datastore' for disk index [%s]" % disk_index)

                    # Check if given value is datastore or datastore cluster
                    datastore_name = disk['datastore']
                    datastore_cluster = find_obj(self.content, [vim.StoragePod], datastore_name)
                    datastore = find_obj(self.content, [vim.Datastore], datastore_name)

                    if datastore is None and datastore_cluster is None:
                        self.module.fail_json(msg="Failed to find datastore or datastore cluster named '%s' "
                                                  "in given configuration." % disk['datastore'])
                    if datastore_cluster:
                        # If user specified datastore cluster, keep track of that for determining datastore later
                        current_disk['datastore_cluster'] = datastore_cluster
                    elif datastore:
                        current_disk['datastore'] = datastore
                    current_disk['autoselect_datastore'] = False
                elif 'autoselect_datastore' in disk:
                    # Find datastore which fits requirement
                    datastores = get_all_objs(self.content, [vim.Datastore])
                    if not datastores:
                        self.module.fail_json(msg="Failed to gather information about"
                                                  " available datastores in given datacenter.")
                    datastore = None
                    datastore_freespace = 0
                    for ds in datastores:
                        if ds.summary.freeSpace > datastore_freespace:
                            # If datastore field is provided, filter destination datastores
                            datastore = ds
                            datastore_freespace = ds.summary.freeSpace
                    current_disk['datastore'] = datastore

                if 'datastore' not in disk and 'autoselect_datastore' not in disk and 'filename' not in disk:
                    self.module.fail_json(msg="Either 'datastore' or 'autoselect_datastore' is"
                                              " required parameter while creating disk for "
                                              "disk index [%s]." % disk_index)

                if 'filename' in disk:
                    current_disk['filename'] = disk['filename']

                if [x for x in disk.keys() if x.startswith('size_') or x == 'size']:
                    # size, size_tb, size_gb, size_mb, size_kb
                    disk_size_parse_failed = False
                    if 'size' in disk:
                        size_regex = re.compile(r'(\d+(?:\.\d+)?)([tgmkTGMK][bB])')
                        disk_size_m = size_regex.match(disk['size'])
                        if disk_size_m:
                            expected = disk_size_m.group(1)
                            unit = disk_size_m.group(2)
                        else:
                            disk_size_parse_failed = True
                        try:
                            if re.match(r'\d+\.\d+', expected):
                                # We found float value in string, let's typecast it
                                expected = float(expected)
                            else:
                                # We found int value in string, let's typecast it
                                expected = int(expected)
                        except (TypeError, ValueError, NameError):
                            disk_size_parse_failed = True
                    else:
                        # Even multiple size_ parameter provided by user,
                        # consider first value only
                        param = [x for x in disk.keys() if x.startswith('size_')][0]
                        unit = param.split('_')[-1]
                        disk_size = disk[param]
                        if isinstance(disk_size, (float, int)):
                            disk_size = str(disk_size)

                        try:
                            if re.match(r'\d+\.\d+', disk_size):
                                # We found float value in string, let's typecast it
                                expected = float(disk_size)
                            else:
                                # We found int value in string, let's typecast it
                                expected = int(disk_size)
                        except (TypeError, ValueError, NameError):
                            disk_size_parse_failed = True

                    if disk_size_parse_failed:
                        # Common failure
                        self.module.fail_json(msg="Failed to parse disk size for disk index [%s],"
                                                  " please review value provided"
                                                  " using documentation." % disk_index)

                    disk_units = dict(tb=3, gb=2, mb=1, kb=0)
                    unit = unit.lower()
                    if unit in disk_units:
                        current_disk['size'] = expected * (1024 ** disk_units[unit])
                    else:
                        self.module.fail_json(msg="%s is not a supported unit for disk size for disk index [%s]."
                                                  " Supported units are ['%s']." % (unit,
                                                                                    disk_index,
                                                                                    "', '".join(disk_units.keys())))

                elif current_disk['filename'] is None:
                    # No size found but disk, fail
                    self.module.fail_json(msg="No size, size_kb, size_mb, size_gb or size_tb"
                                              " attribute found into disk index [%s] configuration." % disk_index)
            # Check SCSI controller key
            if 'scsi_controller' in disk:
                try:
                    temp_disk_controller = int(disk['scsi_controller'])
                except ValueError:
                    self.module.fail_json(msg="Invalid SCSI controller ID '%s' specified"
                                              " at index [%s]" % (disk['scsi_controller'], disk_index))
                if temp_disk_controller not in range(0, 4):
                    # Only 4 SCSI controllers are allowed per VM
                    self.module.fail_json(msg="Invalid SCSI controller ID specified [%s],"
                                              " please specify value between 0 to 3 only." % temp_disk_controller)
                current_disk['scsi_controller'] = temp_disk_controller
            else:
                self.module.fail_json(msg="Please specify 'scsi_controller' under disk parameter"
                                          " at index [%s], which is required while creating disk." % disk_index)
            # Check for disk unit number
            if 'unit_number' in disk:
                try:
                    temp_disk_unit_number = int(disk['unit_number'])
                except ValueError:
                    self.module.fail_json(msg="Invalid Disk unit number ID '%s'"
                                              " specified at index [%s]" % (disk['unit_number'], disk_index))
                if temp_disk_unit_number not in range(0, 16):
                    self.module.fail_json(msg="Invalid Disk unit number ID specified for disk [%s] at index [%s],"
                                              " please specify value between 0 to 15"
                                              " only (excluding 7)." % (temp_disk_unit_number, disk_index))

                if temp_disk_unit_number == 7:
                    self.module.fail_json(msg="Invalid Disk unit number ID specified for disk at index [%s],"
                                              " please specify value other than 7 as it is reserved"
                                              "for SCSI Controller" % disk_index)
                current_disk['disk_unit_number'] = temp_disk_unit_number

            else:
                self.module.fail_json(msg="Please specify 'unit_number' under disk parameter"
                                          " at index [%s], which is required while creating disk." % disk_index)

            # Type of Disk
            disk_type = disk.get('type', 'thick').lower()
            if disk_type not in ['thin', 'thick', 'eagerzeroedthick']:
                self.module.fail_json(msg="Invalid 'disk_type' specified for disk index [%s]. Please specify"
                                          " 'disk_type' value from ['thin', 'thick', 'eagerzeroedthick']." % disk_index)
            current_disk['disk_type'] = disk_type

            # Mode of Disk
            temp_disk_mode = disk.get('disk_mode', 'persistent').lower()
            if temp_disk_mode not in ['persistent', 'independent_persistent', 'independent_nonpersistent']:
                self.module.fail_json(msg="Invalid 'disk_mode' specified for disk index [%s]. Please specify"
                                          " 'disk_mode' value from ['persistent', 'independent_persistent', 'independent_nonpersistent']." % disk_index)
            current_disk['disk_mode'] = temp_disk_mode

            # Sharing mode of disk
            current_disk['sharing'] = self.get_sharing(disk, disk_type, disk_index)

            # SCSI Controller Type
            scsi_contrl_type = disk.get('scsi_type', 'paravirtual').lower()
            if scsi_contrl_type not in self.scsi_device_type.keys():
                self.module.fail_json(msg="Invalid 'scsi_type' specified for disk index [%s]. Please specify"
                                          " 'scsi_type' value from ['%s']" % (disk_index,
                                                                              "', '".join(self.scsi_device_type.keys())))
            current_disk['scsi_type'] = scsi_contrl_type
            if 'shares' in disk:
                current_disk['shares'] = disk['shares']
            if 'iolimit' in disk:
                current_disk['iolimit'] = disk['iolimit']
            disks_data.append(current_disk)
        return disks_data

    def get_recommended_datastore(self, datastore_cluster_obj, disk_spec_obj):
        """
        Return Storage DRS recommended datastore from datastore cluster
        Args:
            datastore_cluster_obj: datastore cluster managed object

        Returns: Name of recommended datastore from the given datastore cluster,
                 Returns None if no datastore recommendation found.

        """
        # Check if Datastore Cluster provided by user is SDRS ready
        sdrs_status = datastore_cluster_obj.podStorageDrsEntry.storageDrsConfig.podConfig.enabled
        if sdrs_status:
            # We can get storage recommendation only if SDRS is enabled on given datastorage cluster
            disk_loc = vim.storageDrs.PodSelectionSpec.DiskLocator()
            pod_config = vim.storageDrs.PodSelectionSpec.VmPodConfig()
            pod_config.storagePod = datastore_cluster_obj
            pod_config.disk = [disk_loc]
            pod_sel_spec = vim.storageDrs.PodSelectionSpec()
            pod_sel_spec.initialVmConfig = [pod_config]
            storage_spec = vim.storageDrs.StoragePlacementSpec()
            storage_spec.configSpec = vim.vm.ConfigSpec()
            storage_spec.configSpec.deviceChange.append(disk_spec_obj)
            storage_spec.resourcePool = self.vm.resourcePool
            storage_spec.podSelectionSpec = pod_sel_spec
            storage_spec.vm = self.vm
            storage_spec.type = 'reconfigure'

            try:
                rec = self.content.storageResourceManager.RecommendDatastores(storageSpec=storage_spec)
                rec_action = rec.recommendations[0].action[0]
                return rec_action.destination.name
            except Exception:
                # There is some error so we fall back to general workflow
                pass
        datastore = None
        datastore_freespace = 0
        for ds in datastore_cluster_obj.childEntity:
            if ds.summary.freeSpace > datastore_freespace:
                # If datastore field is provided, filter destination datastores
                datastore = ds
                datastore_freespace = ds.summary.freeSpace
        if datastore:
            return datastore.name
        return None

    @staticmethod
    def gather_disk_facts(vm_obj):
        """
        Gather facts about VM's disks
        Args:
            vm_obj: Managed object of virtual machine

        Returns: A list of dict containing disks information

        """
        disks_facts = dict()
        if vm_obj is None:
            return disks_facts

        disk_index = 0
        for disk in vm_obj.config.hardware.device:
            if isinstance(disk, vim.vm.device.VirtualDisk):
                if disk.storageIOAllocation is None:
                    disk.storageIOAllocation = vim.StorageResourceManager.IOAllocationInfo()
                    disk.storageIOAllocation.shares = vim.SharesInfo()
                if disk.shares is None:
                    disk.shares = vim.SharesInfo()
                disks_facts[disk_index] = dict(
                    key=disk.key,
                    label=disk.deviceInfo.label,
                    summary=disk.deviceInfo.summary,
                    backing_filename=disk.backing.fileName,
                    backing_datastore=disk.backing.datastore.name,
                    backing_disk_mode=disk.backing.diskMode,
                    backing_sharing=disk.backing.sharing,
                    backing_writethrough=disk.backing.writeThrough,
                    backing_thinprovisioned=disk.backing.thinProvisioned,
                    backing_eagerlyscrub=bool(disk.backing.eagerlyScrub),
                    backing_uuid=disk.backing.uuid,
                    controller_key=disk.controllerKey,
                    unit_number=disk.unitNumber,
                    iolimit_limit=disk.storageIOAllocation.limit,
                    iolimit_shares_level=disk.storageIOAllocation.shares.level,
                    iolimit_shares_limit=disk.storageIOAllocation.shares.shares,
                    shares_level=disk.shares.level,
                    shares_limit=disk.shares.shares,
                    capacity_in_kb=disk.capacityInKB,
                    capacity_in_bytes=disk.capacityInBytes,
                )
                disk_index += 1
        return disks_facts


def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(
        name=dict(type='str'),
        uuid=dict(type='str'),
        moid=dict(type='str'),
        folder=dict(type='str'),
        datacenter=dict(type='str', required=True),
        disk=dict(type='list', default=[], elements='dict'),
        use_instance_uuid=dict(type='bool', default=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['name', 'uuid', 'moid']
        ]
    )

    if module.params['folder']:
        # FindByInventoryPath() does not require an absolute path
        # so we should leave the input folder path unmodified
        module.params['folder'] = module.params['folder'].rstrip('/')

    pyv = PyVmomiHelper(module)
    # Check if the VM exists before continuing
    vm = pyv.get_vm()

    if not vm:
        # We unable to find the virtual machine user specified
        # Bail out
        vm_id = (module.params.get('name') or module.params.get('uuid') or module.params.get('moid'))
        module.fail_json(msg="Unable to manage disks for non-existing"
                             " virtual machine '%s'." % vm_id)

    # VM exists
    try:
        pyv.ensure_disks(vm_obj=vm)
    except Exception as exc:
        module.fail_json(msg="Failed to manage disks for virtual machine"
                             " '%s' with exception : %s" % (vm.name,
                                                            to_native(exc)))


if __name__ == '__main__':
    main()
