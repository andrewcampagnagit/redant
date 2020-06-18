"""

Gather module is used for grabbing / generating info on the installation node.

Version: 2.2.0
Author: Andrew Campagna

* THIS IS A NON-PRODUCTION VERSION *

"""

from bs4 import BeautifulSoup
from os import path
from os.path import expanduser
import requests
import yaml
import os
import re


#	Collects data from install-config.yaml
def collect(static_ip):
	with open("install-config.yaml", "r") as install_cfg_file:
	        install_config = yaml.safe_load(install_cfg_file)
	        install_cfg_file.close()

	project_name = install_config["metadata"]["name"]
	bootstrap_url = "http://"+ static_ip +"/"+ project_name +"/bootstrap.ign"

	return project_name, static_ip, bootstrap_url


#	Creates list of available OCP versions for install
def available_versions():
	response = requests.get("https://mirror.openshift.com/pub/openshift-v4/clients/ocp/")
	soup = BeautifulSoup(response.content, "html.parser")
	links = soup.findAll("a")

	available = []

	for link in links:
		if re.match("^[0-9]*.[0-9]*.[0-9]*\/$", link.text):
			available.append(link.text.replace("/", ""))

	return available


#	Creates SSH Key
def make_ssh_key():
	print(os.popen("echo '\n' | ssh-keygen -t rsa -b 4096 -N ''").read())
	print(os.popen("eval \"$(ssh-agent -s )\" \\ ssh-add ~/.ssh/id_rsa").read())


# Grab and return SSH Key
def grab_ssh_key():
	if not path.exists(expanduser("~") + "/.ssh/id_rsa.pub"):
		print("No file ~/.ssh/id_rsa.pub found...attempting to create one...")
		make_ssh_key()
	return os.popen("cat ~/.ssh/id_rsa.pub").read()
