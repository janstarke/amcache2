# amcache2.py
creates a bodyfile from AmCache.hve

## Installation

I recommend to use *pipenv* instead of *venv*, because using *venv* I had problems with https://github.com/construct/construct/pull/930

```shell
pipenv install amcache2
```

## Usage
```shell
usage: amcache2.py [-h] registry_hive

Parse program execution entries from the Amcache.hve Registry hive

positional arguments:
  registry_hive  Path to the Amcache.hve hive to process

options:
  -h, --help     show this help message and exit
```

## Example
```shell
pipenv run amcache2.py Amcache.hve | mactime -d -b -
```