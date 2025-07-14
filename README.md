# Snusbase Lookup

~~This is just a script I wrote to lookup domains and emails using the snusbase api. Currently I only need domain and email, but plan on adding more features as I need to for my osint and other projects.~~

~~NOTE: I need to do better error handling so some stuff is broken and I haven't gotten around to fixing it.~~

I finally managed to add username, domain, email, etc and made the code a tad bit better. There might be some bugs here and there, but things work from all my various testing.

------

### Install:

```bash
python3 -m venv venv
venv/bin/pip3 install requests requests.auth argparse snusbase
```

Replace ```snusbase_auth = "API_KEY"``` with your key from your account.

------

### Usage:

```bash
usage: main.py [-h] [--email EMAIL] [--domain DOMAIN] [--username USERNAME] [--getemails | --no-getemails | -ge] [--input INPUT]
               [--domainfile | --no-domainfile | -df] [--emailfile | --no-emailfile | -ef] [--usernamefile | --no-usernamefile | -uf]
               [--output OUTPUT] [--json JSON]

Simple python3 program to check if an email, username, and domain is in any data breaches.

options:
  -h, --help            show this help message and exit
  --email, -e EMAIL     Email to check.
  --domain, -d DOMAIN   Domain to check
  --username, -u USERNAME
                        Username to check
  --getemails, --no-getemails, -ge
                        Extract emails from results
  --input, -i INPUT     File with emails or domains, one on each line.
  --domainfile, --no-domainfile, -df
                        Define if input file is for domains
  --emailfile, --no-emailfile, -ef
                        Define if input file is for emails
  --usernamefile, --no-usernamefile, -uf
                        Define if input file is for usernames
  --output, -o OUTPUT   Specify a file to save results to as a text file.
  --json, -j JSON       Specify a file to save results to as a json file.
```

------

### Lookup via domain and get emails:

```bash
venv/bin/python3 main.py -d tesla.com -ge
```

```bash
venv/bin/python3 main.py -d tesla.com -ge -o test-tesla.txt
```

------

### Lookup email:

```bash
venv/bin/python3 main.py -e jorth@tesla.com
```

```bash
venv/bin/python3 main.py -e jorth@tesla.com -ge -o test-email.txt
```

------

### Lookup username:

```bash
venv/bin/python3 main.py -u whatever
```

------

I added saving to a json file and also added various other options. For commands without `-ge` or `--getemails`, it throws an error that it must be `-j` or `--json`, but this is mostly because the raw output without any kind of filtering, is json so I thought it was appropiate to do this.

