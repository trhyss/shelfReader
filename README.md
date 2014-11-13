shelfReader
===========

shelfReader is an application that helps speed-up and reduce errors with shelf reading.  It is written in Python3 and uses an SQLite database.  This software was designed to work with ExLibris Aleph.

To use sheflReader, you must export items records and create a database with two columns titled, 'barcode' and 'call'.  I use SQL Devleoper to export the records and then the SQLite manager addon in Firefox to create/ manage the database.

How shelfReader works:
  Scan the bar code of the first itme you wish to shelf read.
  With this bar code, shelfReader queries the database and retrieves the corresponding call number.
  The call number is parsed and made comparable to another call number.
  Scan the next itme.
  ShelfReader again queries the database and retrieve the corresponding call number.
  This call number is parsed.
  The two parsed call numbers are compared and shelfReader returns an audible response depending on whter the two items    are shleved correctly with regard to each other.
  Continue scanning bar codes.
  Each scanned barcode will queried, the corresponding call number parsed, and compared with the previous call number.
