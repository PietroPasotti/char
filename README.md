
`newgrp docker`

To build:
`docker build --tag localhost:32000/char . `

To send to microk8s:
`docker push localhost:32000/char`

Run an ork:
`docker run --env ENEMIES=127.0.0.1:8001 --env NAME=ork -p 8000:8080 --expose 8000 --rm -d char`

Run an elf:
`docker run --env ENEMIES=127.0.0.1:8000 --env NAME=elf -p 8001:8080 --expose 8001 --rm -d char`

Then open the docs at `127.0.0.1:8001/docs` and `/attack` the ork for 0 damage; watch the battle unfold.

Docker cleanup:
`docker stop $(docker ps -a -q); docker rm $(docker ps -a -q)`

`docker images` 
`docker rmi [ID of the old image]`

Juju deploy:
if you have a char image called, say, char:latest in docker, do:
`docker save char:latest | microk8s ctr image import -`

now you can reference that image in microk8s; let's map it to char-image (or whatever you labelled your 
image in metadata.yaml)
`juju deploy --debug ./char-operator_ubuntu-20.04-amd64.charm --resource char-image=char:latest`                                     
sa