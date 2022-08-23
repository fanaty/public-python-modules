# public-python-modules

##### How to push a new version
0. Commit your code
1. Update version in **pyproject.toml**
2. `git add pyproject.toml`
3. `git commit -m '<version>'`
4. `git tag <version>`
5.  `git push --tags`

*This last command will not push your code to a branch. Use `git push` as you would do normally to accomplish this.*

##### How to install a specific version

Put this inside the requirements.txt of other project:
`git+https://github.com/fanaty/public-python-modules.git@0.7`

You can also install from the **master** branch by omitting the `@<version>` portion.
If **pyproject.toml** is in the root directory of the repository, you can omit the subdirectory bit.

##### How to import modules
The package contains modules. Here's an example import:
```py
from ppm import test_module
```


##### Hot to generate .pyi (stub) files

```bash
source .venv/bin/activate
pip install mypy
cd src
stubgen ppm/*.py -o .
```