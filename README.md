# Overview

The purpose of this playground is to have a simple server in GCP serving [Ganache](https://github.com/trufflesuite/ganache) that vulnerable smart contracts can be deployed to. Then a user can run the corresponding attack contract to understand the vulnerability. 


# Prerequisites

* A GCP project
* Terraform and Python 3.8 installed locally
* Git clone repo
* Create key pair
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

## Create key pair
```
cd ganache-playground/keys
ssh-keygen -t rsa -f playground-key -C <username>
```

## Update variables.tf

Open variables.tf in root folder with IDE/text editor and modify the following:
* Update "project" to your GCP Project
* Update "source-ip" to your IPv4 (https://whatismyipaddress.com/)
* Update "user" to your username used in key creation step
* Update "public_key_path" to name of public key
* Update "private_key_path" to name of private key

## Create a bucket to store state, modify backend.tf (Optional)

You'll can use a bucket to store the state of your terraform configuration or you can store it locally. If you want to store it in a bucket, you'll need to log into your GCP Project and create a bucket. Then you'll need to modify the backend.tf with the bucket name. If not, delete the backend.tf file. 

# Getting started

You'll need to initialize terraform first. Next, you'll do a plan to see what resources are going to be created. If everything is configured right, when you do a terraform apply, you should be successful
```
terraform init
terraform plan
terraform apply
```

## Deploying contracts

The smart contracts and code are all prewritten, you'll just need to run the python scripts to perform the attacks.

## Supported Smart Contract Vulnerabilities at the moment:
* Reentrancy
* Self Destruct