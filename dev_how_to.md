# How-To for Package Development

## Run Tests with Pytest
In the terminal
```
pytest -vv
```

## Generate a Code Coverage Report as HTML
In the terminal
```
pytest --cov --cov-report=html:cov_html
```

## Upload a New Version to PyPi
After all tests pass and the code coverage report has been generated,

1. Increment the version number in *pyproject.toml*
2. Generate distribution archives: Run `python3 -m pip install --upgrade build` then `python3 -m build`
3. Upload the distribution archives to TestPyPi: Run `python3 -m pip install --upgrade twine` then `python3 -m twine upload --repository testpypi dist/*`
4. Upload the distribution archives to PyPi: Run `twine upload dist/*`
