all: build

build:
	/home/hydrogen/.solc-select/usr/bin/solc-v0.8.0 contracts/SwearJar.sol -o build --abi --bin

test:
	python -i scripts/test.py

deploy: build
	python scripts/deploy.py

