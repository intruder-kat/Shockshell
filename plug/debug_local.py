"""
a garbage plugin which runs commands on our local machine for testing and debugging
"""

import subprocess

class _Plug():

    def init_session(*args):
        pass

    def exit_session(self):
        pass

    def command(self, bstr):
        sub = subprocess.run(bstr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return (sub.returncode, sub.stdout)

plugin = _Plug()

