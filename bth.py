#!/usr/bin/env python3

import os
import sys
import shutil

_from = sys.argv[1]
_to = sys.argv[2]


def try_harder(src, dst):
    st = os.stat(src)
    offset = 0
    blocksize = st.st_blksize
    src_fd = os.open(src, os.O_RDONLY)
    dst_fd = os.open(dst, os.O_WRONLY | os.O_CREAT)
    good = 0
    bad = 0
    print(" #", src)
    while offset < st.st_size:
        try:
            buf = os.pread(src_fd, blocksize, offset)
        except Exception as e:
            offset += len(blocksize)
            bad += 1
            print("X", end="", flush=True)
        else:
            os.pwrite(dst_fd, buf, offset)
            offset += len(buf)
            good += 1
            print(".", end="", flush=True)

    shutil.copystat(src, dst)
    shutil.chown(dst, st.st_uid, st.st_gid)

    print("")
    print("# Total (good/bad):", good, "/", bad)


try_harder(_from, _to)
