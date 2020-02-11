"""Compile Nim libraries as Python Extension Modules.

If you want your namespace to coexist with your pthon code, name this ponim.nim
and then your import will look like `from ponim.nim import adder` and
`from ponim import subtractor`. There must be a way to smooth that out in the
__init__.py file somehow.

Note that the file must be in the included source code dir. Currently it is
easiest to just put this in with your python code.
"""

from os import listdir, mkdir
from os.path import join, expanduser
from setuptools import Extension
from shutil import copyfile, rmtree
from typing import Sequence, Dict, List
import subprocess
import sys


# class NimLib(TypedDict):
#     """Wrapper around a lib name and path for nim cdoe"""

#     name: str
#     path: str


def nythonize(nimbase: str, modules: Sequence[Dict[str, str]]) -> List[Extension]:
    """Compile a Nim library as a Python Extension Module.

    `nimbase` is the path to `nimbase.h` on your system, which is needed for 
    Python to compile gene Nim generated C code.


    This builds a set of Extenstions, which are then passed back to setuptools.
    """
    extensions = []
    # Create a top level working dir
    rmtree(join("build", "nim_build"), ignore_errors=True)
    mkdir(join("build", "nim_build"))
    for module in modules:
        module_dir = join("build", "nim_build", f"{module['name']}_build")
        rmtree(module_dir, ignore_errors=True)
        mkdir(module_dir)
        subprocess.run(
            [
                "nim",
                "compileToC",
                "--compileOnly",
                "-d:release",
                "-d:ssl",
                "--app:lib",
                "--opt:speed",
                "--gc:markAndSweep",
                f"--nimcache:{module_dir}",
                module["path"],
            ],
            check=True,
            stderr=sys.stdout.buffer,
        )
        copyfile(
            nimbase, join(module_dir, "nimbase.h"),
        )
        sources = []
        for c_source_file in listdir(module_dir):
            if c_source_file.endswith(".c"):
                sources.append(join(module_dir, c_source_file))
        extensions.append(
            Extension(
                name=module["name"],
                sources=sources,
                extra_compile_args=[
                    "-flto",
                    "-ffast-math",
                    "-march=native",
                    "-mtune=native",
                    "-O3",
                    "-fno-ident",
                    "-fsingle-precision-constant",
                ],
                extra_link_args=["-s"],
                include_dirs=[module_dir],
            )
        )
    return extensions
