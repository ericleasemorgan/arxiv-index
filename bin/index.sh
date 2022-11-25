#!/usr/bin/env bash

# index.sh- create full text index of a configured database

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# August 26, 2022 - first cut; while waiting for my flight to Lyon


# configure
DB='./etc/arxiv.db'
DROPINDX='DROP TABLE IF EXISTS indx;'
CREATEINDX='CREATE VIRTUAL TABLE indx USING FTS5( id, author, submitter, title, date, abstract, comments, journal, doi, report, license, category, landingPage, pdf );'
INDEX='INSERT INTO indx SELECT b.id, b.author, b.submitter, b.title, b.date, b.abstract, b.comments, b.journal, b.doi, b.report, b.license, GROUP_CONCAT( c.category, "; " ), b.landingPage, b.pdf FROM bibliographics as b, categories as c where b.id is c.id GROUP BY c.id;';

# index; do the actual work
echo $DROPINDX   | sqlite3 $DB
echo $CREATEINDX | sqlite3 $DB
echo $INDEX      | sqlite3 $DB
exit
