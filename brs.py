#!/usr/bin/env python3

import os
import sys
import shutil

_from = sys.argv[1]
_to = sys.argv[2]

total_hint = 1075345

badfiles = []
all_files = 0


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


def _copy(src, dst, *, follow_symlinks=True):
    global all_files, _from
    relpath = os.path.relpath(src, _from)
    print("# Copying", relpath, "-> ", end="", flush=True)
    try:
        # shutil.copy2(src, os.devnull)
        shutil.copy2(src, dst)
        try:
            st = os.stat(src)
            shutil.chown(dst, st.st_uid, st.st_gid)
        except Exception as _:
            pass
        print("OK", end="")
    except Exception as e:
        badfiles.append(src)
        print(e, "FAIL", end="")
    all_files += 1
    print(" (", all_files, "/", total_hint, ")", sep="", flush=True)


shutil.copytree(_from, _to, symlinks=True, copy_function=_copy)


print("Total tried:", all_files, "files")
print("Failed files:", len(badfiles))
badfile_txt = os.path.join(_to, ".badfiles.txt")

with open(badfile_txt, "w") as f:
    f.write("\n".join(badfiles))
