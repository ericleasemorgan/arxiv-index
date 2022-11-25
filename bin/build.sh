#!/usr/bin/env bash

# build.sh - one script to rule them all

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# August 26, 2022 - first cut; on the plane to Lyon


# fill the database
echo "Step #1 of 2: Reading JSON and filling database" >&2
./bin/json2db.sh

# index it
echo "Step #2 of 2: Indexing" >&2
./bin/index.sh

# done
exit
