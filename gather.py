import json, sys, re

starting_year = 2015

faculty = [
    'Bagchi',
    'Bolnick',
    'Cooley',
    'Davis',
    'Diggle',
    'Elphick',
    'Fusco',
    'Goffinet',
    'Holsinger',
    'LewisL',
    'LewisP',
    'Schultz',
    'Schwenk',
    'Seemann',
    'Trumbo',
    'Urban',
    'Wegrzyn',
    'Yarish'
]

filepaths = {
    'Bagchi':    'Robert-Bagchi-final.json',
    'Bolnick':   'Daniel-Bolnick-final.json',
    'Cooley':    'John-Cooley-final.json',
    'Davis':     'Miranda-Davis-final.json',
    'Diggle':    'Pamela-Diggle-final.json',
    'Elphick':   'Chris-Elphick-final.json',
    'Fusco':     'Nicole-Fusco-final.json',
    'Goffinet':  'Bernard-Goffinet-final.json',
    'Holsinger': 'Kent-Holsinger-final.json',
    'LewisL':    'Louise-Lewis-final.json',
    'LewisP':    'Paul-Lewis-final.json',
    'Schultz':   'Eric-Schultz-final.json',
    'Schwenk':   'Kurt-Schwenk-final.json',
    'Seemann':   'Jeff-Seemann-final.json',
    'Trumbo':    'Stephen-Trumbo-final.json',
    'Urban':     'Mark-Urban-final.json',
    'Wegrzyn':   'Jill-Wegrzyn-final.json',
    'Yarish':    'Charles-Yarish-final.json'
}

def dumpException(exceptf, f, a, y, t, j, v, b, e, doi):
    exceptf.write('-------- %s ---------\n' % f)

    if a:
        exceptf.write('authors: %s\n' % a)
    else:
        exceptf.write('authors: MISSING\n')

    if y:
        exceptf.write('year: %s\n' % y)
    else:
        exceptf.write('year: MISSING\n')

    if t:
        exceptf.write('title: %s\n' % t)
    else:
        exceptf.write('title: MISSING\n')

    if j:
        exceptf.write('journal: %s\n' % j)
    else:
        exceptf.write('journal: MISSING\n')

    if v:
        exceptf.write('volume: %s\n' % v)
    else:
        exceptf.write('volume: MISSING\n')

    if b:
        exceptf.write('bpage: %s\n' % b)
    else:
        exceptf.write('bpage: MISSING\n')

    if e:
        exceptf.write('epage: %s\n' % e)
    else:
        exceptf.write('epage: MISSING\n')

    if doi:
        exceptf.write('https://doi.org/%s\n' % doi)
    else:
        exceptf.write('doi: MISSING\n')

exceptf = open('exceptions.txt', 'w')
nyearless = 0
nexceptions = 0
ninpress = 0
nchapters = 0
bibentries = []
for f in faculty:
    fn = '%s' % filepaths[f]
    print('Reading file "%s"...' % fn)
    stuff = open(fn, 'r').read()
    results = json.loads(stuff)
    for result in results:
        if not result['ignore']:
            # Capture information in r
            authors = result['authors']
            year    = result['year']
            title   = re.sub(r'\b_(.+?)_\b', r'<em>\1</em>', result['title'])
            journal = result['journal']
            volume  = result['volume']
            number  = result['number']
            try:
                booktitle      = result['booktitle']
                bookeditors    = result['bookeditors']
                bookpublisher  = result['bookpublisher']
                bookcity       = result['bookcity']
                bookisbn       = result['bookisbn']
            except KeyError:
                booktitle      = None
                bookeditors    = None
                bookpublisher  = None
                bookcity       = None
                bookisbn       = None
            bpage   = result['bpage']
            epage   = result['epage']
            article = result['article']
            doi     = result['doi']
            url     = result['url']
            citation_id = result['citation_id']
            
            # Construct bibliography string
            yearless = False
            exception = False
            inpress = False
            ischapter = False
            bib = ''
            if authors:
                bib += '%s' % authors
            if year:
                bib += ' %s.' % year
            else:
                yearless = True
            if title:
                bib += ' %s.' % title
            if journal and volume and bpage and epage:
                bib += ' %s %s:%s-%s.' % (journal, volume, bpage, epage)
            elif journal and volume and article:
                bib += ' %s %s:%s.' % (journal, volume, article)
            elif journal and volume == 'inpress':
                inpress = True
                bib += ' %s (in press).' % journal
            elif booktitle and bookeditors and bookpublisher and bookcity and bpage and epage:
                ischapter = True
                bib += ' pp. %s-%s in: %s, %s (eds.) %s, %s' % (bpage, epage, booktitle, bookeditors, bookpublisher, bookcity)
            elif booktitle and bookeditors and bookpublisher and bpage and epage:
                ischapter = True
                bib += ' pp. %s-%s in: %s, %s (eds.) %s' % (bpage, epage, booktitle, bookeditors, bookpublisher)
            elif booktitle and bookpublisher:
                ischapter = True
                bib += ' In: %s, %s' % (booktitle, bookpublisher)
            else:
                exception = True
            if doi:
                bib += ' DOI:%s.' % doi

            # Save in bibentries list
            if yearless:
                nyearless += 1
                dumpException(exceptf, f, authors, year, title, journal, volume, bpage, epage, doi)
            elif exception:
                nexceptions += 1
                dumpException(exceptf, f, authors, year, title, journal, volume, bpage, epage, doi)
            elif ischapter:
                nchapters += 1
                entry = (year, bib)
                bibentries.append(entry)
            else:
                entry = (year, bib)
                bibentries.append(entry)
            if inpress:
                ninpress += 1
                    
exceptf.close()

bibentries.sort()

gatherf = open('gathered.txt', 'w')
gatherf.write('\nSorted bibliographic entires:\n')
ngood = len(bibentries)
for b in bibentries:
    gatherf.write('%s\n' % b[1])
gatherf.close()

print('nyearless   = %d' % nyearless)
print('nexceptions = %d' % nexceptions)
print('ninpress    = %d' % ninpress)
print('nchapters   = %d' % nchapters)
print('ngood       = %d' % ngood)