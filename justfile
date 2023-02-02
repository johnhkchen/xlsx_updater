ok:
  just format
  just lint
  just test
  just clean

main:
  python3 src/main.py

test:
  python3 -m tox

lint:
  python3 -m flake8 src tests --max-line-length 88

format:
  python3 -m black src tests

clean:
  rm -f output/yaml/*.yaml
  rm -f output/xlsx/*.xlsx
  rm -f tests/output/yaml/*.yaml
  rm -f tests/output/xlsx/*.xlsx