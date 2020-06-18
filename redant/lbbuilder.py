"""

Build Load Balancer haproxy.cfg

"""

import os


with open("resources/master_template.cfg", "r") as master_template_file:
	master_template = "".join(master_template_file.readlines())
	master_template_file.close()


with open("resources/compute_template.cfg", "r") as master_template_file:
	compute_template = "".join(master_template_file.readlines())
	master_template_file.close()


def build_config_master(head, masterFrom, masterTo, workerFrom, workerTo, bootstrap, installer):

	global master_template
	
	# Bootstrap and Masters - Port 6443
	block = ""
	for idx, endbyte in enumerate(range(int(masterFrom), int(masterTo) + 1)):
		block += "	server master-" + str(idx) + " " + head + "." + str(endbyte) + ":6443 check\n"
	block += "	server bootstrap " + head + "." + bootstrap + ":6443 check"
	master_template = master_template.replace("@BOOTSTRAP_MASTER:6443", block)


	# Bootstrap and Masters - Port 22623
	block = ""
	for idx, endbyte in enumerate(range(int(masterFrom), int(masterTo) + 1)):
		block += "	server master-" + str(idx) + " " + head + "." + str(endbyte) + ":22623 check\n"
	block += "	server bootstrap " + head + "." + bootstrap + ":22623 check"
	master_template = master_template.replace("@BOOTSTRAP_MASTER:22623", block)


	# Installer and Compute - Port 80
	block = ""
	for idx, endbyte in enumerate(range(int(workerFrom), int(workerTo) + 1)):
		block += "	server	compute-" + str(idx) + " " + head + "." + str(endbyte) + ":80 check\n"
	block += "	server	installer " + head + "." + installer + ":80 check"
	master_template = master_template.replace("@BINSTALLER_COMPUTE:80", block)


	# Installer and Compute - Port 443
	block = ""
	for idx, endbyte in enumerate(range(int(workerFrom), int(workerTo) + 1)):
		block += "	server compute-" + str(idx) + " " + head + "." + str(endbyte) + ":443 check\n"
	block += "	server installer " + head + "." + installer + ":443 check"
	master_template = master_template.replace("@BINSTALLER_COMPUTE:443", block)


	with open("templates/master_haproxy.cfg", "w+") as haproxy_file:
		haproxy_file.write(master_template)
		haproxy_file.close()

	print("Built master haproxy.cfg")


def build_config_compute(head, storageFrom, storageTo, workerFrom, workerTo, installer):

	global compute_template
	
	# Installer, computes, and storage - Port 80
	block = ""
	for idx, endbyte in enumerate(range(int(workerFrom), int(workerTo) + 1)):
		block += "	server  compute-" + str(idx) + " " + head + "." + str(endbyte) + ":80 check\n"
	for idx, endbyte in enumerate(range(int(storageFrom), int(storageTo) + 1)):
		block += "	server  storage-" + str(idx) + " " + head + "." + str(endbyte) + ":80 check\n"
	block += "	server  installer " + head + "." + installer + ":80 check"
	compute_template = compute_template.replace("@INSTALLER_COMPUTE_STORAGE:80", block)


	# Installer, computes, and storage - Port 443
	block = ""
	for idx, endbyte in enumerate(range(int(workerFrom), int(workerTo) + 1)):
		block += "	server  compute-" + str(idx) + " " + head + "." + str(endbyte) + ":443 check\n"
	for idx, endbyte in enumerate(range(int(storageFrom), int(storageTo) + 1)):
		block += "	server  storage-" + str(idx) + " " + head + "." + str(endbyte) + ":443 check\n"
	block += "	server  installer " + head + installer + ":443 check"
	compute_template = compute_template.replace("@INSTALLER_COMPUTE_STORAGE:443", block)


	with open("templates/compute_haproxy.cfg", "w+") as haproxy_file:
		haproxy_file.write(compute_template)
		haproxy_file.close()

	print("Built compute haproxy.cfg")

