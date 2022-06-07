# api
This microservice will have a public IP and will attend user-query requests with a lat and long parameters.

# Instructions
* This template is created as a template. Selected this template when creating a new repository.
* Edit the .env file and adjust variables accordingly
* Use make <COMMAND> to work with this repository:

```
make build
```
It builds the image in the local docker repository.
```
make run
```
It runs the application in the container. It's configured for hot reloading. Everytime you make a change in the code the app will refresh.
```
make logs
```
Outputs in the terminal the output of the application
```
make stop
```
Stop the application
```
make bash
```
Enter the command line of the image for debugging. Shouldn't need to do this very often
```
make auth
```
Authenticates gcloud and docker
```
make deploy
```
Deploys the application in the appropriate GCP Artifact repository. By defualt the repository should be named as the image created locally. IF it's not Make file should be modified.
