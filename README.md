# Snusbase Lookup:

This is just a script I wrote to lookup domains and emails using the snusbase api. Currently I only need domain and email, but plan on adding more features as I need to for my osint and other projects.

NOTE: I need to do better error handling so some stuff is broken and I haven't gotten around to fixing it.

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
usage: main.py [-h] [--email EMAIL] [--domain DOMAIN] [--getemails | --no-getemails | -ge] [--input INPUT]
               [--domainfile | --no-domainfile | -df] [--emailfile | --no-emailfile | -ef] [--output OUTPUT]

Simple python3 program to check if an email is associated with any of the import online account modules.

options:
  -h, --help            show this help message and exit
  --email, -e EMAIL     Email to check.
  --domain, -d DOMAIN   Domain to check
  --getemails, --no-getemails, -ge
                        Extract emails from results
  --input, -i INPUT     File with emails or domains, one on each line.
  --domainfile, --no-domainfile, -df
                        Define if input file is for domains
  --emailfile, --no-emailfile, -ef
                        Define if input file is for emails
  --output, -o OUTPUT   Specify a file to save results to.
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
