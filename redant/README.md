# Easy install

Features:
- Auto detecting SSH Keygen
- Single yaml file installation (install-config.yaml)
- OCP Version selector that is linked directly to RedHat
- HaProxy configuration API
- Multi-cluster deployment support

0. Run the set-up installer

	Clone the repo and execute the following shell script **setup.sh**
	
	```bash
	bash setup.sh
	```
	
1. Start the flask app

	```bash
	export FLASK_APP=redant.py
	```
	
	```bash
	flask run -h 0.0.0.0 -p 8080
	```

#### Build Install Node

1. Create your install-config.yaml file
	
	```yaml
	apiVersion: v1
	baseDomain: [ocp.csplab.local]
	compute:
	- hyperthreading: Enabled   
	  name: worker
	  replicas: 0
	controlPlane:
	  hyperthreading: Enabled   
	  name: master
	  replicas: 3
	metadata:
	  name: [vhavard]
	platform:
	  vsphere:
	    vcenter: [demo-vcenter.csplab.local]
	    username: [username]
	    password: [password]
	    datacenter: [CSPLAB]
	    defaultDatastore: [SANDBOX-OCS]
	pullSecret: '[contents of pull-secret.txt]'
	sshKey: '[contents of ~/.ssh/id_rsa.pub]'
	```
	
	To get your SSH key visit the web UI at http://installer-ip-address:8080/ and click on **SSH Keygen**
	
	Pull-Secret: https://cloud.redhat.com/openshift/install/vsphere/user-provisioned 
	
	
2. Provide your install-config.yaml and select your OCP version --- Then click build and you're done!

#### Configure HaProxy Configuration

1. Click on **Load Balancers** and provide the ipv4 addresses for your workers, masters, storage, install, and bootstrap nodes. The message ***Built!*** will appear when the task is complete.

2. SSH into your loadbalancers and use simply wget the pre-configured haproxy.cfg files from the RedAnt API.

master load balancer
```bash
wget http://installer-ip-address:8080/masterlb
```

compute load balancer
```bash
wget http://installer-ip-address:8080/computelb
```

### Remember to rename these files to haproxy.cfg
