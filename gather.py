import json, sys, re, sys

starting_year = 2015

authors_like_faculty = [
    'RR Colwell',
    'C Anderson',
    'CD Anderson',
    'DL Anderson',
    'E Anderson',
    'J Anderson',
    'M Anderson',
    'MKJ Anderson',
    'RL Anderson',
    'RM Anderson',
    'T Anderson',
    'TJ Anderson',
    'SE Bush',
    'AM Cooley',
    'JE Cooley',
    'CJ Davis', 
    'D Davis',   
    'DA Davis',   
    'DR Davis', 
    'KE Davis',  
    'JI Davis',
    'JM Davis',
    'JP Davis',
    'WJ Davis',
    'N Henry',
    'WJ Henry',
    'AT Jones',
    'AW Jones',
    'FA Jones',
    'FAM Jones',
    'TH Jones',
    'AM Les',
    'FH Wagner',
    'DM Wagner',
    'M Wagner',
    'V Wagner',
    'CB Schultz',
    'A Simon',
    'MF Simon',
    'B Wells',
    'Z Yuan'
]

singleton = None #['Bagchi']
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
        return (False, None)
    
    # Split the authors list at the commas
    author_list = authors.split(',')
    
    for a in author_list:
        astripped = a.strip();
        m = re.match('<(.+)>', astripped)
        if m is not None:
            astripped = m.group(1)
        eeb_parts = astripped.split()
        initials = None
        surname = None
        partial_surnames = ['al', 'Al', 'dalla', 'Dalla', 'da', 'Da', 'de', 'De', 'del', 'Del', 'den', 'Den', 'des', 'Des', 'di', 'Di', 'do', 'Do', 'dos', 'Dos', 'la', 'La', 'le', 'Le', 'san', 'San', 'st', 'St', 'ter', 'Ter', 'van', 'Van', 'von', 'Von']
        if len(eeb_parts) == 5:
            ok = False
            if eeb_parts[1] in partial_surnames:
                initials = eeb_parts[0]
                surname = '%s %s %s %s' % (eeb_parts[1], eeb_parts[2], eeb_parts[3], eeb_parts[4])
                ok = True
            elif astripped == '(511 authors including <MR Willig>)':
                initials = ''
                surname = astripped
                ok = True
            assert ok, 'eeb_parts has length 5 but does not fall into acceptable cases: author = "%s"' % astripped
        elif len(eeb_parts) == 4:
            ok = False
            if eeb_parts[1] in partial_surnames:
                initials = eeb_parts[0]
                surname = '%s %s %s' % (eeb_parts[1], eeb_parts[2], eeb_parts[3])
                ok = True
            assert ok, 'eeb_parts has length 4 but does not fall into acceptable cases: author = "%s"' % astripped
        elif len(eeb_parts) == 3:
            ok = False
            if eeb_parts[2] in ['Jr', 'II', 'III']:
                ok = True
            elif eeb_parts[1] in partial_surnames:
                initials = eeb_parts[0]
                surname = '%s %s' % (eeb_parts[1], eeb_parts[2])
                ok = True
            elif 'D Ortega‐Del Vecchyo' == astripped:
                initials = 'D'
                surname = 'Ortega‐Del Vecchyo'
                ok = True
            assert ok, 'eeb_parts has length 3 but does not fall into acceptable cases: author = "%s" (eeb_parts[2] = "%s")' % (astripped, eeb_parts[2])
        elif len(eeb_parts) == 2:
            initials = eeb_parts[0]
            surname = eeb_parts[1]
        elif len(eeb_parts) == 1:
            initials = ''
            surname = eeb_parts[0]
        elif 'et al.' in astripped:
            initials = ''
            surname = astripped
        else:
            assert False, 'Could not parse EEB author "%s"' % astripped
            
        # See if author a is marked as being an EEB faculty member
        #m = re.match('<(.+)>', astripped)
        if m is None:
            # author a is NOT marked as an EEB faculty member
            # check to make sure it is really not an EEB faculty member
            if surname in faculty and not astripped in authors_like_faculty:
                print('"%s" should be marked as EEB faculty?' % astripped)
                return (True, astripped)
        else:
            # author a is marked as an EEB faculty member
            if surname == 'Lewis':
                if initials == 'L' or initials == 'LA':
                    surname = 'LLewis'
                elif initials == 'P' or initials == 'PO':
                    surname = 'PLewis'
            
            if surname in person_counts.keys():
                person_counts[surname] += 1
            else:
                person_counts[surname] = 1
    
    return (True, None)
    
def checkJournalNames(journalf, journal):
    if journal is None:
        return None
        
    journal_asis = [
        'and', 
        'in', 
        'of', 
        'the',
        'for',
        'et',
        'de',
        'del',
        'as',
        'la',
        'ACS',
        'BioScience',
        'MBio',
        'ISME',
        'PLoS',
        'PeerJ',
        'BMC',
        'della',
        'SORT-Statistics',
        '(Punta',
        'Arenas)',
        'DNA',
        'Asia-Pacific',
        'SSAR',
        'IAWA'
    ]        
        
    diff = ord('a') - ord('A')
    ordA = ord('A')
    ordZ = ord('Z')

    # Create new journal name with every word capitalized
    jvect = []
    jparts = journal.strip().split(' ')
    for jpart in jparts:
        if jpart == '&':
            jvect.append('and')
        elif not jpart in journal_asis:
            jvect.append(jpart.capitalize())
        else:
            jvect.append(jpart)
        
    journal2 = ' '.join(jvect)
    ok = journal == journal2
        
    if not ok:
        journalf.write('"%s" --> "%s"\n' % (journal, journal2))
        return journal2
        
    return journal

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
journalf = open('journal-issues.txt', 'w')
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

chosen_ones = singleton
if chosen_ones is None:
    chosen_ones = faculty
for f in chosen_ones:
    fn = '%s' % filepaths[f]
    print('Reading file "%s"...' % fn)
    stuff = open(fn, 'r').read()
    results = json.loads(stuff)
    
    for result in results:
        if not result['ignore']:
            # Add to counts for EEB authors
            has_authors,eeb_author_not_bracketed = updateCounts(result['authors'])
            if eeb_author_not_bracketed is not None:
                print(result)
                sys.exit('author "%s" needs to be bracketed' % eeb_author_not_bracketed)
            if result['authors'] is None:
                authors = None
            else:
                authors,nsubs = re.subn(r'<(.+?)>', r'**\1**', result['authors'])
            year    = result['year']
            #title   = re.sub(r'\b_(.+?)_\b', r'<em>\1</em>', result['title'])
            title   = result['title']

            journal = result['journal']
            good_journal_name = checkJournalNames(journalf, journal)
            if not good_journal_name == journal:
                print(result)
                sys.exit('bad journal name: "%s" --> "%s"' % (journal,good_journal_name))

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
                bib += '%s.' % authors
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
                bib = '%s (eds.) %s. %s. %s, %s.' % (bookeditors, year, booktitle, bookpublisher, bookcity)
            elif booktitle and bookeditors and bookpublisher and bookcity and bpage and epage:
                ischapter = True
                bib += ' pp. %s-%s in: %s, %s (eds.) %s, %s.' % (bpage, epage, booktitle, bookeditors, bookpublisher, bookcity)
            elif booktitle and bookeditors and bookpublisher and bpage and epage:
                ischapter = True
                bib += ' pp. %s-%s in: %s, %s (eds.) %s.' % (bpage, epage, booktitle, bookeditors, bookpublisher)
            elif booktitle and bookpublisher:
                ischapter = True
                bib += ' In: %s, %s' % (booktitle, bookpublisher)
            elif bookisbn and bookpublisher:
                isbook = True
                bib += ' %s' % bookpublisher
                if bookcity:
                    bib += ', %s' % bookcity
                else:
                    bib += '.'
            else:
                exception = True
            if doi:
                bib += ' [https://doi.org/%s](https://doi.org/%s)' % (doi,doi)
            elif bookisbn:
                bib += ' ISBN: %s.' % bookisbn
            bib += '\n'
            
            if not has_authors:
                nexceptions += 1
                dumpException(exceptf, f, 'NO AUTHORS!', year, title, journal, volume, bpage, epage, doi)

            # Save in bibentries list
            if yearless:
                nyearless += 1
                nexceptions += 1
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
journalf.close()

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
