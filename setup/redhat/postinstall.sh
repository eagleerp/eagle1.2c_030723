#!/bin/sh

set -e

EAGLE_CONFIGURATION_DIR=/etc/eagle
EAGLE_CONFIGURATION_FILE=$EAGLE_CONFIGURATION_DIR/eagle.conf
EAGLE_DATA_DIR=/var/lib/eagle
EAGLE_GROUP="eagle"
EAGLE_LOG_DIR=/var/log/eagle
EAGLE_LOG_FILE=$EAGLE_LOG_DIR/eagle-server.log
EAGLE_USER="eagle"

if ! getent passwd | grep -q "^eagle:"; then
    groupadd $EAGLE_GROUP
    adduser --system --no-create-home $EAGLE_USER -g $EAGLE_GROUP
fi
# Register "$EAGLE_USER" as a postgres user with "Create DB" role attribute
su - postgres -c "createuser -d -R -S $EAGLE_USER" 2> /dev/null || true
# Configuration file
mkdir -p $EAGLE_CONFIGURATION_DIR
# can't copy debian config-file as addons_path is not the same
if [ ! -f $EAGLE_CONFIGURATION_FILE ]
then
    echo "[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = False
db_port = False
db_user = $EAGLE_USER
db_password = False
addons_path = /usr/lib/python3.6/site-packages/eagle/addons
" > $EAGLE_CONFIGURATION_FILE
    chown $EAGLE_USER:$EAGLE_GROUP $EAGLE_CONFIGURATION_FILE
    chmod 0640 $EAGLE_CONFIGURATION_FILE
fi
# Log
mkdir -p $EAGLE_LOG_DIR
chown $EAGLE_USER:$EAGLE_GROUP $EAGLE_LOG_DIR
chmod 0750 $EAGLE_LOG_DIR
# Data dir
mkdir -p $EAGLE_DATA_DIR
chown $EAGLE_USER:$EAGLE_GROUP $EAGLE_DATA_DIR

INIT_FILE=/lib/systemd/system/eagle.service
touch $INIT_FILE
chmod 0700 $INIT_FILE
cat << EOF > $INIT_FILE
[Unit]
Description=Eagle Open Source ERP and CRM
After=network.target

[Service]
Type=simple
User=eagle
Group=eagle
ExecStart=/usr/bin/eagle --config $EAGLE_CONFIGURATION_FILE --logfile $EAGLE_LOG_FILE
KillMode=mixed

[Install]
WantedBy=multi-user.target
EOF
