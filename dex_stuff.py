import hashlib
import struct
import zlib

__version__ = '1.0'
__status__ = 'WTF'
__author__ = 'nomuus'
__copyright__ = """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""
__email__ = "%s%cnomuus.%com" % (
    "".join([chr((i>>8)&0xff)+chr(i&0xff) for i in[24932,30067,30061,25976,
    29797,29294,30061]]), 64, 99
)
__company__ = 'www.nomuus.com'
__description__ = 'dex related stuff'

# DEX file header:
# magic               : 'dex\n035\0'
# checksum            : 900dbaad
# signature           : c00l...d00d
# file_size           : 3643816
# header_size         : 112
# link_size           : 0
# link_off            : 0 (0x000000)
# string_ids_size     : 28244
# string_ids_off      : 112 (0x000070)
# type_ids_size       : 3351
# type_ids_off        : 113088 (0x01b9c0)
# field_ids_size      : 10716
# field_ids_off       : 197556 (0x0303b4)
# method_ids_size     : 23914
# method_ids_off      : 283284 (0x045294)
# class_defs_size     : 2506
# class_defs_off      : 474596 (0x073de4)
# data_size           : 3089028
# data_off            : 554788 (0x087724)
# ...

# TODO: Optimize this hacked together code.
class DexStuff(object):
    # http://source.android.com/tech/dalvik/dex-format.html
    # header_item
    def __init__(self):
        pass
    # #######################################################################
    def get_magicnum(self, data):
        return data[0:8]
    # #######################################################################
    def get_checksum(self, data, endian_out):
        #return struct.unpack("<I", data[8:12])
        if endian_out in ["little", "as-is"]:  # as-is the dex file
            return data[8:12] if len(data) >= 12 else None
        else:  # big-endian, ">", or "human"
            return data[8:12][::-1] if len(data) >= 12 else None
    # #######################################################################
    def get_signature(self, data):
        return data[12:32]
    # #######################################################################
    def new_checksum(self, data, endian_out):
        # checksum	uint	adler32 checksum of the rest of the file 
        #                   (everything but magic and this field); used 
        #                   to detect file corruption
        checksum = zlib.adler32(data[12:]) & 0xffffffff
        if endian_out in ["little", "as-is"]:
            return struct.pack("<I", checksum)
        else:  # big-endian, ">", or "human"
            return struct.pack(">I", checksum)
    # #######################################################################
    def new_signature(self, data):
        # signature	ubyte[20]	SHA-1 signature (hash) of the rest of the 
        #                       file (everything but magic, checksum, and 
        #                       this field); used to uniquely identify files
        h = hashlib.sha1()
        h.update(data[32:])
        return h.digest()
    # #######################################################################
    def valid_magic(self, data):
        magic = self.get_magicnum(data)
        if magic.startswith("dex\n") and magic.endswith("\0"):
            return True
        return False
    # #######################################################################
    def fix_dex(self, data):
        if not self.valid_magic(data):
            magic = "dex\n035\0"
        else:
            magic = self.get_magicnum(data)
        buf = bytearray(data)
        buf[0:8] = magic
        new_sig = self.new_signature(str(buf))
        buf[12:32] = new_sig
        new_sum = self.new_checksum(str(buf), "little")
        buf[8:12] = new_sum
        return buf
#############################################################################
def test_stuff(dex_file):
    ds = DexStuff()
    with open(dex_file, 'rb') as f:
        valid = ds.valid_magic(f.read(8))
        if not valid:
            return -1
        f.seek(0)
        data = f.read()
    if not data:
        return -2
    
    print "Current"
    print "-" * 55
    print "Checksum ", ds.get_checksum(data, "like_dexdump").encode("hex")
    print "Signature", ds.get_signature(data).encode("hex")
    print
    print "Modified"
    print "-" * 55
    data = str(ds.fix_dex(data + "\xFF"))
    print "Checksum ", ds.get_checksum(data, "like_dexdump").encode("hex")
    print "Signature", ds.get_signature(data).encode("hex")
    
    return 0
#############################################################################	
#############################################################################
if __name__ == "__main__":
    import os
    import sys
    ret = 1
    if os.path.isfile(sys.argv[1]):
        ret = test_stuff(sys.argv[1])
    sys.exit(ret)
