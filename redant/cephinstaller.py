"""

Installs Ceph cluster on OpenShift

"""

import git
import os
import time

#	Label storage nodes
def label_storage_nodes(storage_node_names):

	for node in storage_node_names:
		os.popen("oc label node "+ node +" role=storage-node")



#	Gets status of deployment
def get_deployment_status(deployment_name):
	deployments = os.popen("oc get deployment -n rook-ceph").read().split("\n")[1:-1]
	for deployment in deployments:
		if deployment_name in deployment:
			ready_status = deployment.split()[1]
			if ready_status.split("/")[0] == ready_status.split("/")[1]:
				return True

	return False


#	Download and deploy rook-ceph operator
def deploy_ceph_operator(cluster_file_path):

	os.chdir("/opt")
	repo = git.Repo.clone_from("https://github.com/rook/rook.git", "rook")
	repo.git.checkout("3d5776f")
	os.chdir("cd /opt/rook/cluster/examples/kubernetes/ceph")
	print(os.popen("oc create -f common.yaml"))
	print(os.popen("oc create -f operator-openshift.yaml"))
	print("Deploying rook-ceph-operator...", end="")

	while(not get_deployment_status("rook-ceph-operator")):
		print(".", end="")
		time.sleep(5)

	print(os.popen("oc create -f " + cluster_file_path).read())
	print("Ceph cluster deployed!")