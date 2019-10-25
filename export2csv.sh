#!/usr/bin/env bash

sqlite3 -header -csv /mnt/NAS_QData/Stas/omnik.sqlite "select * from minutes;" > solar.csv
