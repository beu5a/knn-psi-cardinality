
package(default_visibility = ["//visibility:public"])

PSI_LINKOPTS = select({
    "@platforms//os:osx": [],
    "//conditions:default": [
        # Needed on some Linux systems. See also
        # https://github.com/google/cctz/issues/47
        # https://github.com/tensorflow/tensorflow/issues/15129
        "-lrt",
    ],
})



 

cc_library(
    name = "psi_node",
    srcs = ["psi_node.cpp"],
    hdrs = [
        "psi_node.h",
    ],
    includes = ["."],
    deps = [
        "//cpp/util:crypto",
        "//cpp/util:set_operations",
        "//proto:psi_cc_proto",
        "@boringssl//:crypto",
        "@com_google_absl//absl/memory",
        "@com_google_absl//absl/status:statusor",
        "@com_google_absl//absl/strings",
        "@com_google_absl//absl/types:span",
        "@private_join_and_compute//private_join_and_compute/crypto:ec_commutative_cipher",
    ],
)

cc_test(
    name = "psi_test",
    srcs = ["psi_test.cpp"],
    deps = [
        ":psi_node",
        "@com_google_googletest//:gtest",
        "@com_google_googletest//:gtest_main",
        "@com_google_absl//absl/memory",
        "@com_google_absl//absl/status:statusor",
        "@com_google_absl//absl/strings",
        "@com_google_absl//absl/types:span",
    ],
)
cc_binary(
    name = "psi_benchmark",
    srcs = ["psi_benchmark.cpp"],
    linkopts = PSI_LINKOPTS,
    deps = [
        ":psi_node",
        "@com_google_absl//absl/strings",
        "@com_google_benchmark//:benchmark_main",
    ],
)



