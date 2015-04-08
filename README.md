shelfReader
===========

shelfReader is an application that helps speed-up and reduce errors with shelf reading.  It is written in Python3 and uses an SQLite database.  This software was designed to work with ExLibris Aleph v.20.

To use shelfReader, you must export items records and create a database (gcCatalog.slite) with three columns titled, 'barcode', 'call', and 'description'.

How shelfReader works:
  Scan the bar code of the first item you wish to shelf read.
  With this bar code, shelfReader queries the database and retrieves the corresponding call number.
  The call number is parsed and made comparable to another call number.
  Scan the next item.
  shelfReader again queries the database and retrieves the corresponding call number.
  This call number is parsed.
  The two parsed call numbers are compared and shelfReader returns an audible response depending on whether the two items    are shleved correctly with regard to each other.  The audible responses are as follows:
      1-beep   -- the books is shelved correctly;  
      2-beeps -- the book’s barcodes are identical;  
      3-beeps – the book is miss-shelved;  
      4-beeps (high, low, high, low)  -- the previous book is miss-shelved;  
      1 long beep  -- the barcode is not in the database

  Continue scanning bar codes.
  Each scanned barcode is queried, the corresponding call number parsed, and compared with the previous call number.
  To quit shelfReader, type a "1" into the "Scan next barcode:" field and press enter.
  A entry into a log file will be created upon quitting the program.  The log file contains date/time, number of books     scanned, and scan rate per hour.
