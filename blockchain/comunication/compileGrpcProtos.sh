# generate Protos python files using all files in protos directory
# NOTE: After generation is possible that you must modify an import in [*]_pb2_grpc.py
python -m grpc_tools.protoc -I./protos --python_out=./grpc_protos --grpc_python_out=./grpc_protos ./protos/*.proto