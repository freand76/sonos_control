#!/bin/bash

cp sonos_control.service /lib/systemd/system/.
systemctl daemon-reload
systemctl enable sonos_control.service
systemctl start sonos_control.service
