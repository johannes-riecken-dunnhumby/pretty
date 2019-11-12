import subprocess
import os

class fooPrinter:
    """Print an associative array."""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        typ = self.val.type

        f = open('helpers.d', 'w')
        contents = """import std.format;
import std.string;
extern (C) {
    immutable(char)* writeln_AArray(long addr) {
        immutable(char)* ret = toStringz(format("%%s", *cast(%s*)addr));
        return ret;
    }
}
""" % (self.val.type)
        f.write(contents)
        f.close()
        subprocess.run(["gdc-9", "-g", "-shared", "-fPIC", "-o", "libhelpers.so", "helpers.d"])
        gdb.parse_and_eval("""(void*)dlopen("%s/libhelpers.so", 2)""" %
                os.getcwd())
        ret = gdb.parse_and_eval("(char*)writeln_AArray(%s)" % (self.val.address))
        return ret

import gdb.printing

def build_pretty_printer():
    pp = gdb.printing.RegexpCollectionPrettyPrinter(
        "my_library")
    pp.add_printer('foo', '.*\[.*\].*', fooPrinter)
    return pp
