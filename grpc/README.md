# python-grpc

### install
```
$ docker-compose build
$ docker-compose up -d
```

#### generate grpc code
```
$ python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/greet.proto
```

#### run server and client
```
$ python greet_server.py
$ python greet_client.py
```
