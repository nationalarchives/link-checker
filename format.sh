poetry run isort --profile black --overwrite-in-place app
poetry run black -t py311 --line-length 80 --verbose app
poetry run flake8 --ignore E203,E266,E501,W503,F403,F401 --max-line-length 80 app