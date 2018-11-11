docker run -it -v $HOME/.WebControl:/root/.WebControl -v /var/run/docker.sock:/var/run/docker.sock -p 5001:5001 -e HOST_HOME=$HOME --network="host" --privileged madgrizzle/webmcp
