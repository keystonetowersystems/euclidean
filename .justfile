build: clean
  python setup.py sdist

clean:
  rm -rf dist

# packagr credentials are define in ~/.pypirc
release: build
  git push --follow-tags origin master
  twine upload --repository packagr dist/*

test:
  python -m pytest

coverage:
  coverage run -m pytest
  coverage html
