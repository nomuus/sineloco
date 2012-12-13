#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import os
import re
import sys
#############################################################################
#############################################################################
__version__ = '1.0'
__status__ = 'release'
__author__ = 'nomuus'
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
__email__ = "%s%cnomuus.%com" % (
    "".join([chr((i>>8)&0xff)+chr(i&0xff) for i in[24932,30067,30061,25976,
    29797,29294,30061]]), 64, 99
)
__company__ = 'www.nomuus.com'
__description__ = 'replace tabs with spaces or vice versa'
#############################################################################
#############################################################################
DEFAULT_NUM = 4
#############################################################################
def num_from_arg(arg, s):
    x = arg.replace(s, "").lstrip("=:")
    return int(x) if x.isdigit() else DEFAULT_NUM
#############################################################################
def usage(silent=0):
    basename = os.path.basename(sys.argv[0])
    
    if silent == 0xff:
        cpr = __copyright__.split("\n")[0]
        div = lambda c: c * 78
        banner = str(
            " _ __   _____   _____  \n" +
            "| '_ \ / _ \ \ / / _ \ \n" +
            "| | | | (_) \ V / (_) |\n" +
            "|_| |_|\___/ \_/ \___/ [%s - %s]\n" %  (basename, __version__) +
            div(".") + "\n" + __copyright__ + "\n"
        )
        sys.stdout.write(banner)
        return 0
    sys.stdout.write("usage: %s ACTION FILE\n" % basename)
    sys.stdout.write("       PIPE | %s ACTION\n" % basename)
    sys.stdout.write("       %s ACTION < REDIRECT\n\n" % basename)
    if silent:
        return silent
    sys.stdout.write("ACTION\n")
    sys.stdout.write("--tab-to-space=N,       Replace tabs with N number of spaces.\n")
    sys.stdout.write("--tab-to-space          If N is omitted, defaults to %d.\n\n" % DEFAULT_NUM)
    sys.stdout.write("--space-to-tab=N,       Replace N number of spaces with tab.\n")
    sys.stdout.write("--space-to-tab          If \"=N\" is omitted, defaults to %d.\n\n" % DEFAULT_NUM)
    sys.stdout.write("--version, --license    Display version and license information.\n\n")
    sys.stdout.write("FILE\n")
    sys.stdout.write("Replace lines in file beginning with those specified by ACTION.\n\n")
    sys.stdout.write("PIPE\n")
    sys.stdout.write("Replace piped lines beginning with those specified by ACTION.\n\n")
    sys.stdout.write("REDIRECT\n")
    sys.stdout.write("Replace redirected lines beginning with those specified by ACTION.\n")
    return 0
#############################################################################
def stream_line(fd, brk="\n"):
    chunk = []
    x = fd.read(1)
    chunk.append(x)
    while x:
        if x == brk:
            yield "".join(chunk)
            del chunk[:]
        x = fd.read(1)
        chunk.append(x)
    yield "".join(chunk)
#############################################################################
def __main(argv):
    len_argv = len(argv)
    n = DEFAULT_NUM
    S2T = "--space-to-tab"
    T2S = "--tab-to-space"
    VER = "--version"
    LIC = "--license"
    USE = "--usage"
    HEL = "--help"
    
    if VER in argv or LIC in argv:
        sys.exit(usage(0xff))
    if USE in argv or HEL in argv:
        sys.exit(usage(0))
    
    # Parse FILE argument
    if len_argv == 2:
        if sys.stdin.isatty():
            sys.exit(usage(-1))
        i = 1
    elif len_argv > 2:
        if os.path.isfile(argv[1]):
            path = os.path.abspath(argv[1])
            i = 2
        elif os.path.isfile(argv[2]):
            path = os.path.abspath(argv[2])
            i = 1
        else:
            sys.stderr.write("No file specified.\n")
            sys.exit(usage(-2))
    else:
        sys.exit(usage(0))

    # Parse ACTION argument
    if argv[i].lower().startswith(T2S):
        n = num_from_arg(argv[i], T2S)
        act = action = "\t "
        re_action = re.compile("^([\t])+")
    elif argv[i].lower().startswith(S2T):
        n = num_from_arg(argv[i], S2T)
        re_action = re.compile("^([ ]{%d})+" % n)
        act = action = " \t"
    else:
        sys.stderr.write("Invalid action specified.\n\n")
        sys.exit(usage(-3))

    # Read FILE or PIPE data
    # NOTE: Encoding may become a factor, as may the 'n' multiplier.
    if not sys.stdin.isatty():
        fd = sys.stdin
    else:
        fd = open(path, 'r')
        atexit.register(fd.close)
    
    for x in stream_line(fd):
        m = re_action.search(x)
        if m:
            s = m.group(0)
        else:
            sys.stdout.write(x)
            continue
        if action == "\t ":
            sys.stdout.write(re_action.sub(s.replace(act[0], act[1] * n), x))
        elif action == " \t":
            sys.stdout.write(re_action.sub(s.replace(act[0] * n, act[1]), x))
        else:
            sys.stderr.write("Unknown action: %s.\n\n" % repr(action))
            sys.exit(usage(-4))
#############################################################################
#############################################################################
if __name__ == "__main__":
    try:
        __main(sys.argv)
    except KeyboardInterrupt:
        sys.stderr.write("Operation aborted.\n")
        sys.exit(1)
