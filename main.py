#!/usr/bin/env python3

from requests.auth import HTTPBasicAuth
import requests
import argparse
import time
import json
import sys

snusbase_auth = "API_KEY"
snusbase_api = "https://api.snusbase.com/"

def read_file(file):
    try:
        # Read file using readlines
        fd = open(file, 'r')
        lines = fd.readlines()
 
        return lines
    except Exception as error:
        print("Error at read_file: {}".format(error))

def write_file(data, file):
    json_data =  json.dumps(data, indent=4)
    fd = open(file, "a")

    # This is dumb.
    fd.write(json_data+"\n")
    fd.close()

def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)

def get_email(data):
    output = []
    for i in item_generator(data, "email"):
        email = i
        output.append(email)

    return output

# Python code to remove duplicate elements
def remove_duplicates(data):
    results = []
    for line in data:
        if line not in results:
            print(line)
            results.append(line)
    return results

# Re-usable function for the Snusbase API
def send_request(url, body=None):
    headers = {
        'Auth': snusbase_auth,
        'Content-Type': 'application/json',
    }
    method = 'POST' if body else 'GET'
    data = json.dumps(body) if body else None
    response = requests.request(method, snusbase_api + url, headers=headers, data=data)
    return response.json()

def search_domains(domain):
    # TODO: Run emails in blocks with multiprocessing "threading". Will make it go faster.

    # Search Snusbase
    search_response = send_request('data/search', {
        'terms': [domain],
        'types': ["_domain"],  # can be username, email, lastip, hash, password and/or name, and _domain
        'wildcard': False,
    })
             
    return search_response

def args_write_file(search_response, emails, args):
     if len(search_response["results"]) != 0 or len(emails) != 0 and args.output is not None:
                print("Writing results to file {}".format(args.output))
                
                if len(emails) != 0:
                    final_emails = remove_duplicates(emails)
                    #print(final_emails)

                    with open(args.output, mode="a") as email_fd:
                        email_fd.write("\n".join(final_emails) + "\n")

def main():

    chk_emails = list()
    chk_domains = list()

    email_buff = list()

    # TODO: Add username and ip options. Also can add name as well.
    # TODO: Add arguments to define which kind of input file. True or False.
    # TODO: Add an argument to read file and see if the format (search-option:what-to-lookup).

    parser=argparse.ArgumentParser(description="Simple python3 program to check if an email is associated with any of the import online account modules.")
    parser.add_argument("--email", "-e", help="Email to check.", type=str)
    parser.add_argument("--domain", "-d", help="Domain to check", type=str)
    parser.add_argument("--getemails", "-ge", help="Extract emails from results", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--input", "-i", help="File with emails or domains, one on each line.", type=str)
    parser.add_argument("--domainfile", "-df", help="Define if input file is for domains", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--emailfile", "-ef", help="Define if input file is for emails", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--output", "-o", help="Specify a file to save results to.", type=str)
    args=parser.parse_args()

    if args.email is not None:
        chk_emails.append(args.email)
    elif args.input is not None and args.emailfile == True: 
        emails = read_file(args.input)
        
        for email in emails:
            chk_emails.append(email.strip())
    elif args.domain is not None:
        chk_domains.append(args.domain)

    elif args.input is not None and args.domainfile == True:
        domains = read_file(args.input)
        
        for domain in domains:
            chk_domains.append(domain.strip())
    else:
        parser.print_help()
        sys.exit(1)
        
    
    if chk_domains is not None:
        for domain in chk_domains:
            print("Checking domain: {}".format(domain))
            search_response = search_domains(domain)

            if args.getemails == True:
               emails = get_email(search_response)
            else:
                emails = None
                print(search_response)

            # TODO: Add a block to write just the json returned instead of filtering out just the emails

            if args.output and emails is not None:
                args_write_file(search_response, emails, args)
            elif emails is not None:
                final_emails = remove_duplicates(emails)

            print("Sleeping")
            time.sleep(1)

    if chk_emails is not None:
        for email in chk_emails:
            print("Checking email: {}".format(email))
            
            # TODO: Run emails in blocks with multiprocessing "threading". Will make it go faster.

            # Search Snusbase
            search_response = send_request('data/search', {
                        'terms': [email],
                        'types': ["email"],  # can be username, email, lastip, hash, password and/or name, and _domain
                        'wildcard': False,
             })

            if args.getemails == True:
               emails = get_email(search_response)
            else:
                emails = None
                print(search_response)

            if args.output and emails is not None:
                args_write_file(search_response, emails, args)
            elif emails is not None:
                final_emails = remove_duplicates(emails)

            print("Sleeping")
            time.sleep(1)                

# TODO: Add more options to filter out like usernames, passwords, hashes, etc
# TODO: Add more options to search like usernames, passwords, hashes, etc

# Still lots of stuff to add, but this has worked for what I needed at the time.

main()
