# WebMCP

### Docker

You can build a Docker image with

    docker build -t madgrizzle/webmcp .

Then you can run it directly

    docker run -it -v $HOME/.WebControl:/root/.WebControl -v /var/run/docker.sock:/var/run/docker.sock -p 5001:5001 -e HOST_HOME=$HOME --privileged madgrizzle/webmcp

Or push it up to Docker Hub

    docker push madgrizzle/webmcp

Then the WebMCP interface will be available at http://localhost:5001
