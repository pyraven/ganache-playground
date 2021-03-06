# Overview

The purpose of this playground is to have a simple server in GCP serving [Ganache](https://github.com/trufflesuite/ganache) that vulnerable smart contracts can be deployed to. Then a user can run the corresponding attack contract to understand the vulnerability. 

Inspired by these channels:
* [Block Explorer](https://www.youtube.com/c/BlockExplorerMedia)
* [Dapp University](https://www.youtube.com/c/DappUniversity)
* [MammothInteractive](https://www.youtube.com/c/MammothInteractive)
* [Smart Contract Programmer](https://www.youtube.com/channel/UCJWh7F3AFyQ_x01VKzr9eyA)

# Prerequisites

* A GCP project
* Terraform, Python 3.8, netcat installed locally
* Git clone repo
* Update variables/backend
* Deploy


## Create project or login to existing project
```
https://console.cloud.google.com/
```

## Install Terraform on Mac
```
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

## Install Terraform on Windows
```
choco install terraform
```

## Clone repo locally
```
git clone https://github.com/pyraven/ganache-playground
```

## Update variables.tf

Open variables.tf in root folder with IDE/text editor and modify the following:
* Update "project" to your GCP Project
* Update "source-ip" to your [IPv4](https://whatismyipaddress.com/)

## Create a bucket to store state, modify backend.tf (Optional)

You'll can use a bucket to store the state of your terraform configuration or you can store it locally. If you want to store it in a bucket, you'll need to log into your GCP Project and create a bucket. Then you'll need to modify the backend.tf with the bucket name. If not, delete the backend.tf file. 

# Getting started

You'll need to initialize terraform first. Next, you'll do a plan to see what resources are going to be created. If everything is configured right, when you do a terraform apply, you should be successful
```
terraform init
terraform plan
terraform apply
```

To verify you can reach Ganache, run the output value when the Terraform apply is complete:
```
nc <gcp_instance_public_ip> 9000
```

To get the current block number:
```
python3 status.py --host <gcp_instance_public_ip>:9000
```

### Accessing the instance for troubleshooting
While recently authenticated, OS Login is enabled on the instance so running this command will allow you to SSH into the host if needed:
```
gcloud compute ssh --zone <zone> <instance_name>  --project <project_id>
```

## Deploying contracts

The smart contracts and code are all prewritten, you'll just need to run the python scripts to deploy the contracts and perform the attacks. The workflow is:

```
# deploy contracts, this will create two JSON files for the other scripts to use (for ABI/deployed contract addresses)

python3.8 deploy.py --host <gcp_instance_public_ip>:9000

# if available, some won't have this script, skip if not

python3.8 play.py --host <gcp_instance_public_ip>:9000 

# attack deployed contracts

python3.8 attack.py --host <gcp_instance_public_ip>:9000
```

## Supported Smart Contract Vulnerabilities at the moment, more to come:
* Reentrancy
* Self Destruct
* Private Variables