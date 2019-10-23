vpn-exec: vpn-exec.c
	gcc -Werror -Wall -Wextra -pedantic $< -o $@

install:
	install -t /usr/local/bin/ vpn-exec
	chmod u+s /usr/local/bin/vpn-exec
