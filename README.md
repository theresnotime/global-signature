# global-signature
A Python script to add a global signature to your user preference on all (or just one) attached Wikimedia wiki(s).

## Usage
### Clone the repo
```shell
git clone https://github.com/theresnotime/global-signature.git
```

### Set up a virtual environment
```shell
python3 -m venv venv && source venv/bin/activate
```

### Install dependencies
```shell
pip install -r requirements.txt
```

### Create config file
```shell
cp config.example.py config.py
```
Now edit `config.py`:
```python
# Use Special:BotPasswords to generate a bot password
BOT_USER = ""
BOT_PASS = ""
USER_SIGNATURE = "— [[User:Example|Example]] ([[User talk:Example|talk]])"
```

### Read the help
```
$ python3 global-sig.py -h

global-sig v0.0.1
usage: global-sig.py [-h] [--all] [-w WIKI] [-d] [-v]

global-sig, v0.0.1

options:
  -h, --help            show this help message and exit
  --all                 Run on all attached wikis
  -w WIKI, --wiki WIKI  The wiki domain to run on
  -d, --dry             Don't make any changes
  -v, --verbose         Be verbose
```

## Examples
### Run on all attached wikis
```shell
python3 global-sig.py --all --verbose
```

### Run on a specific wiki
```shell
python3 global-sig.py --wiki en.wikipedia.org --verbose
```