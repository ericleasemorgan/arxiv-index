#!/usr/bin/env bash

# json2db.sh - create and fill a database

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# August 26, 2022 - first cut; in the airport on my way to Lyon


# configure
DB='./etc/arxiv.db'
SCHEMA='./etc/schema.sql'
JSON2SQL='./bin/json2sql.py'
TRANSACTION='./tmp/transaction.sql'

# re-initialize
rm -rf $DB
cat $SCHEMA | sqlite3 $DB

# create a transaction
echo "BEGIN TRANSACTION;" >  $TRANSACTION
$JSON2SQL                 >> $TRANSACTION
echo "END TRANSACTION;"   >> $TRANSACTION

# do the work and done
cat $TRANSACTION | sqlite3 $DB
exit
