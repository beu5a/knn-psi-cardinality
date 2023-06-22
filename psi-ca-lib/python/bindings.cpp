#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <memory>
#include <vector>

#include "absl/status/statusor.h"
#include "cpp/psi_node.h"
#include "proto/psi.pb.h"

namespace {
namespace psi = private_set_intersection;
namespace py = pybind11;
}  // namespace

template <class T>
T throwOrReturn(const absl::StatusOr<T>& in) {
  if (!in.ok()) throw std::runtime_error(std::string(in.status().message()));
  return *in;
}

template <class T>
auto saveProto(const T& obj) {
  return py::bytes(obj.SerializeAsString());
}

template <class T>
auto loadProto(T& obj, const py::bytes& data) {
  if (!obj.ParseFromString(data)) {
    throw std::invalid_argument("failed to parse proto data");
  }
}

void bind(pybind11::module& m) {
    m.doc() =
        "Private Set Intersection Cardinality protocol";

    py::class_<psi_proto::Setup>(m, "cpp_proto_setup")
        .def(py::init<>())
        .def("load", [](psi_proto::Setup& obj,
                        const py::bytes& data) { return loadProto(obj, data); })
        .def("save",
            [](const psi_proto::Setup& obj) { return saveProto(obj); })
        .def_static("Load", [](const py::bytes& data) {
            psi_proto::Setup obj;
            loadProto(obj, data);
            return obj;
        });

    py::class_<psi_proto::Request>(m, "cpp_proto_request")
        .def(py::init<>())
        .def("load", [](psi_proto::Request& obj,
                        const py::bytes& data) { return loadProto(obj, data); })
        .def("save", [](const psi_proto::Request& obj) { return saveProto(obj); })
        .def_static("Load", [](const py::bytes& data) {
            psi_proto::Request obj;
            loadProto(obj, data);
            return obj; 
        });

    py::class_<psi_proto::Response>(m, "cpp_proto_response")
        .def(py::init<>())
        .def("load", [](psi_proto::Response& obj,
                        const py::bytes& data) { return loadProto(obj, data); })
        .def("save",
            [](const psi_proto::Response& obj) { return saveProto(obj); })
        .def_static("Load", [](const py::bytes& data) {
            psi_proto::Response obj;
            loadProto(obj, data);
            return obj;
        });


    py::class_<psi_proto::Result>(m, "cpp_proto_result")
        .def(py::init<>())
        .def("load", [](psi_proto::Result& obj,
                        const py::bytes& data) { return loadProto(obj, data); })
        .def("save",
            [](const psi_proto::Result& obj) { return saveProto(obj); })
        .def_static("Load", [](const py::bytes& data) {
            psi_proto::Result obj;
            loadProto(obj, data);
            return obj;
        });

    

    py::class_<psi::PsiNode>(m, "cpp_node")
        .def_static(
            "CreateWithNewKey",
            []() {
                auto node = psi::PsiNode::CreateWithNewKey();
                if (!node.ok())
                throw std::runtime_error(std::string(node.status().message()));
                return std::move(*node);
            },
            py::call_guard<py::gil_scoped_release>())
        .def_static(
            "CreateFromKey",
            [](const std::string& key_bytes) {
                auto node =
                    psi::PsiNode::CreateFromKey(key_bytes);
                if (!node.ok())
                throw std::runtime_error(std::string(node.status().message()));
                return std::move(*node);
            },
            py::call_guard<py::gil_scoped_release>())
        .def(
            "CreateRequest",
            [](const psi::PsiNode& obj,
                const std::vector<std::string>& inputs) {
                return throwOrReturn(obj.CreateRequest(inputs));
            },
            py::call_guard<py::gil_scoped_release>())
        .def(
          "ProcessRequest",
          [](const psi::PsiNode& obj,
             const psi_proto::Request& request,
             const std::vector<std::string>& inputs) {
            return throwOrReturn(obj.ProcessRequest(request,inputs));
          },
          py::call_guard<py::gil_scoped_release>())
        .def(
            "ProcessResponse",
            [](const psi::PsiNode& obj,
                const psi_proto::Response& response) {
                return throwOrReturn(obj.ProcessResponse(response));
            },
            py::call_guard<py::gil_scoped_release>())
        .def(
            "GetPrivateKeyBytes",
            [](const psi::PsiNode& obj) {
                return py::bytes(obj.GetPrivateKeyBytes());
            },
            py::call_guard<py::gil_scoped_release>());

}

PYBIND11_MODULE(psi_ca, m) { bind(m); }
PYBIND11_MODULE(_psi_ca, m) { bind(m); }
