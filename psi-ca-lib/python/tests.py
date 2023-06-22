import pytest
import sys
import re
from math import ceil, floor

import python as psi

node_key_1 = bytes(range(32))
node_key_2 = bytes(range(1, 33))

n_inputs_node_1 = 10
n_inputs_node_2 = 100
node_1_items = ["Element " + str(i) for i in range(n_inputs_node_1)]
node_2_items = ["Element " + str(2 * i) for i in range(n_inputs_node_2)]



def test_static_key():
    c = psi.Node.CreateFromKey(node_key_1)
    assert c.GetPrivateKeyBytes() == node_key_1

    s = psi.Node.CreateFromKey(node_key_2)
    assert s.GetPrivateKeyBytes() == node_key_2



def test_integration():
    c = psi.Node.CreateWithNewKey()
    s = psi.Node.CreateWithNewKey()



    request = psi.Request()
    request.ParseFromString(c.CreateRequest(node_1_items).SerializeToString())

    response = psi.Response()
    response.ParseFromString(s.ProcessRequest(request,node_2_items).SerializeToString())


    intersection = c.ProcessResponse(response)


    assert intersection >= floor(n_inputs_node_1 / 2.0)
    assert intersection <= ceil((n_inputs_node_1 / 2.0) * 1.1)


if __name__ == "__main__":
    sys.exit(pytest.main(["-s", "-v", "-x", __file__]))
