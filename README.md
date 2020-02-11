# Nython 

Build Python Extension Modules for Nim libraries.

## Synopsis

This is using Nim's compileToC command to generate C code that Python can then pakcage as an extension module and compile natively when your package is installed elsewhere.

## System Reqs

- [Nim](https://nim-lang.org/)
- [Nimpy](https://github.com/yglukhov/nimpy)

## Install

Using your favorite Python package manager, this library lives on pypi

```
pip install nython
```

## Usage

See the example folder of a working project that uses nython (and runs all the tests).

### Poetry

- Add `nython` as package dependancy
- In the `[tool.poetry]` section of the `pyproject.toml`, add `build = "build.py"
- Create the file `build.py` in top level of your project. This will be called by poetry when creating the package, essentially it just needs to have a `build` function that takes a dict of setup kwargs and adds to it.
- Add your Nim modules, nythonize them, and pass them back
- Note: you must pass in nimbase.h
- Note: your nim code must live in a directory that is included in your package build process. It can live side by side with your python.

```python
# Example build.py script
from nython import nythonize
from os.path import expanduser


def build(setup_kwargs):
    """Called by poetry, the args are added to the kwargs for setup."""
    nimbase = expanduser("~") + "/.choosenim/toolchains/nim-1.0.4/lib/nimbase.h"
    setup_kwargs.update(
        {
            "ext_modules": nythonize(
                nimbase, [{"name": "adder", "path": "ponim/adder.nim"}]
            ),
        }
    )
```

### Setuptools

Todo - but basically just add `ext_modules = nythonize(nimbase, [{"name": "adder", "path": "ponim/adder.nim"}])` to your setup call

## Development

### Goals

Create a seamless development experience for integrating Nim code with Python. Nim should be so easy to use that eventually you just end up writing Nim-only modules for Python, and then realize you don't really need Python and migrate to just Nim. This package should enable Nim in places and companies where it can't be selected as the primary language for a project, but it can be reached for when performance is needed. This should be easier to use than Cython.

### Tests

Currently this is tested by running the code in the example project. I would like to find a better way to do this, so if you have a good idea, feel free to contribute!

Currently:

```
cd example
poetry shell
poetry install
poetry run py_test
```

And that is it. 

### TODOs

- Support Nimble / full nim projects with dependancies
- Allow for fine-grained compiler option tuning
- Remove the spurious .so file that ends up in your project root dir.
- Remove the dep fo passing in nimbase.h and find it on the system somehow
- Possibly create a nim install in your local virtualenv somehow, with nimpy
- Generate some performance tests, although that is more on nimpy than this package