#! /usr/bin/python3
#add comment to check Gitub
'''ShelfReader is an application that partially automates the process of
shelf reading.
Copyright (C) 2015  Parker O'Mara (pomar001@plattsburgh.edu)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import sqlite3
import winsound
import time
import datetime
import sys

def main():  

    barcode = eval(input ("Scan the first barcode: "))
    if barcode:
        startTime= time.time()
        count=1
    complete_call= call_grabber(barcode)
    call, description = complete_call
    call= call+' '+description
    while not call:
        not_found()
        barcode = eval(input ("Scan the first barcode: "))
        complete_call= call_grabber(barcode)
        call, description = complete_call
        call= call+' '+description
    parse_call= call_parser(call)
    second_last_call= ('','','','','','','','','')   

    while parse_call:
        next_barcode = eval(input("Scan the next barcode: "))
        count= count+1
        bookCount=count-1
        if next_barcode == 1:
            logger(bookCount,startTime,next_barcode)
        next_complete_call = call_grabber(next_barcode)
        next_call, next_description= next_complete_call
        next_call = next_call + ' ' + next_description
        while not next_call:
            not_found()
            next_barcode = eval(input("Scan the next barcode: "))
            next_complete_call = call_grabber(next_barcode)
            next_call, next_description = next_complete_call
            next_call= next_call + ' '+ next_description
        parse_next_call = call_parser(next_call)
        comparer(parse_call, parse_next_call, second_last_call)
        second_last_call= parse_call
        parse_call = parse_next_call
    
# call_grabber, using the barcode, queries the database and returns
# the call number and description.
def call_grabber(barcode):
    description=''
    conn = sqlite3.connect('gcCatalog.sqlite')
    try:
        c = conn.cursor()

        try:
            c.execute("select call, description from items where barcode = ?", (barcode,))

            row = c.fetchone()
            if row:
                call = row[0]
                description= row[1]
            else:
                call = None

        finally:
            c.close()

    finally:
        conn.close()
    
    return call, description

# call_parser splits up the call number into 'comparable' pieces.
def call_parser(call):
    call= call.rstrip()
    call= call.replace('0','',1)
    call= call.replace(' ','',1)
    call_div, call= splitter(call)
        
    subject, cutter= call.split(' ',1)
    addl1= ('')
    addl2= ('')
    addl3= ('')
    addl4= ('')
    addl5= ('')
    addla= ('')
    addlb= ('')
    addlc= ('')
    addld= ('')
    if ' ' in cutter:
        cutter, addla = cutter.split(' ',1)
    else:
        cutter= cutter
    if ' ' in addla:
        addl1, addlb = addla.split(' ',1)
    else:
        addl1= addla
    if ' ' in addlb:
        addl2, addlc = addlb.split(' ', 1)
    else:
        addl2= addlb
    if ' ' in addlc:
        addl3, addld = addlc.split(' ',1)
    else:
        addl3 = addlc
    if ' ' in addld:
        addl4, addl5 = addld.split(' ',1)
    else:
        addl4= addld
    if addl1== 'v.' or addl1=='vol.':
        add1= 'vol'
    if addl2== 'v.' or addl2=='vol.':
        addl2= 'vol'
    if addl3== 'v.' or addl3=='vol.':
        addl3= 'vol'
    if addl4== 'v.' or addl4=='vol.':
        addl4= 'vol'
    if addl1== 'c.':
        add1= 'copy'
    if addl2== 'c.':
        addl2= 'copy'
    if addl3== 'c.':
        addl3= 'copy'
    if addl4== 'c.':
        addl4= 'copy'
    cutteralpha= cutter[0]
    cutternum= cutter[1:]
    cutternum= '.'+ cutternum
    return call_div, subject, cutteralpha, cutternum, addl1, addl2, addl3, addl4, addl5

# splitter separates the division from the call number.
def splitter(call):
    if '#' in call:
            call=call.replace('#','@',1)
            call_div, call = call.split('@')
    elif '!' in call:
        call=call.replace('!','@', 1)
        call_div, call = call.split('@')
    elif '"' in call:
        call=call.replace('"','@',1)
        call_div, call = call.split('@')
    elif '!' and '#' and '"' not in call:
        while True:
            if call[1] in '0123456789 ':
                call_div= call[0:1]
                call = call[1:]
                if call[0] == ' ':
                    call= call.replace(' ','',1)
                break
            if call[2] in '0123456789 ':
                call_div= call[0:2]
                call = call[2:]
                if call[0] == ' ':
                    call= call.replace(' ','',1)
                break
            if call[3] in '0123456789 ':
                call_div= call[0:3]
                call = call[3:]
                if call[0] == ' ':
                    call= call.replace(' ','',1)

    return call_div, call

# logger logs how many books shelf-read and shelf-reading rate per hour.
def logger(bookCount,startTime,next_barcode):
    log= open("log.txt", "a")
    datetimeStamp=datetime.datetime.now()
    format= "%a %b %d %H:%M:%S %Y"
    timestamp= datetimeStamp.strftime(format)
    finishTime= time.time()
    elapsedTime= finishTime - startTime
    rate=(bookCount/int(elapsedTime))*3600
    print(timestamp, file=log)
    print('count: ',bookCount, file=log)
    if int(elapsedTime) < 60:
        print ('Total time: ',int(elapsedTime),' seconds',file=log)
    if 3600 > int(elapsedTime) >= 60:
        minutes= int(elapsedTime)//60
        seconds= int(elapsedTime)%60
        print ('Total time: ',minutes,':',seconds,' (min:sec)', file=log)
    if int(elapsedTime)>= 3600:
        hours = int(elapsedTime)//3600
        minutes= int(elapsedTime)//60
        seconds= int(elapsedTime)%60
        print('Total time: ',hours,':',minutes,':',seconds,' (hr:min:sec)', file=log)
    print('books per hour: ',int(rate),'\n', file=log)
    log.close()
    sys.exit()

# comparer unpacks all the variables and compares each piece.
def comparer(call, next_call, second_last_call):
    div,subject,cutteralpha,cutternum,addl1,addl2,addl3,addl4, addl5 = call
    (next_div,next_subject,next_cutteralpha, next_cutternum, next_addl1,
    next_addl2, next_addl3, next_addl4, next_addl5) = next_call
    (second_last_div,second_last_subject,second_last_cutteralpha,
    second_last_cutternum, second_last_addl1, second_last_addl2,
    second_last_addl3, second_last_addl4, second_last_addl5) = second_last_call
    if next_div < div:
        if second_last_div<next_div<div:
            prev_misshelved(call)
        else:
            misshelved(next_call)
    if next_div > div:
        correct(next_call)
    if next_div == div:
        if float(next_subject) < float(subject):
            if second_last_subject != '':
                if float(second_last_subject)<float(next_subject)<float(subject):
                    prev_misshelved(call)
                else:
                    misshelved(next_call)
            else:
                misshelved(next_call)
        if float(next_subject) > float(subject):
            correct(next_call)
        if float(next_subject) == float(subject):
            if next_cutteralpha < cutteralpha:
                if second_last_cutteralpha<next_cutteralpha<cutteralpha:
                    prev_misshelved(call)
                else:
                    misshelved(next_call)
            if next_cutteralpha > cutteralpha:
                correct(next_call)
            if next_cutteralpha == cutteralpha:
                if next_cutternum<cutternum:
                    if second_last_cutternum<next_cutternum<cutternum:
                        prev_misshelved(call)
                    else:
                        misshelved(next_call)
                if next_cutternum>cutternum:
                    correct(next_call)
                if next_cutternum== cutternum:
                    if addl1 == '' and next_addl1 == '':
                        identical()
                    if addl1 == '' and next_addl1 != '':
                        correct(next_call)
                    if addl1 != '' and next_addl1 == '':
                        misshelved(next_call)
                    if addl1 != '' and next_addl1 != '':
                        if next_addl1 < addl1:
                            if second_last_addl1 < next_addl1 < addl1:
                                prev_misshelved(call)
                            else:
                                misshelved(next_call)
                        if next_addl1 > addl1:
                            correct(next_call)
                        if next_addl1 == addl1:
                            if addl1 == 'vol':
                                if int(next_addl2) < int(addl2):
                                    if int(second_last_addl2) < int(next_addl2) < int(addl2):
                                        prev_misshelved(call)
                                    else:
                                        misshelved(next_call)
                                if int(next_addl2) > int(addl2):
                                    correct(next_call)
                            else:
                                if addl2 == '' and next_addl2 == '':
                                    identical()
                                if addl2 == '' and next_addl2 != '':
                                    correct(next_call)
                                if addl2 != '' and next_addl2 == '':
                                    misshelved(next_call)
                                if addl2 != '' and next_addl2 != '':
                                    if next_addl2 < addl2:
                                        if second_last_addl2 < next_addl2 < addl2:
                                            prev_misshelved(call)
                                        else:
                                            misshelved(next_call)
                                    if next_addl2 > addl2:
                                        correct(next_call)
                                    if next_addl2 == addl2:
                                        if addl2 == 'vol':
                                            if int(next_addl3) < int(addl3):
                                                if int(second_last_addl3) < int(next_addl3) < int(addl3):
                                                    prev_misshelved(call)
                                                else:
                                                    misshelved(next_call)
                                            if int(next_addl3) > int(addl3):
                                                correct(next_call)
                                        else:
                                            if addl3 == '' and next_addl3 == '':
                                                identical()
                                            if addl3 == '' and next_addl3 != '':
                                                correct(next_call)
                                            if addl3 != '' and next_addl3 == '':
                                                misshelved(next_call)
                                            if addl3 != '' and next_addl3 != '':
                                                if next_addl3 < addl3:
                                                    if second_last_addl3 < next_addl3 < addl3:
                                                        prev_misshelved(call)
                                                    else:
                                                        misshelved(next_call)
                                                if next_addl3 > addl3:
                                                    correct(next_call)
                                                if next_addl3 == addl3:
                                                    if addl3 == 'vol':
                                                        if int(next_addl4) < int(addl4):
                                                            if int(second_last_addl4) < int(next_addl4) < int(addl4):
                                                                prev_misshelved(call)
                                                            else:
                                                                misshelved(next_call)
                                                        if int(next_addl4) > int(addl4):
                                                            correct(next_call)
                                                    else:
                                                        if addl4 == '' and next_addl4 == '':
                                                            identical()
                                                        if addl4 == '' and next_addl4 != '':
                                                            correct(next_call)
                                                        if addl4 != '' and next_addl4 == '':
                                                            misshelved(next_call)
                                                        if addl4 != '' and next_addl4 != '':
                                                            if next_addl4 < addl4:
                                                                if second_last_addl4 < next_addl4 < addl4:
                                                                    prev_misshelved(call)
                                                                else:
                                                                    misshelved(next_call)
                                                            if next_addl4 > addl4:
                                                                correct(next_call)
                                                            if next_addl4 == addl4:
                                                                if addl4 == 'vol':
                                                                    if int(next_addl5) < int(addl5):
                                                                        if int(second_last_addl5) < int(next_addl5) < int(addl5):
                                                                            prev_misshelved(call)
                                                                        else:
                                                                            misshelved(next_call)
                                                                    if int(next_addl5) > int(addl5):
                                                                        correct(next_call)
                                                                else:
                                                                    if addl5 == '' and next_addl5 == '':
                                                                        identical()
                                                                    if addl5 == '' and next_addl5 != '':
                                                                        correct(next_call)
                                                                    if addl5 != '' and next_addl5 == '':
                                                                        misshelved(next_call)
                                                                    if addl5 != '' and next_addl5 != '':
                                                                        if next_addl5 < addl5:
                                                                            if second_last_addl5 < next_addl5 < addl5:
                                                                                prev_misshelved(call)
                                                                            else:
                                                                                misshelved(next_call)
                                                                        if next_addl5 > addl5:
                                                                            correct(next_call)
                                                                        else:
                                                                            identical()
                                        



                                                            
# Audio and text output messages.
def correct(next_call):
    Freq = 2093
    Dur = 400
    winsound.Beep(Freq,Dur)
    print (next_call,' is shelved correctly.')

def misshelved(next_call):
    Freq = 523
    Dur = 400
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq,Dur)
    print (next_call,' is misshelved.')

def identical():
    Freq = 1046
    Dur = 400
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq,Dur)
    print ('The call numbers are identical.')

def prev_misshelved(call):
    Freq = 523
    Freq2= 1046
    Dur = 400
    winsound.Beep(Freq2,Dur)
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq2,Dur)
    winsound.Beep(Freq, Dur)
    print('The previous book, ',call,', is misshelved.')

def not_found():
    Freq = 523
    Dur = 1200
    winsound.Beep(Freq,Dur)
    print ('Barcode not found in database.')
    
main()
