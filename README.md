# data_handling

Implement SOLID data input and output methods with simple APIs. Make them easy to swap as new input and output types are needed by extending the functionality, without modification.

If you use a config setup to provide the paths, then only the format_type argument and config.base_path has to change when a new file format is used.


## Installation
Getting started running code in this project is easy.

1. First, clone the repository:
    ```bash
    git clone https://github.com/AndersHenriksen-dev/data_handling
    cd data_handling
    ```


2. This project uses `uv` as dependency manager, make sure you have `uv` installed. You can find installation instructions [here](https://uv.dev/).
3. You might have to run the following to make sure uv is installed in path:
    ```bash
    uv tool install uv
    uv tool update-shell
    ```
    or
    ```bash
    pip install uv
    uv tool update-shell
    ```

4. Then, install the dependencies:
    ```bash
    uv sync
    ```

Alternately, just copy the data_io.py and test_data_io.py files into your project and ``uv add`` the dependencies to your project.

## Acknowledgements

Created using [python mlops template](https://github.com/AndersHenriksen-dev/python_mlops_cookiecutter_template),
a [cookiecutter template](https://github.com/cookiecutter/cookiecutter) for getting started with new python projects.
