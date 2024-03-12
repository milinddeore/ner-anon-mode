# DeID 
This model facilitates both data anonymization and the incorporation of synthetic data, all based on the provided prompt details in the scripts. This application is delivered as part of a Docker container compatible with both CPU and GPU environments.

![anon_mode](https://github.com/talkWiise/deid/blob/main/anon_mode.gif)

# Model Used
The inference [model](https://huggingface.co/TheBloke/airoboros-l2-7b-gpt4-1.4.1-GGML/resolve/main/airoboros-l2-7b-gpt4-1.4.1.ggmlv3.q4_0.bin) employed is Airoboros, sourced from Hugging Face. You can find specific details about the model [here](https://huggingface.co/TheBloke/airoboros-l2-7b-gpt4-1.4.1-GGML). It's important to note that this is a GGML model, which necessitates conversion to GGUF before it can be utilized. Use [script](https://github.com/ggerganov/llama.cpp/blob/master/convert-llama-ggml-to-gguf.py) to convert from GGML to GGUF.

# MLops
All current deployments are conducted using Docker containers, so it is essential to update the `Dockerfile` with the most recent code and requirements. After completing the `Dockerfile` update, proceed with the steps to build the image and push it to Docker Hub:

```
# Step: 1
ubuntu@ip-172-31-24-214:~/nonymus-ner/deid$ docker build . -t nonymushub/deid:v0.2

# Step: 2
ubuntu@ip-172-31-24-214:~/nonymus-ner/deid$ docker images
REPOSITORY        TAG       IMAGE ID       CREATED        SIZE
nonymushub/deid   v0.2      ed0d89b27525   43 hours ago   13.9GB

# Step: 3
ubuntu@ip-172-31-24-214:~/nonymus-ner/deid$ docker push nonymushub/deid:v<version_number>
```

# Running the container
Pull the images from docker-hub with the respective tag, if the image is not locally available.  

```
# Step: 1 (optional)
$ docker pull nonymushub/deid:v0.2
```

If you have the Nvidia GPU on the machine, you should see following command. This is on the host machine, where you want to run the docker container:

```
# Step: 2 (on Host machine)
ubuntu@ip-172-31-24-214:~/nonymus-ner/deid$ nvidia-smi
Sat Sep  9 11:29:11 2023
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.54.03              Driver Version: 535.54.03    CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       On  | 00000000:00:1E.0 Off |                    0 |
| N/A   33C    P8               9W /  70W |      0MiB / 15360MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
```

If you see the above, you can accelerate the model speed.
```
# Step: 3 (for GPU)
docker run --gpus <GPU_ID, usually 0> --rm -p 8080:8080 -it nonymushub/deid:<version>
```

Docker should be up and running on the host. to validate run following command: 
```
# Step: 4
ubuntu@ip-172-31-24-214:~/nonymus-ner/deid$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                       NAMES
370898e09ffb   nonymushub/deid:v0.2   "/opt/nvidia/nvidia_…"   36 seconds ago   Up 34 seconds   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   gracious_antonelli
```

Now, container is hosted and ready to take the request.

## Container exposed to the external world
In case the container is exposed to the internal application or client, it has to have HTTPS access. This means you can install the SSL certificate and point the root location to the container. If you can use Lets Encrypt, it update `/etc/nginx/sites-available/default` and attach the domain (ex: abc.com) hence no need to create a seperate configuration file under the same path else you will see error `conflicting server name "abc.com" on 0.0.0.0:80, ignored`

Update the server setting as following in the file `/etc/nginx/sites-available/default`: 
```
        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;
        server_name talksecretai.com; # managed by Certbot


        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                #try_files $uri $uri/ =404;
                proxy_pass http://127.0.0.1:8080;            <<<<<<<<<<<<<<<<<< This is where the container is running on port 8080
        }
```
