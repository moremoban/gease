pip freeze
coverage run -m --source=gease pytest --doctest-modules && coverage report --show-missing
