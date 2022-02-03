
Hack to query Active Directory server looking up username's.
Tried to make it a bit flexible with JSON config file.

	"want_json" - set to "1" to get JSON output

	"verbose"   - set to "1" will set the ldap3.ALL_ATTRIBUTES
	(see https://ldap3.readthedocs.io/en/latest/searches.html#attributes)

	"bind_password" - define at own risk, if not in config, qill query for password



Usage:

    a) interactive loop, no password defined

	$ ./getaduser.py 
	Password for user 'CN=Mike Smith,OU=Users,OU=Sweden,OU=_CORP,DC=example,DC=com': 
	Abort with ctrl-c...
	Username: 

    b) provide one or more usernames 

	$ ./getaduser.py user1 user2 user3


