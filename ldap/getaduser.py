#!/usr/bin/env python3

import sys
import os
import json
import getpass
import ldap3
from ldap3 import Server, Connection, ObjectDef, AttrDef, Reader, Writer, ALL, core

configfile = "getaduser.json"			
default_password = "default - will be prompted"

def get_config():
    myfile = os.path.dirname(os.path.realpath(__file__)) + '/' + configfile
    try:
        with open(myfile) as f:
            conf = json.load(f)
        return conf
    except Exception as e:
        print("Could not open config file ' ", myfile, "':", repr(e))
        return False

def errorout(msg):
    print("ERROR:", msg)
    sys.exit(1)

def ldap_connect(server, user, pw):
    try:
        conn = Connection(server, user, pw, auto_bind=True)
    except core.exceptions.LDAPBindError as e:
        print("LDAP connect error: " + str(e))
        sys.exit(1)
    return conn

def ldap_search(conn, base, filter, attr):
    try:
        conn.search(base, filter, attributes=attr)
    except Exception as e:
        errorout("ldap_search error: " + repr(e))
    return conn
    
def query_user(conn, username, base, attr, want_json):
    filter = "(&(objectClass=user)(sAMAccountName=" + username + ")(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"
    #filter = "(&(objectclass=user)(sAMAccountName=" + username + "))"
    conn = ldap_search(conn, base, filter, attr)
    if want_json:
        response = json.loads(conn.response_to_json())
        print(json.dumps(response, indent=4, sort_keys=True))
    else:
        for entry in conn.entries:
            print(entry)


if __name__ == '__main__':
    conf = get_config()
    for k in [ 'adserver', 'adserverport', 'use_ssl', 'bind_user', 'search_base', 'verbose', 'want_json' ]:
        if k in conf.keys():
            exec(k+"=conf[k]")	# define vars 'adserver' etc
        else:
            errorout("you need to define '" + k + "'")

    if 'bind_password' in conf.keys() and conf['bind_password'] != default_password:
        bind_password = conf['bind_password']
    else:
        bind_password = getpass.getpass(prompt="Password for user '" + bind_user + "': ")

    if 'attributes' in conf.keys():
        attributes = conf['attributes']
    else:
        attributes = [ 'displayName' ]
    if verbose:
        attributes = ldap3.ALL_ATTRIBUTES

    server = Server(adserver, port=adserverport, use_ssl=use_ssl)
    connection = ldap_connect(server, bind_user, bind_password)
    
    if len(sys.argv) > 1:
        for u in sys.argv:
            query_user(connection, u, search_base, attributes, want_json)
    else:
        print("Abort with ctrl-c...")
        while True:
            try:
                username = input("Username: ")
            except:
                sys.exit(0)
            query_user(connection, username, search_base, attributes, want_json)

