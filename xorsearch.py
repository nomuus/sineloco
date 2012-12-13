#############################################################################
__version__ = '1.0'
__status__ = 'beta'
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
__description__ = 'xor cipher-texts to locate plain-texts using keywords'
#############################################################################
#############################################################################
def slice_search(data, s, limit=-1):
    offset = data.find(s)
    if limit == 1:
        yield offset
        offset = -1
    if offset != -1:
        yield offset
        last_offset = offset
        while last_offset != -1:
            offset = data[last_offset+len(s):].find(s)
            if offset == -1:
                break
            else:
                offset = last_offset + len(s) + offset
                if offset != last_offset:
                    yield offset
                    last_offset = offset
                else:
                    break
#############################################################################
def xor(data, x):
    if isinstance(data, bytearray):
        pass
    elif isinstance(data, basestring):
        data = bytearray(data)
    elif isinstance(data, list):
        data = bytearray("".join([str(s) for s in data]))
    else:
        data = bytearray(str(data))
    c = len(data) - 1
    while c > -1:
        data[c] ^= x
        c -= 1
    return data
#############################################################################
def test_xorsearch(rpad=50):
    ciphertext = xor("http://www.nomuus.com/", 0x0A)
    print "Ciphertext"
    print "-" * 55
    print repr(str(ciphertext))
    print
    print "Xorsearch"
    print "-" * 55
    i = 0x00
    while i < 256:
        plaintext = xor(bytearray(ciphertext), i)
        for x in slice_search(plaintext, "http"):
            pt = repr(str(plaintext[x:x+rpad]))
            print "0x%x key @ offset %d -> %s" % (i, x, pt)
        i += 1
#############################################################################
if __name__ == "__main__":
    test_xorsearch()
