# data_handling

Implement SOLID data input and output methods with simple APIs. Make them easy to swap as new input and output types are needed by extending the functionality, without modification.

If you use a config setup to provide the paths, then only the format_type argument and config.base_path has to change when a new file format is used.


## Installation
Getting started running code in this project is easy.

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AndersHenriksen-dev/data_handling
    cd data_handling
    ```


2. **Install uv:**
   This project uses `uv` as dependency manager, make sure you have `uv` installed. You can find installation instructions [here](https://uv.dev/).
3. **Install uv in path:**
   You might have to run the following to make sure uv is installed in path:
    ```bash
    uv tool install uv
    uv tool update-shell
    ```
    or
    ```bash
    pip install uv
    uv tool update-shell
    ```

4. **install the dependencies:**
   If you intend to develop and wish to run tests:
    ```bash
    uv sync
    ```

    If you just want to use the code and don't care about tests:
     ```bash
    uv sync --no-dev
    ```

Alternately, just copy the data_io.py and test_data_io.py files into your project and ``uv add`` the dependencies to your project.

## Acknowledgements

Created using [python mlops template](https://github.com/AndersHenriksen-dev/python_mlops_cookiecutter_template),
a [cookiecutter template](https://github.com/cookiecutter/cookiecutter) for getting started with new python projects.
