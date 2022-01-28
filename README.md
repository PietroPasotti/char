

Run an ork:
`docker run --env ENEMIES=127.0.0.1:8001 --env UVICORN_PORT=8000 --env NAME=ork -p 8000:8000 --expose 8000 --rm -d char`

Run an elf:
`docker run --env ENEMIES=127.0.0.1:8000 --env UVICORN_PORT=8001 --env NAME=elf -p 8001:8001 --expose 8001 --rm -d char`

Then open the docs at 127.0.0.1:8001 and /attack the ork for 0 damage; watch the battle unfold.

Docker cleanup:
`docker stop $(docker ps -a -q); docker rm $(docker ps -a -q)`
