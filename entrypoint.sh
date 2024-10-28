#!/bin/bash

cat > /etc/stunnel/stunnel.conf <<EOF
debug = ${DEBUG:-5}
foreground = yes
setgid = stunnel
setuid = stunnel
socket = l:TCP_NODELAY=1
socket = r:TCP_NODELAY=1
syslog = no

[default]
client = ${CLIENT:-no}
accept = ${ACCEPT}
connect = ${CONNECT}

cert = ${CERT:-/etc/stunnel/certs/cert.pem}
key = ${KEY:-/etc/stunnel/certs/key.pem}

EOF

exec stunnel "$@"
