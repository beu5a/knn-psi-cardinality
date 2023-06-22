import pytest
import sys
import python as psi


def helper_create_request(c, inputs):
    req = c.CreateRequest(inputs)
    return req

@pytest.mark.parametrize("cnt", [1, 10, 100, 1000, 10000])
def test_create_request(cnt, benchmark):
    c = psi.Node.CreateWithNewKey()
    inputs = ["Element " + str(i) for i in range(cnt)]
    benchmark(helper_create_request, c, inputs)




def helper_process_request(s, req, inputs2):
    resp = s.ProcessRequest(req, inputs2)
    return resp
 
@pytest.mark.parametrize("cnt", [1, 10, 100, 1000, 10000])
def test_process_request(cnt, benchmark):
    c = psi.Node.CreateWithNewKey()
    s = psi.Node.CreateWithNewKey()
    inputs = ["Element " + str(i) for i in range(cnt)]
    inputs2 = ["Element " + str(i) for i in range(100)]
    req = c.CreateRequest(inputs)
    benchmark(helper_process_request, s, req, inputs2)

def helper_process_response(c, resp):
    out = c.ProcessResponse(resp)
    return out

@pytest.mark.parametrize("cnt", [1, 10, 100, 1000, 10000])
def test_process_response(cnt, benchmark):
    c = psi.Node.CreateWithNewKey()
    s = psi.Node.CreateWithNewKey()
    inputs = ["Element " + str(i) for i in range(cnt)]
    inputs2 = ["Element " + str(i) for i in range(100)]
    req = c.CreateRequest(inputs)
    resp = s.ProcessRequest(req, inputs2)
    benchmark(helper_process_response, c, resp)

if __name__ == "__main__":
    sys.exit(pytest.main(["-s", "-v", "-x", __file__]))
