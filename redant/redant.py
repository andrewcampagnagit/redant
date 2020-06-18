"""

Project RedAnt is an IPI installer for OpenShift Cloud Platform 4.2 by Red Hat.

Version: 2.2.0
Author: Andrew Campagna

* THIS IS A NON-PRODUCTION VERSION *

"""

from flask import Flask, render_template, request, send_file
import gather
import lbbuilder
import os


app = Flask(__name__)


#	Installation node builder
@app.route('/')
def index():
    return render_template('index.html', versions=gather.available_versions())


@app.route('/', methods=['POST'])
def installer_form_post():
	install_config = request.form["installconfig"]
	ocpversion = request.form["ocpversion"]
	with open("install-config.yaml", "w+") as install_config_file:
		install_config_file.writelines(install_config)

	project_name, static_ip, bootstrap_url = gather.collect(request.base_url.split("/")[2].split(":")[0])
	os.popen("sudo python3 installnode.py " + project_name + " " + bootstrap_url + " " + ocpversion)
	return render_template("installing.html", project_name=project_name, static_ip=static_ip, bootstrap_url=bootstrap_url, ocp_version=ocpversion)


#	Grabs SSH Key and builds one if none are available
@app.route('/sshkey')
def grab_ssh_key():
	return gather.grab_ssh_key()


#	haproxy.cfg Builder
@app.route('/buildhaproxy')
def build_haproxy():
	return render_template("loadbalancer.html")


#	Master boad balancer configuration file
@app.route('/masterlb')
def masterlb_file():
	return send_file("templates/master_haproxy.cfg")


#	Master boad balancer configuration file
@app.route('/computelb')
def computelb_file():
	return send_file("templates/compute_haproxy.cfg")


#	Builds master haproxy.cfg
@app.route('/buildhaproxy', methods=['POST'])
def build_lb():
	masterFrom = request.form["fromMasterRange"].split(".")[-1]
	masterTo = request.form["toMasterRange"].split(".")[-1]
	print(masterFrom)
	print(masterTo)
	workerFrom = request.form["fromWorkerRange"].split(".")[-1]
	workerTo = request.form["toWorkerRange"].split(".")[-1]
	print(workerFrom)
	print(workerTo)
	storageFrom = request.form["fromStorageRange"].split(".")[-1]
	storageTo = request.form["toStorageRange"].split(".")[-1]
	print(storageFrom)
	print(storageTo)
	bootstrap = request.form["bootstrapIP"].split(".")[-1]
	installer = request.form["installerIP"].split(".")[-1]
	print(bootstrap)
	print(installer)
	head = ".".join((request.form["installerIP"]).split(".")[:-1])
	print(head)
	lbbuilder.build_config_master(head, masterFrom, masterTo, workerFrom, workerTo, bootstrap, installer)
	lbbuilder.build_config_compute(head, storageFrom, storageTo, workerFrom, workerTo, installer)
	return render_template("loadbalancer.html")
