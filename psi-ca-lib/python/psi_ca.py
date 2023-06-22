
from typing import List

from . import _psi_ca as psi_ca
## Add proto import here

from .psi_ca_pb2 import (
    Setup,
    Request,
    Response,
)

class Node:

    def __init__(self, data: psi_ca.cpp_node):
        self.data = data

    @classmethod
    def CreateWithNewKey(cls):
        return cls(psi_ca.cpp_node.CreateWithNewKey())

    @classmethod
    def CreateFromKey(cls, key_bytes: bytes):
        return cls(psi_ca.cpp_node.CreateFromKey(key_bytes))

    def CreateRequest(self, inputs: List[str]) -> Request:
        interm_req = self.data.CreateRequest(inputs).save()
        req = Request()
        req.ParseFromString(interm_req)
        return req
    
    def ProcessRequest(self, request: Request , inputs: List[str]) -> Response:
        interm_req = psi_ca.cpp_proto_request.Load(request.SerializeToString())
        interm_resp = self.data.ProcessRequest(interm_req,inputs).save()
        resp = Response()
        resp.ParseFromString(interm_resp)
        return resp

    
    def ProcessResponse(self, response: Response) -> int:
        interm_resp = psi_ca.cpp_proto_response.Load(response.SerializeToString())
        res = self.data.ProcessResponse(interm_resp)
        return res

    def GetPrivateKeyBytes(self) -> bytes:
        return self.data.GetPrivateKeyBytes()




__all__ = [
    "Node",
    "Setup",
    "Response",
    "Request",
]
