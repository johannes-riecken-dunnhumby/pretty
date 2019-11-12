import std.format;
import std.string;
extern (C) {
    immutable(char)* writeln_AArray(long addr) {
        immutable(char)* ret = toStringz(format("%s", *cast(int[][int]*)addr));
        return ret;
    }
}
