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
    src_fd = os.open(src, os.O_RDONLY | os.O_BINARY)
    dst_fd = os.open(dst, os.O_WRONLY | os.O_CREAT | os.O_BINARY)
    while offset < st.st_size:
        try:
            buf = os.pread(src_fd, blocksize, offset)
        except Exception as e:
            print(" #", src, "bad block of", blocksize, "@", offset)
        else:
            os.pwrite(dst_fd, buf, offset)
        offset += len(buf)

    os.close(src_fd)
    os.close(dst_fd)

    shutil.copystat(src, dst)
    shutil.chown(dst, st.st_uid, st.st_gid)


try_harder(_from, _to)
