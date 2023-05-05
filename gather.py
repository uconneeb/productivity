import json, sys, re, sys

starting_year = 2015

faculty = [
    'Anderson',
    'Bagchi',
    'Bolnick',
    'Bush',
    'Caira',
    'Chazdon',
    'Colwell',
    'Cooley',
    'Davis',
    'Diggle',
    'Elphick',
    'Fusco',
    'GarciaRobledo',
    'Goffinet',
    'Henry',
    'Herrick',
    'Holsinger',
    'Jockusch',
    'Jones',
    'Knutie',
    'LewisL',
    'LewisP',
    'Les',
    'Likens',
    'Schlichting',
    'Schultz',
    'Schwenk',
    'Seemann',
    'Silander',
    'Simon',
    'Tingley',
    'Trumbo',
    'Turchin',
    'Urban',
    'Wagner',
    'Wegrzyn',
    'Wells',
    'Willig',
    'Yarish',
    'Yuan'
]

filepaths = {
    'Anderson':      'Gregory-Anderson-final.json',
    'Bagchi':        'Robert-Bagchi-final.json',
    'Bolnick':       'Daniel-Bolnick-final.json',
    'Bush':          'Andrew-Bush-final.json',
    'Caira':         'Janine-Caira-final.json',
    'Chazdon':       'Robin-Chazdon-final.json',
    'Colwell':       'Rob-Colwell-final.json',
    'Cooley':        'John-Cooley-final.json',
    'Davis':         'Miranda-Davis-final.json',
    'Diggle':        'Pamela-Diggle-final.json',
    'Elphick':       'Chris-Elphick-final.json',
    'Fusco':         'Nicole-Fusco-final.json',
    'GarciaRobledo': 'Carlos-GarciaRobledo-final.json',
    'Goffinet':      'Bernard-Goffinet-final.json',
    'Henry':         'Charles-Henry-final.json',
    'Herrick':       'Susan-Herrick-final.json',
    'Holsinger':     'Kent-Holsinger-final.json',
    'Jockusch':      'Elizabeth-Jockusch-final.json',
    'Jones':         'Cynthia-Jones-final.json',
    'Knutie':        'Sarah-Knutie-final.json',
    'LewisL':        'Louise-Lewis-final.json',
    'LewisP':        'Paul-Lewis-final.json',
    'Les':           'Donald-Les-final.json',
    'Likens':        'Gene-Likens-final.json',
    'Schlichting':   'Carl-Schlichting-final.json',
    'Schultz':       'Eric-Schultz-final.json',
    'Schwenk':       'Kurt-Schwenk-final.json',
    'Seemann':       'Jeff-Seemann-final.json',
    'Silander':      'John-Silander-final.json',
    'Simon':         'Chris-Simon-final.json',
    'Tingley':       'Morgan-Tingley-final.json',
    'Trumbo':        'Stephen-Trumbo-final.json',
    'Turchin':       'Peter-Turchin-final.json',
    'Urban':         'Mark-Urban-final.json',
    'Wagner':        'David-Wagner-final.json',
    'Wegrzyn':       'Jill-Wegrzyn-final.json',
    'Wells':         'Kentwood-Wells-final.json',
    'Willig':        'Michael-Willig-final.json',
    'Yarish':        'Charles-Yarish-final.json',
    'Yuan':          'Yaowu-Yuan-final.json'
}

def updateCounts(authors):
    global person_counts
    if authors is None:
        return
        
    author_list = authors.split(',')
    for a in author_list:
        m = re.match('<(.+)>', a.strip())
        if m is not None:
            eeb_author = m.group(1)
            eeb_parts = eeb_author.split()
            if len(eeb_parts) == 3:
                assert eeb_parts[2] == 'Jr'
            else:
                assert len(eeb_parts) == 2, 'More than two parts found for EEB author "%s"' % eeb_author
            eeb_author_key = eeb_parts[1]
            if eeb_parts[1] == 'Lewis':
                if eeb_parts[0] == 'L' or eeb_parts[0] == 'LA':
                    eeb_author_key = 'LLewis'
                elif eeb_parts[0] == 'P' or eeb_parts[0] == 'PO':
                    eeb_author_key = 'PLewis'
            
            if eeb_author_key in person_counts.keys():
                person_counts[eeb_author_key] += 1
            else:
                person_counts[eeb_author_key] = 1

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
dupf = open('duplicates.txt', 'w')
nyearless = 0
nexceptions = 0
nduplicates = 0
ninpress = 0
nbooks = 0
nchapters = 0
neditedvolumes = 0
bibentries = []
titles_seen = {}
title_lookup = {}
person_counts = {}
for f in faculty:
    fn = '%s' % filepaths[f]
    print('Reading file "%s"...' % fn)
    stuff = open(fn, 'r').read()
    results = json.loads(stuff)
    for result in results:
        if not result['ignore']:
            # Add to counts for EEB authors
            updateCounts(result['authors'])
            # Capture information in r
            if result['authors'] is None:
                authors = None
            else:
                authors,nsubs = re.subn(r'<(.+?)>', r'**\1**', result['authors'])
            year    = result['year']
            #title   = re.sub(r'\b_(.+?)_\b', r'<em>\1</em>', result['title'])
            title   = result['title']
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
                
            already_seen = False
            if title in titles_seen.keys():
                already_seen = True
            else:
                titles_seen[title] = f
            
            # Construct bibliography string
            yearless = False
            exception = False
            inpress = False
            ischapter = False
            iseditedvolume = False
            isbook = False
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
            elif authors is None and (booktitle and bookeditors and bookpublisher and bookcity and bpage and epage):
                iseditedvolume = True
                bib = '%s (eds.) %s. %s. %s, %s' % (bookeditors, year, booktitle, bookpublisher, bookcity)
            elif booktitle and bookeditors and bookpublisher and bookcity and bpage and epage:
                ischapter = True
                bib += ' pp. %s-%s in: %s, %s (eds.) %s, %s' % (bpage, epage, booktitle, bookeditors, bookpublisher, bookcity)
            elif booktitle and bookeditors and bookpublisher and bpage and epage:
                ischapter = True
                bib += ' pp. %s-%s in: %s, %s (eds.) %s' % (bpage, epage, booktitle, bookeditors, bookpublisher)
            elif booktitle and bookpublisher:
                ischapter = True
                bib += ' In: %s, %s' % (booktitle, bookpublisher)
            elif bookisbn and bookpublisher:
                isbook = True
                bib += ' %s' % bookpublisher
                if bookcity:
                    bib += ', %s' % bookcity
                if bookisbn:
                    bib += ' ISBN: %s' % bookisbn
            else:
                exception = True
            if doi:
                bib += ' [DOI](https://doi.org/%s)' % doi
            bib += '\n'

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
                if already_seen:
                    nduplicates += 1
                    dupf.write('\n-------------------\n')
                    dupf.write('Previous: %s\n' % titles_seen[title])
                    dupf.write('~~> %s\n' % bib)
                    dupf.write('Current: %s\n' % f)
                    dupf.write('~~> %s\n' % title_lookup[title])
                else:
                    bibentries.append(entry)
                    title_lookup[title] = bib
            elif isbook:
                nbooks += 1
                entry = (year, bib)
                bibentries.append(entry)
            elif iseditedvolume:
                neditedvolumes += 1
                entry = (year, bib)
                if already_seen:
                    nduplicates += 1
                    dupf.write('\n-------------------\n')
                    dupf.write('Previous: %s\n' % titles_seen[title])
                    dupf.write('~~> %s\n' % bib)
                    dupf.write('Current: %s\n' % f)
                    dupf.write('~~> %s\n' % title_lookup[title])
                else:
                    bibentries.append(entry)
                    title_lookup[title] = bib
            else:
                entry = (year, bib)
                if already_seen:
                    nduplicates += 1
                    dupf.write('\n-------------------\n')
                    dupf.write('Previous: %s\n' % titles_seen[title])
                    dupf.write('~~> %s\n' % bib)
                    dupf.write('Current: %s\n' % f)
                    dupf.write('~~> %s\n' % title_lookup[title])
                else:
                    bibentries.append(entry)
                    title_lookup[title] = bib
            if inpress:
                ninpress += 1
                    
exceptf.close()
dupf.close()

#for (y,b) in bibentries:
#    print(y)
#    #if '<' in b:
#    #    print('\n~~~~~\n%s\n~~~~~\n' % b)

bibentries.sort()

gatherf = open('bibliography.md', 'w')
gatherf.write('\nSorted bibliographic entires:\n')
ngood = len(bibentries)
for b in bibentries:
    gatherf.write('%s\n' % b[1])
gatherf.close()

print('nyearless      = %d' % nyearless)
print('nexceptions    = %d' % nexceptions)
print('nduplicates    = %d' % nduplicates)
print('ninpress       = %d' % ninpress)
print('nchapters      = %d' % nchapters)
print('nbooks         = %d' % nbooks)
print('neditedvolumes = %d' % neditedvolumes)
print('ngood          = %d' % ngood)

print('\nPerson counts:')
counts = []
for k in person_counts.keys():
    counts.append((person_counts[k], k))
counts.sort()
counts.reverse()
for c,p in counts:
    print('%6d %s' % (c,p))
