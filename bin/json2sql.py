#!/usr/bin/env python

# json2sql.py - given a configured JSON file, output a stream of SQL insert statements

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# August 26, 2022 - first investigations; at the airport on the way to Lyon!


# configure
JSON           = './etc/snapshot.json'
MAXIMUM        = 1000
BIBLIOGRAPHICS = "INSERT INTO bibliographics ( 'author', 'landingPage', 'pdf', 'report', 'license', 'comments', 'journal', 'doi', 'id', 'submitter', 'title', 'abstract', 'date' ) VALUES ( '##AUTHOR##', '##LANDINGPAGE##', '##PDF##', '##REPORT##', '##LICENSE##', '##COMMENTS##', '##JOURNAL##', '##DOI##', '##ID##', '##SUBMITTER##', '##TITLE##', '##ABSTRACT##', '##DATE##' );"
CATEGORIES     = "INSERT INTO categories ( 'id', 'category' ) VALUES ( '##ID##', '##CATEGORY##' );"
AUTHORS        = "INSERT INTO authors ( 'id', 'firstName', 'lastName' ) VALUES ( '##ID##', '##FIRSTNAME##', '##LASTNAME##' );"
LANDINGPAGE    = 'https://arxiv.org/abs/##ID##'
PDF            = 'https://export.arxiv.org/pdf/##ID##'

# require
import json
import sys
import re

# open the data file
with open( JSON ) as handle :

	# process each record (line)
	for index, record in enumerate( handle ) : 
	
		# parse
		record        = json.loads( record )
		id            = record[ 'id' ]
		submitter     = '' if record[ 'submitter' ]   is None else record[ 'submitter' ]
		authors       = record[ 'authors' ]
		title         = record[ 'title' ]
		comments      = '' if record[ 'comments' ]    is None else record[ 'comments' ]
		journal       = '' if record[ 'journal-ref' ] is None else record[ 'journal-ref' ]
		doi           = '' if record[ 'doi' ]         is None else record[ 'doi' ]
		report        = '' if record[ 'report-no' ]   is None else record[ 'report-no' ]
		categories    = record[ 'categories' ]
		license       = '' if record[ 'license' ]     is None else record[ 'license' ]
		abstract      = record[ 'abstract' ]
		versions      = record[ 'versions' ]
		date          = record[ 'update_date' ]
		authorsParsed = record[ 'authors_parsed']
		
		# normalize
		abstract  = abstract.replace( '\n', ' ' )
		abstract  = re.sub( ' +', ' ', abstract )
		abstract  = abstract.replace( "'", "''" )
		abstract  = re.sub( '^ +', '', abstract )
		authors   = authors.replace( '\n', ' ' )
		authors   = authors.replace( "'", "''" )
		comments  = comments.replace( '\n', ' ' )
		comments  = comments.replace( "'", "''" )
		comments  = re.sub( ' +', ' ', comments )
		journal   = journal.replace( '\n', ' ' )
		journal   = journal.replace( "'", "''" )
		report    = report.replace( '\n', ' ' )
		report    = report.replace( "'", "''" )
		submitter = submitter.replace( "'", "''" )
		title     = re.sub( ' +', ' ', title )
		title     = title.replace( '\n', ' ' )
		title     = title.replace( "'", "''" )
		
		# debug
		sys.stderr.write( str( index ) + '\r' )
		#sys.stderr.write( '          id: ' + id + '\n')
		#sys.stderr.write( '   submitter: ' + submitter + '\n')
		#sys.stderr.write( '     authors: ' + authors + '\n')
		#sys.stderr.write( '       title: ' + title + '\n')
		#sys.stderr.write( '    comments: ' + comments + '\n')
		#sys.stderr.write( '     journal: ' + journal + '\n')
		#sys.stderr.write( '         doi: ' + doi + '\n')
		#sys.stderr.write( '      report: ' + report + '\n')
		#sys.stderr.write( '  categories: ' + str( categories ) + '\n')
		#sys.stderr.write( '     license: ' + license + '\n')
		#sys.stderr.write( '   abastract: ' + abstract + '\n')
		#sys.stderr.write( '    versions: ' + str( versions ) + '\n')
		#sys.stderr.write( '        date: ' + date + '\n')
		#sys.stderr.write( '     authors: ' + str( authorsParsed ) + '\n')
		#sys.stderr.write( '\n\n')
		
		
		# bibliographics; substitute and output
		sql = BIBLIOGRAPHICS.replace( '##ID##', id )
		sql = sql.replace( '##TITLE##', title )
		sql = sql.replace( '##SUBMITTER##', submitter )
		sql = sql.replace( '##ABSTRACT##', abstract )
		sql = sql.replace( '##DATE##', date )
		sql = sql.replace( '##COMMENTS##', comments )
		sql = sql.replace( '##JOURNAL##', journal )
		sql = sql.replace( '##DOI##', doi )
		sql = sql.replace( '##REPORT##', report )
		sql = sql.replace( '##LICENSE##', license )
		sql = sql.replace( '##LANDINGPAGE##', LANDINGPAGE.replace( '##ID##', id ) )
		sql = sql.replace( '##PDF##', PDF.replace( '##ID##', id ) )
		sql = sql.replace( '##AUTHOR##', authors )
		print( sql )
		
		# process each category
		categories = categories.split( ' ' )
		for category in categories : 
		
			# substitute and output
			sql = CATEGORIES.replace( '##ID##', id )
			sql = sql.replace( '##CATEGORY##', category )
			print( sql )
		
		# process each author
		for author in authorsParsed :
		
			# parse
			firstName = author[ 1 ]
			lastName  = author[ 0 ]

			# normalize
			firstName = firstName.replace( "'", "''" )
			lastName  = lastName.replace( "'", "''" )
			
			# substitute and output
			sql = AUTHORS.replace( '##ID##', id )
			sql = sql.replace( '##FIRSTNAME##', firstName )
			sql = sql.replace( '##LASTNAME##', lastName )
			print( sql )

		# break, conditionally
		#if index > MAXIMUM : break
		
# done
exit()
