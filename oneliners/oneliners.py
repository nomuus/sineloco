__version__ = "0.1"
__author__ = "nomuus"
__copyright__ = """Copyright (c) 2012, nomuus. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    * Neither the name of the copyright holder nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
__email__ = "mu*nre*txemusu*da"[::-1].replace('*', '') + "!@#$%^&*()"[1] + "nomuus" + "+..com"[2:]
__company__ = 'www.nomuus.com'
__description__ = 'Python one-liners'


# IP Obfuscator: Inspired by IP Obfuscation Calculator <http://ha.ckers.org/xss.html>
obfuscate_ip = lambda ip, level=0: (lambda n=[int(n) for n in ip.split('.')], d={0: 16777216, 1:65536, 2:256}: (lambda dw=sum(map(lambda x: n[x] * d[x], d)) + n[3] +(4294967296*level), oc=[str(oct(a)).zfill(4) for a in n], hx=["0x%s" % hex(a)[2:].zfill(2) for a in n]: map(lambda b: '.'.join(b), [[str(dw)], oc, hx]))())() if ip.count('.') == 3 and level in [0, 1] and len([n for n in ip.split('.') if n.isdigit() and int(n) >= 0 and int(n) <= 255]) == 4 else []
