# Cloud Picture Album API

This is a backend API that allows users to create albums, upload pictures and manage them in the cloud. 

This is currently **backend-only**. Authentication and frontend templating will be added soon.

The project was insipired by my experience at [Northcoders](https://www.northcoders.com/), where I broadend and cemented my understanding of RESTful APIs and cloud infrastrastructure.

## Table of Contents
- Features

- Technologies

- Installation

- Usage

- Database Structure

- Future Enhancements/Project Status

- Acknowledgements

- License

## Features
- Create and update picture albums.
- Upload pictures to specific albums or the user's default album.
- Cloud-based storage and infrastructure via Terraform and AWS.
- Deployment using AWS EC2.
- Testing using pytest.

## Technologies
- **Backend**: Python, FastAPI

- **Frontend**: (To be implemented)

- **Database**: PostgreSQL

- **Cloud Provider**: AWS

- **CI/CD**: Github Actions

- **Version Control**: Git/GitHub

## Installation
1. Clone the repository:

```
git clone https://github.com/AbbyAdj/cloud-picture-album-api.git
cd cloud-picture-album-api
```

2. Install the necessary dependencies:

```
pip install -r requirements.txt
```

3. Setup your AWS CLI (for deployment and Terraform):
   
**If this step is already done, move on to step 4**

```
pip install awscli 

aws configure # configure with your aws credentials 
```

4. Configure Environment Secrets and Terraform Variables:
   
The following are to be provided in a .env file.
```
DB_USER
DB_HOST
DB_DATABASE
DB_PASSWORD
S3_USER_STORAGE_BUCKET
```
Terraform variables can be found in their various modules. Some are set to defaults so you can change them accordingly or set them in the root main.tf.

5. Deploy cloud infrastructure with Terraform:

**A makefile will soon be provided to provide a more seamless experience**
```
cd terrafor
terraform init
terrafrom plan # This is optional for your use
terraform apply
```
6. SSH into the EC2 (Optional):
   
If you would prefer to SSH into the instance for your own use
```
ssh -i /path/to/your-key.pem ec2-user@<instance_ip>
```
Alternatively, you can access the ssh path in the AWS EC2 instance console,

7. Access the API:
   
Once the EC2 is up and running, you can get the public IP on
```
terraform output instance_ip 
```
 You can then access the API on a browser or on Postman:
```
http://<instance_ip>:8000
```


## Usage

Once the API is up and running, you can interact with the endpoints.

**Full docs on the endpoints will be provided soon**

## Database Structure

**Fields to be updated here soon**


## Future Enhancements/Project Status

- **Authentication**: JWT-based authentication or similar to be incorporated.
- **Frontend Templating**: By use of Jinja, Flask or Django for a better UI/UX.
- **Public/Private Album Support**
- **Full API Documentation**
- **Docker Support for local deployment**

## Acknowledgements

A very big THANK YOU and shoutout to [Northcoders](https://www.northcoders.com/) for lighting the spark to this project idea. What started as me simply trying to challenge myself turned into an impressive real world cloud-first project.

## License

This project is licensed under the MIT License.
