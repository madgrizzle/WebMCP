# WebMCP

### Docker

You can build a Docker image with

    docker build -t madgrizzle/webmcp .

Then you can run it directly

    docker run -it -v $HOME/.WebControl:/root/.WebControl -v /var/run/docker.sock:/var/run/docker.sock -p 5001:5001 -e HOST_HOME=$HOME --privileged madgrizzle/webmcp

Or run it in the background

	docker run -d --rm -v $HOME/.WebControl:/root/.WebControl -v /var/run/docker.sock:/var/run/docker.sock -p 5001:5001 -e HOST_HOME=$HOME --privileged madgrizzle/webmcp

Or push it up to Docker Hub

    docker push madgrizzle/webmcp

Then the WebMCP interface will be available at http://localhost:5001

### systemd

You can easily configure the docker image to get run at startup with systemd. Just copy the `web-mcp.service.example` file to `/etc/systemd/system`.

    cp webmcp.service.example /etc/systemd/system/

Then you can tell systemd to start WebMCP

    sudo systemctl start webmcp

Then you can tell systemd to always start WebMCP at system boot.

    sudo systemctl enable webmcp
