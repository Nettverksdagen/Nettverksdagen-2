#!/bin/bash

backdir="../backups/$(date --rfc-3339='seconds' | sed 's/\ /_/g')"
mkdir -p $backdir
cp -r fileserver/uploads $backdir
cp -r ghost/data $backdir
docker exec -t postgres pg_dumpall -c -U postgres > "$backdir/api_db.sql"
