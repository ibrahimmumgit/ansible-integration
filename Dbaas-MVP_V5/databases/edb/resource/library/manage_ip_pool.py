#!/usr/bin/python
import json
try:
	from netaddr import *
	_module_not_found = False
except ImportError:
	_module_not_found = True

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

def exclude_ips(ip_prefix, all_ips, exclude_range):
	if not exclude_range:
		return all_ips
	range_split = exclude_range.split('-')
	if len(range_split) < 2:
		raise Exception('Invalid range specified')

	if range_split[0] > range_split[1]:
		raise Exception('Invalid range specified')

	range_start = ip_prefix+'.'+range_split[0]
	range_end = ip_prefix+'.'+range_split[1]

	ip_list = list(iter_iprange(range_start, range_end))
	exclude_ips = ['%s' % ip for ip in ip_list]

	pool_ips = []
	for ip in all_ips:
		if ip not in exclude_ips:
			pool_ips.append(ip)

	return pool_ips

def write_json_to_file(data, fname):
	if not data:
		LOG.debug("Writing empty data into json file")
		return
	try:
		with open(fname, 'w') as outfile:
			json.dump(data, outfile, indent=4)
			outfile.flush()
	except Exception as exp:
		raise Exception("Could not write to file \'{}\'. msg: {}".format(fname, exp))

def read_json_from_file(file_name):

	try:
		with open(file_name) as json_file:
			json_data = json.load(json_file)
			if json_data:
				return json_data
	except Exception as exp:
		raise Exception("Failed to read file \'{}\'. msg: {}".format(file_name, exp))

def create_ip_pool(ip_network, ip_range, exclude_range, path):
	range_split = ip_range.split('-')

	try:
		ip_net = IPNetwork(ip_network)
	except Exception as exp:
		raise Exception('Invalid network specified')

	if len(range_split) < 2:
		raise Exception('Invalid range specified')

	if range_split[0] > range_split[1]:
		raise Exception('Invalid range specified')

	ip_prefix = '.'.join(ip_network.split('.')[:3])

	range_start = ip_prefix+'.'+range_split[0]
	range_end = ip_prefix+'.'+range_split[1]

	ip_list = list(iter_iprange(range_start, range_end))
	all_ips = ['%s' % ip for ip in ip_list if '%s' % ip in ip_net]

	if len(all_ips) == 0:
		raise Exception('No IPs available, please check inputs!')

	pool_ips = exclude_ips(ip_prefix, all_ips, exclude_range)

	if len(pool_ips) == 0:
		raise Exception('No IPs available, please check inputs!')

	pool = []
	for ip in pool_ips:
		pool.append(dict(ip=ip,reserved=False,cluster_name =""))

	write_json_to_file(pool, path)

def fetch_ips_from_pool(cluster_name, count, path):
	pool = read_json_from_file(path)
	ips = [ip_fact['ip'] for ip_fact in pool if not ip_fact['reserved']]
	if count > len(ips):
		raise Exception("Insufficient IPs in the pool")
	usable_ips = ips[:count]
	for ip_fact in pool:
		if ip_fact['ip'] in usable_ips:
			ip_fact['reserved'] = True
			ip_fact['cluster_name'] = cluster_name
	write_json_to_file(pool, path)
	return usable_ips

def verify_ips_from_pool(count, path):
	pool = read_json_from_file(path)
	ips = [ip_fact['ip'] for ip_fact in pool if not ip_fact['reserved']]
	if count > len(ips):
		raise Exception("Insufficient IPs in the pool")

def release_ips_pool(ips, path):
	pool = read_json_from_file(path)
	for ip_fact in pool:
		if ip_fact['ip'] in ips:
			ip_fact['reserved'] = False
			ip_fact['cluster_name'] = ""
	write_json_to_file(pool, path)

def display_ip_pool(path):
	pool = read_json_from_file(path)
	return pool

def main():
	module = AnsibleModule(
		argument_spec=dict(
		ip_net=dict(required=False, type='str'),
		ip_range=dict(required=False, type='str'),
		exclude_range=dict(required=False, type='str', default=''),
		action=dict(required=True, choices=['create_pool', 'verify_ips', 'reserve_ips', 'release_ips', 'view_pool'], type='str'),
		cluster_name=dict(required=False, type='str'),
		ips=dict(required=False, type='list'),
		count=dict(required=False, type='int'),
		path=dict(required=False, default='/opt/dbaas/ip_pool.json', type='str'),
	))

	ip_net = module.params['ip_net']
	ip_range = module.params['ip_range']
	exclude_range = module.params['exclude_range']
	action = module.params['action']
	cluster_name = module.params['cluster_name']
	count = module.params['count']
	ips = module.params['ips']
	path = module.params['path']

	if _module_not_found:
		module.fail_json(msg='the python netaddr module is required')
	try:
		if action == 'create_pool':
			if not ip_net or not ip_range:
				module.fail_json(msg="Missing required fields 'ip_net' or 'ip_range'")
			create_ip_pool(ip_net, ip_range, exclude_range, path)
		if action == 'verify_ips':
			verify_ips_from_pool(count, path)
		if action == 'reserve_ips':
			usable_ips = fetch_ips_from_pool(cluster_name, count, path)
			module.exit_json(usable_ips=usable_ips)
		if action == 'release_ips':
			release_ips_pool(ips, path)
		if action == 'view_pool':
			pool = display_ip_pool(path)
			module.exit_json(pool=pool)
	except Exception as exp:
		module.fail_json(msg="{}".format(exp))
	module.exit_json(msg="Operation successful!")

if __name__ == '__main__':
	 main()

