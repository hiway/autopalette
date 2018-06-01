rm -r dist
rm -r build
pandoc --from=markdown --to=rst README.md > README.rst && \
python setup.py sdist bdist_wheel
