
"""

    Network Error Object Decoded from CAPE V2 returned data

"""

class CapeSandboxNetError(object):
    def __init__(self, detail: str) -> None:
        self.detail = detail
