

load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_cc//cc:defs.bzl", "cc_proto_library")
load("@rules_proto_grpc//python:defs.bzl", "python_proto_library")



package(default_visibility = ["//visibility:public"])

proto_library(
    name = "psi_proto",
    srcs = ["psi.proto"],
)

cc_proto_library(
    name = "psi_cc_proto",
    deps = [":psi_proto"],
)

python_proto_library(
    name = "psi_python_proto",
    protos = [":psi_proto"],
)

