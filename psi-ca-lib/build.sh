#!/bin/bash

bazel build //cpp/...
bazel build -c opt //python:psi_ca

##write script that copies the files from bazel-bin/ to the fpsica folder
cp bazel-bin/python/_psi_ca.so fpsica/fpsica/_psi_ca.so
cp bazel-bin/python/psi_ca_python_proto_pb/proto/psi_pb2.py fpsica/fpsica/psi_pb2.py
