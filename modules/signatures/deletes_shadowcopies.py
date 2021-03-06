# Copyright (C) 2015 Accuvant, Inc. (bspengler@accuvant.com)
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class DeletesShadowCopies(Signature):
    name = "deletes_shadow_copies"
    description = "Attempts to delete volume shadow copies"
    severity = 3
    categories = ["ransomware"]
    authors = ["Accuvant"]
    minimum = "1.2"
    evented = True

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)

    filter_apinames = set(["CreateInternalProcessW","ShellExecuteExW"])

    def on_call(self, call, process):
        if call["api"] == "CreateInternalProcessW":
            cmdline = self.get_argument(call, "CommandLine").lower()
            if "vssadmin" in cmdline and "delete" in cmdline and "shadows" in cmdline:
                return True
        elif call["api"] == "ShellExecuteExW":
            filepath = self.get_argument(call, "FilePath").lower()
            params = self.get_argument(call, "Parameters").lower()
            if "vssadmin" in filepath and "delete" in params and "shadows" in params:
                return True
