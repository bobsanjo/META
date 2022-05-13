---
permalink: /docs/internals/linux_development_in_docker/
title: "Linux Development in Docker"
toc: true
---

If you do not have a linux machine, you can simply use docker on your usual os (Windows or Mac) to do linux development. You need to [install docker](https://docs.docker.com/get-docker/). On windows, you might first need to install [windows subsystem for linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

## Basic tools

### Running an image

Once docker is installed and running you can run a docker image. For example, to run the standard ubuntu image, run
```terminal
docker run -it ubuntu:latest
```
You will then enter the realm of your docker image. Your terminal will change to something like this
```terminal
root@2220972d3a34:/#
```

### Container id

Docker will give this container an id. To see the id (which you will find handy), run
```terminal
docker ps
```
and you should see the running container, and its id.

### Enter container from another terminal 

You can enter the same container from another terminal too. Simply run
```terminal
docker exec -it <container id> /bin/bash 
```

### File copying

You can also copy files into your docker image, or out of it. The syntaxes are
```terminal
docker container cp [OPTIONS] <container id>:<file on docker image> <path on native os>

docker cp [OPTIONS] <path on native os>  <container id>:<file on docker image>
```
for copying files out of and into the image, respectively.

## Create your own custom image

You can create a custom image for your personal use (even with your ssh keys, etc), but make sure not to share it with others. Simply enter a standard image, then do any provisioning you desire (copy ssh keys, modify `~/.bashrc`, install packages and compilers). Then, you can save this image with the command
```terminal
docker commit <container id> <container name>:<version>
```
For example,
```terminal
docker commit 7e0aa2d69a15 hoshyari/ubuntu:version1
```
You can later use the docker run command to run this saved image
```terminal
docker run -it hoshyari/ubuntu:version1
```

You can further commit more changes to the container. Remember, if a container stops running and you don't save things, you lose them.

## Develop in the container

The container is a virtual machine. You can compile and debug code in it. It does not have any GUI, but you can use vscode to view and edit files within the container! See [here]({{ site.baseurl }}{% link _docs/internals/vscode_tips.md %}#Connecting-to-a-running-docker-image).

## Host the MetaBuild documentation page in docker

In windows, we need docker to serve the MetaBuild docs page. If you use the easy way described [here]({{ site.baseurl }}{% link _docs/internals/docs.md %}#Use-Jekyll-within-Docker), it can take a long time for the site to rebuild itself. Alternatively, you can serve the site in docker, and just expose the port to your native os to view the site with a web browser.

Run the docker image, but expose the port 4000 by adding the -p parameter.
```terminal
docker run -p 4000:4000 -it <container name>:<version>
```
Make sure to have Jekyll setup within the container. It should be easy to install Jekyll on linux. Then serve the website with 
```terminal
bundle exec jekyll serve --host 0.0.0.0 # within docker
```
Now from your browser in native os, open `http://localhost:4000` and you should see the website.
