"""

Install Node Script

"""

import os
import yaml
import json
import time
import sys

project_name = sys.argv[1]
bootstrap_url = sys.argv[2]
ocpversion = sys.argv[3]

print("Starting installation for project "+ project_name)


## Configure System  & Download OpenShift ##
os.popen("mkdir /opt/"+ project_name)
os.popen("sudo wget -P /opt https://mirror.openshift.com/pub/openshift-v4/clients/ocp/"+ ocpversion +"/openshift-client-linux-"+ ocpversion +".tar.gz").read()
os.popen("sudo wget -P /opt https://mirror.openshift.com/pub/openshift-v4/clients/ocp/"+ ocpversion +"/openshift-install-linux-"+ ocpversion +".tar.gz").read()
os.popen("tar -xvzf /opt/openshift-client-linux-"+ ocpversion +".tar.gz -C /opt").read()
os.popen("tar -xvzf /opt/openshift-install-linux-"+ ocpversion +".tar.gz -C /opt").read()
os.popen("sudo cp /opt/oc /usr/local/bin")
os.popen("sudo cp /opt/kubectl /usr/local/bin")
os.popen("sudo mv install-config.yaml /opt/"+ project_name)
os.chdir("/opt")


## Create Manifests / Edit cluster-scheduler-02-config.yml ##
os.popen("sudo ./openshift-install create manifests --dir=./"+ project_name).read()
with open("/opt/"+ project_name +"/manifests/cluster-scheduler-02-config.yml", "r") as cluster_scheduler_file:
	cluster_config_02 = yaml.safe_load(cluster_scheduler_file)
	cluster_config_02["spec"]["mastersSchedulable"] = False

with open("/opt/"+ project_name +"/manifests/cluster-scheduler-02-config.yml", "w+") as cluster_scheduler_file:
	yaml.dump(cluster_config_02, cluster_scheduler_file, default_flow_style=False)
os.popen("cat /opt/"+ project_name +"/manifests/cluster-scheduler-02-config.yml")
os.chdir("/opt")


## Create ignition files ##
os.popen("sudo ./openshift-install create ignition-configs --dir=./"+ project_name).read()
append_bootstrap = {"ignition":{"config":{"append":[{"source":bootstrap_url,"verification":{}}]},"timeouts":{},"version":"2.1.0"},"networkd":{},"passwd":{},"storage":{},"systemd":{}}


## Create append-bootstrap.ign ##
with open("/opt/"+ project_name +"/append-bootstrap.ign", "w+") as append_bootstrap_file:
	json.dump(append_bootstrap, append_bootstrap_file, indent=4)
	append_bootstrap_file.close()


## Encode ignition files in base64 ##
os.chdir("/opt/" + project_name)
os.popen("base64 -w0 append-bootstrap.ign > append-bootstrap.base64")
os.popen("base64 -w0 master.ign > master.base64")
os.popen("base64 -w0 worker.ign > worker.base64")


## Finish ##
print(os.popen("sudo ln -s /opt/"+ project_name + " /var/www/html/"+ project_name).read())
print("Installation node is complete!")

