#!/usr/bin/env python

# csv2reader.py - given a specifically shaped CSV file, cache content suitable for the Reader

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# August  27, 2022 - first cut; in my flat in Lyon
# October  3, 2022 - tweaking to limit downloads and not repeat work
# October 24, 2022 - added EXPORT


# configure
METADATA  = 'metadata.csv'
EXTENSION = '.pdf'
COLUMNS   = [ 'file', 'author', 'title', 'date' ]
THROTTLE  = 4
LIMIT     = 9999
REPLACE   = 'export.arxiv.org'
FIND      = 'arxiv.org'

# require
from pathlib  import Path
from time     import sleep
import pandas as pd
import re
import string
import sys
import requests

# get input
if len( sys.argv ) != 3 : sys.exit( 'Usage: ' + sys.argv[ 0 ] + " <csv> <directory>" )
file      = sys.argv[ 1 ]
directory = sys.argv[ 2 ]

# read and process each row in the given CSV file
metadata  = pd.read_csv( file )
size      = len( metadata )    
rows      = []
directory = Path( directory )
for index, row in metadata.iterrows() :

	# parse
	id     = str( row[ 'id' ] )
	author = row[ 'author' ]
	title  = row[ 'title' ]
	date   = row[ 'date' ]
	url    = row[ 'pdf' ]
	
	# update the url
	url = url.replace( FIND, REPLACE )
	
	# debug
	sys.stderr.write( "Getting item #%s of %s (%s) \r" % ( str( index + 1 ), str( size ), url ) )
	
	# create a file name and check to see if we've already been here
	file = re.sub( '[^\w\s]', '-', id ) + EXTENSION
	if not ( directory/file ).exists() : 
	
		# get and check a response
		sleep( THROTTLE )
		response = requests.get( url )
		status   = str( response.status_code )
		if response.status_code == 200 :
			
			# save the content
			with open( directory/file, "wb" ) as handle : handle.write( response.content )

		# error
		else :
		
			# debug and continue
			sys.stderr.write( "\nSomething went wrong. HTTP error code: %s\n" % status )
			continue
	
	# update the metadata
	rows.append( [ file, author, title, date ] )
	
	if index > LIMIT : break
	
# create/save metadata file
metadata  = pd.DataFrame( rows, columns=COLUMNS  )
metadata.to_csv( directory/METADATA, index=False )

# done
exit()