#!/usr/bin/env python3

import os
import sys
import shutil

_from = sys.argv[1]
_to = sys.argv[2]

total_hint = 1075345

badfiles = []
all_files = 0


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
