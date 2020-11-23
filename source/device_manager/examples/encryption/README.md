In order to generate a key and certificate the following can be run:  
`openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out sila_server.cert -keyout sila_server.key`  
For the field `Common Name (e.g. server FQDN or YOUR name) []:` add `*.sila.com`.  
The other fields can be left blank.

On the server machine:
- in the `/etc/hostname` file replace the existing content with `{some_name}.sila.com` (this will be the server hostname); it is preferred that the hostname is not the same as the hostnames of other server machines
- specify the key and certificate when starting the server

On the client machine:
- in the `/etc/hosts` file add the following line: `{server_ip} {server_hostname}` (this will be automated in the future)
- copy the certificate in the folder from which you will be executing your code and rename the certificate file to `sila_server.crt`
- the dynamic client can be run in the following way:
`client = DynamicSiLA2Client(name="client", server_ip=None, server_hostname="{server_hostname}", server_port = {server_port})`
- `server_ip` must be set to `None` or to `''` (empty string)
