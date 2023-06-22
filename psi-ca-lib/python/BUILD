load("@pybind11_bazel//:build_defs.bzl", "pybind_extension")
load("@rules_python//python:packaging.bzl", "py_package", "py_wheel")
load("@rules_proto_grpc//python:defs.bzl", "python_proto_library")
load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

pybind_extension(
    name = "_psi_ca",
    srcs = ["bindings.cpp"],
    linkstatic = True,
    visibility = ["//visibility:private"],
    deps = [
        "//cpp:psi_node",
        "//proto:psi_cc_proto",
        "@com_google_absl//absl/status:statusor",
    ],
)

python_proto_library(
    name = "psi_ca_python_proto",
    protos = ["//proto:psi_proto"],
)



py_library(
    name = "psi_ca",
    srcs = ["psi_ca.py"],
    data = [
        ":_psi_ca.so",
    ],
    deps = [
        "psi_ca_python_proto"
    ],
)


py_library(
    name = "init",
    srcs = [
        "__init__.py",
        "version.py",
        ":psi_ca",
        "psi_ca_python_proto",
    ])





py_test(
    name = "tests",
    srcs = ["tests.py"],
    legacy_create_init = False,
    main = "tests.py",
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":psi_ca",
        requirement("pytest")
        ],
)

py_binary(
    name = "benchmarks",
    srcs = ["benchmarks.py"],
    legacy_create_init = False,
    main = "benchmarks.py",
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        ":psi_ca",
        requirement("pytest"),
        requirement("pytest-benchmark")
    ],
)

py_package(
    name = "fpsica_package",
    visibility = ["//visibility:private"],
    deps = [
        ":psi_ca",
    ],
)

py_wheel(
    name = "fpsica_wheel",
    python_requires = ">=3.8.0",
    abi = "ABI",
    requires = ["protobuf>=3.20"],
    deps = [":fpsica_package"],
    distribution = "fpsica",
    version = "0.0.1"
)


