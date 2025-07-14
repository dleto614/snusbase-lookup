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
            # print(line)
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

    # Search Snusbase
    search_response = send_request('data/search', {
        'terms': [domain],
        'types': ["_domain"],  # can be username, email, lastip, hash, password and/or name, and _domain
        'wildcard': False,
    })
             
    return search_response

def search_usernames(username):

    # Search Snusbase
    search_response = send_request('data/search', {
        'terms': [username],
        'types': ["username"],  # can be username, email, lastip, hash, password and/or name, and _domain
        'wildcard': False,
    })
             
    return search_response

def search_emails(email):

    # Search Snusbase
    search_response = send_request('data/search', {
        'terms': [email],
        'types': ["email"],  # can be username, email, lastip, hash, password and/or name, and _domain
        'wildcard': False,
    })
             
    return search_response

def args_write_all_file(search_response, lookup, args):
    if args.json is not None:
        if len(search_response["results"]) != 0:
            print("Writing results to json file {}".format(args.json))

            with open(args.json, mode="a") as fd:
                data = {"lookup": lookup, "results": search_response["results"]}
                fd.write(json.dumps(data, indent=4) + "\n")

def args_write_file(search_response, emails, lookup, args):
    if args.output is not None:
        if len(search_response["results"]) != 0 or len(emails) != 0:
                    print("Writing results to file {}".format(args.output))
                    
                    if len(emails) != 0:
                        final_emails = remove_duplicates(emails)
                        #print(final_emails)

                        with open(args.output, mode="a") as email_fd:
                            email_fd.write("\n".join(final_emails) + "\n")

    elif args.json is not None:
        if len(search_response["results"]) != 0 or len(emails) != 0:
            print("Writing results to json file {}".format(args.json))
            
            if len(emails) != 0:
                final_emails = remove_duplicates(emails)

                data = {"domain": lookup, "emails": final_emails} # Build the json object

                with open(args.json, mode="a") as email_fd:
                    email_fd.write(json.dumps(data, indent=4) + "\n")

def check_output(search_response, request, args):
    if args.getemails == True:
        emails = get_email(search_response)
    else:
        emails = None
        print(search_response)

    if args.output and emails is not None:
        args_write_file(search_response, emails, request, args)
    elif args.json and emails is not None:
        args_write_file(search_response, emails, request, args)
    elif emails is not None:
        final_emails = remove_duplicates(emails)
    elif args.json is not None and args.getemails == False:
        args_write_all_file(search_response, request, args)

    print("Sleeping")
    time.sleep(1)

def check_output_args(args):
    if args.output is not None and args.getemails == False:
                print("Output is in json so please use the '--json' or '-j' flag to write the results to a file")
                sys.exit(1)

def main():

    # ...
    # Santa Clause is coming to town
    
    # He’s making a list,
    # Checking it twice,
    # Gonna find out who’s naughty or nice.
    # Santa Claus is coming to town

    chk_emails = list()
    chk_domains = list()
    chk_usernames = list()

    email_buff = list()

    # TODO: Add username and ip options. Also can add name as well.

    # Added username. Will get to lastip later.

    parser=argparse.ArgumentParser(description="Simple python3 program to check if an email is associated with any of the import online account modules.")
    
    parser.add_argument("--email", "-e", help="Email to check.", type=str)
    parser.add_argument("--domain", "-d", help="Domain to check", type=str)
    parser.add_argument("--username", "-u", help="Username to check", type=str)
    
    parser.add_argument("--getemails", "-ge", help="Extract emails from results", default=False, action=argparse.BooleanOptionalAction)
    
    parser.add_argument("--input", "-i", help="File with emails or domains, one on each line.", type=str)
    parser.add_argument("--domainfile", "-df", help="Define if input file is for domains", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--emailfile", "-ef", help="Define if input file is for emails", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--usernamefile", "-uf", help="Define if input file is for usernames", default=False, action=argparse.BooleanOptionalAction)

    parser.add_argument("--output", "-o", help="Specify a file to save results to as a text file.", type=str)
    parser.add_argument("--json", "-j", help="Specify a file to save results to as a json file.", type=str)

    args=parser.parse_args()

    # if-elif-else goes brrrrrrrrrrrrr
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
    elif args.username is not None:
        chk_usernames.append(args.username)
    elif args.input is not None and args.usernamefile == True:
        usernames = read_file(args.input)
        
        for username in usernames:
            chk_usernames.append(username.strip())
    else:
        parser.print_help()
        sys.exit(1)
        
    
    if chk_domains is not None:
        for domain in chk_domains:

            check_output_args(args)

            print("Checking domain: {}".format(domain))
            search_response = search_domains(domain)

            check_output(search_response, domain, args)

    if chk_emails is not None:
        for email in chk_emails:
            
            check_output_args(args)

            print("Checking email: {}".format(email))
            search_response = search_emails(email)

            check_output(search_response, email, args)

    if chk_usernames is not None:
        for username in chk_usernames:

            check_output_args(args)

            print("Checking username: {}".format(username))
            search_response = search_usernames(username)

            check_output(search_response, username, args)

# TODO: Add more options to filter out like usernames, passwords, hashes, etc
# TODO: Add more options to search like usernames, passwords, hashes, etc

# Added usernames. Will get to passwords and hashes later.

# Still lots of stuff to add, but this has worked for what I needed at the time.

main()
