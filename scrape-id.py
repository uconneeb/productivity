# Usage:
# To perform Google Scholar search on Google Scholar ID bIbzgcwAAAAJ:
#   python3 scrape.py bIbzgcwAAAAJ search
# To combine json files from previous search, omit "search" from command line:
#   python3 scrape.py bIbzgcwAAAAJ

import json, glob, re, sys, os
from serpapi import GoogleSearch

authors = {}
#                                  Adams (no ID)
authors['pH6mu0sAAAAJ'] = {'last':'Anderson',       'first':'Gregory',  'startyear':2015, 'taboo':[]}
authors['bIbzgcwAAAAJ'] = {'last':'Bagchi',         'first':'Robert',   'startyear':2015, 'taboo':[]}
authors['cfwxm0AAAAAJ'] = {'last':'Bolnick',        'first':'Daniel',   'startyear':2018, 'taboo':[]}
authors['SiVfZFYAAAAJ'] = {'last':'Bush',           'first':'Andrew',   'startyear':2015, 'taboo':[]}  
authors['Zqrk9dIAAAAJ'] = {'last':'Caira',          'first':'Janine',   'startyear':2015, 'taboo':[]}
authors['utgfbkgAAAAJ'] = {'last':'Chazdon',        'first':'Robin',    'startyear':2015, 'taboo':[]}
authors['437hzCIAAAAJ'] = {'last':'Klarian',        'first':'Sebastian','startyear':2015, 'taboo':[]}
authors['i2OF2g0AAAAJ'] = {'last':'Colwell',        'first':'Rob',      'startyear':2015, 'taboo':[]}
authors['VrCsRx0AAAAJ'] = {'last':'Diggle',         'first':'Pam',      'startyear':2015, 'taboo':[]}
#                                  Elphick (no ID)
authors['aXo5yZYAAAAJ'] = {'last':'Cooley',         'first':'John',     'startyear':2015, 'taboo':[]}
authors['ww6Yrk8AAAAJ'] = {'last':'Davis',          'first':'Miranda',  'startyear':2015, 'taboo':[]}
authors['89WVt2cAAAAJ'] = {'last':'Finiguerra',     'first':'Michael',  'startyear':2015, 'taboo':[]}
#                                  Fry (no ID)
authors['zC8V-30AAAAJ'] = {'last':'Fusco',          'first':'Nicole',   'startyear':2022, 'taboo':[]}
authors['qa7ATcwAAAAJ'] = {'last':'Garcia-Robledo', 'first':'Carlos',   'startyear':2016, 'taboo':[]}
authors['78jwN4sAAAAJ'] = {'last':'Goffinet',       'first':'Bernard',  'startyear':2015, 'taboo':[]}
authors['5x0u2ZYAAAAJ'] = {'last':'Herrick',        'first':'Susan',    'startyear':2015, 'taboo':[]}
authors['z3n2hIsAAAAJ'] = {'last':'Heyduk',         'first':'Karolina', 'startyear':2023, 'taboo':[]}
authors['J20p_QcAAAAJ'] = {'last':'Holsinger',      'first':'Kent',     'startyear':2015, 'taboo':[]}
authors['Y9KBfWcAAAAJ'] = {'last':'Jones',          'first':'Cynthia',  'startyear':2015, 'taboo':[]}
#                                  Jockusch (no ID)
authors['39rdP4QAAAAJ'] = {'last':'Knutie',         'first':'Sarah',    'startyear':2017, 'taboo':[]}
#                                  Kraemer (no ID)
authors['BRbxQwwAAAAJ'] = {'last':'Kremer',         'first':'Colin',    'startyear':2023, 'taboo':[]}
authors['jMNpedUAAAAJ'] = {'last':'Les',            'first':'Donald',   'startyear':2015, 'taboo':[]}
authors['Q0ZrkG0AAAAJ'] = {'last':'Lewis',          'first':'Louise',   'startyear':2015, 'taboo':['Q0ZrkG0AAAAJ:LjlpjdlvIbIC']}
authors['DyJu67sAAAAJ'] = {'last':'Lewis',          'first':'Paul',     'startyear':2015, 'taboo':['DyJu67sAAAAJ:cFHS6HbyZ2cC','DyJu67sAAAAJ:epqYDVWIO7EC','DyJu67sAAAAJ:9Nmd_mFXekcC','DyJu67sAAAAJ:ZfRJV9d4-WMC','DyJu67sAAAAJ:dTyEYWd-f8wC','DyJu67sAAAAJ:blknAaTinKkC','DyJu67sAAAAJ:j3f4tGmQtD8C','DyJu67sAAAAJ:_Qo2XoVZTnwC','']}
#                                  Likens (no ID)
authors['u-_ya4wAAAAJ'] = {'last':'McAssey',        'first':'Edward',   'startyear':2023, 'taboo':[]}
authors['AjOjxAsAAAAJ'] = {'last':'Merow',          'first':'Cory',     'startyear':2015, 'taboo':[]}
#                                  Preston-Berlin? (no ID)
authors['-OIEJlkAAAAJ'] = {'last':'Rubega',         'first':'Margaret', 'startyear':2015, 'taboo':[]}
authors['zrAaip4AAAAJ'] = {'last':'Schlichting',    'first':'Carl',     'startyear':2015, 'taboo':[]}
authors['2LmtZqAAAAAJ'] = {'last':'Schultz',        'first':'Eric',     'startyear':2015, 'taboo':[]}
authors['G-2IS0oAAAAJ'] = {'last':'Schwenk',        'first':'Kurt',     'startyear':2015, 'taboo':[]}
authors['ARrQFV4AAAAJ'] = {'last':'Seemann',        'first':'Jeff',     'startyear':2017, 'taboo':[]}
authors['h58BltkAAAAJ'] = {'last':'Skeen',          'first':'Heather',  'startyear':2015, 'taboo':[]}
authors['zHF_330AAAAJ'] = {'last':'Silander',       'first':'John',     'startyear':2015, 'taboo':[]}
authors['jSdi-YIAAAAJ'] = {'last':'Simon',          'first':'Chris',    'startyear':2015, 'taboo':[]}
authors['3NcNnn0AAAAJ'] = {'last':'Tingley',        'first':'Morgan',   'startyear':2015, 'taboo':[]}
authors['FwKkT4AAAAAJ'] = {'last':'Trumbo',         'first':'Stephen',  'startyear':2015, 'taboo':[]}
authors['W0C05zIAAAAJ'] = {'last':'Turchin',        'first':'Peter',    'startyear':2015, 'taboo':[]}
authors['8aJp2VQAAAAJ'] = {'last':'Urban',          'first':'Mark',     'startyear':2015, 'taboo':[]}
authors['CxLFoH8AAAAJ'] = {'last':'Wagner',         'first':'David',    'startyear':2015, 'taboo':[]}
authors['vV1_cjUAAAAJ'] = {'last':'Wegrzyn',        'first':'Jill',     'startyear':2015, 'taboo':[]}
authors['1Qj-p7QAAAAJ'] = {'last':'Wells',          'first':'Kentwood', 'startyear':2015, 'taboo':[]}
authors['798Vk8sAAAAJ'] = {'last':'Willig',         'first':'Michael',  'startyear':2015, 'taboo':[]}
#                                  Wilson (no ID)
authors['tlr2fqkAAAAJ'] = {'last':'Yarish',         'first':'Charles',  'startyear':2015, 'taboo':[]}
authors['1dizk4UAAAAJ'] = {'last':'Yuan',           'first':'Yaowu',    'startyear':2015, 'taboo':[]}

assert len(sys.argv) > 1, 'specify Google Scholar ID on command line'
focal_scholar_id = sys.argv[1]
try:
    author = authors[focal_scholar_id]
except ValueError:
    sys.exit('No entry for Google Scholar ID %s' % sys.argv[1])
    
do_search = False
if len(sys.argv) > 2 and sys.argv[2] == 'search':
    do_search = True

if do_search:
    answer = input('About to perform search for papers from %s %s. OK to continue? y/n --> ' % (author['first'], author['last']))
    if not answer == 'y':
        sys.exit('Aborted at user request.')
else:
    print('Combining existing json files into a combined, groomed json file for %s %s' % (author['first'], author['last']))

start      = 0
num        = 20
start_year = author['startyear']

if do_search:
    done = False
    while not done:
        params = {
          "engine": "google_scholar_author",
          "author_id": focal_scholar_id,
          "sort": "pubdate",
          "hl": "en",
          "start": start,
          "num": num,
          "as_vis": 0,
          "api_key": "d573d05be69ecb6194387a8f77c80494e23c8d215f52f7fb2d5baa45b2302681"
        }

        # Perform the Google search
        search = GoogleSearch(params)
        results = search.get_dict()

        # Save the results to a file
        fn = '%s-%s-%d.json' % (author['first'], author['last'], start)
        outf = open(fn,'w')
        outf.write(json.dumps(results, indent=4))
        outf.close()
        
        # Check if need to continue
        years = []
        if 'articles' in results.keys():
            for r in results['articles']:
                try:
                    year = int(r['year'])
                except ValueError:
                    year = 9999
                years.append(year)
            earliest = min(years)
            if earliest <= start_year:
                done = True
            else:
                start += num
                answer = input('earliest year found was %d: continue? y/n --> ' % earliest)
                if not answer in ['y','Y']:
                    done = True
        else:
            print('Could not find any articles in "%s"' % fn)
            done = True
else:
    print('Not doing google scholar search because do_search = False')
            
# Get filenames
filenames = glob.glob('%s-%s-*.json' % (author['first'], author['last']))

def pull(what, result):
    if what in result.keys():
        return result[what]
    else:
        return ''
        
def splitpub(pub, entry):
    done = False
    journal = None
    volume  = None
    number  = None
    bpage   = None
    epage   = None
    article = None
    
    # case 1: Bayesian Analysis 17 (3), 817-847, 2022
    m = re.match('(.+)\s+(\d+)\s+[(](\d+)[)],\s+(\d+)[-](\d+),\s+\d\d\d\d\s*', pub)
    if m is not None:
        journal = m.group(1)
        volume  = m.group(2)
        number  = m.group(3)
        bpage   = m.group(4)
        epage   = m.group(5)
        done = True
        
    # case 2: Bulletin of the Society of Systematic Biologists 1 (2), 2022
    if not done:
        m = re.match('(.+)\s+(\d+)\s+[(](\d+)[)],\s+\d\d\d\d', pub)
        if m is not None:
            journal = m.group(1)
            volume  = m.group(2)
            number  = m.group(3)
            done = True

    # case 3: Bayesian analysis 13 (2), 311, 2018
    if not done:
        m = re.match('(.+)\s+(\d+)\s+[(](\d+)[)],\s+(\d+),\s+\d\d\d\d', pub)
        if m is not None:
            journal = m.group(1)
            volume  = m.group(2)
            bpage   = m.group(4)
            done = True

    # case 4: Proceedings of the Royal Society B 289 (1975), 20220343, 2022
    if not done:
        m = re.match('(.+)\s+(\d+)\s+[(](\d+)[)],\s+([a-z0-9]+),\s+\d\d\d\d', pub)
        if m is not None:
            journal = m.group(1)
            volume  = m.group(2)
            number  = m.group(3)
            article = m.group(4)
            done = True

    # case 5: PeerJ 7, e6899, 2019
    if not done:
        m = re.match('(.+)\s+(\d+),\s+([a-z0-9]+),\s+\d\d\d\d', pub)
        if m is not None:
            journal = m.group(1)
            volume  = m.group(2)
            article = m.group(3)
            done = True
            
    # case 6: Notulae algarum 88, 1-2, 2019            
    m = re.match('(.+)\s+(\d+),\s+(\d+)[-](\d+),\s+\d\d\d\d\s*', pub)
    if m is not None:
        journal = m.group(1)
        volume  = m.group(2)
        bpage   = m.group(3)
        epage   = m.group(4)
        done = True
        
    entry['journal'] = journal
    entry['volume']  = volume
    entry['number']  = number
    entry['bpage']   = bpage
    entry['epage']   = epage
    entry['article'] = article
    return entry

# Read results from json files and transfer to combined json file
groomed = []
feedback_list = []
for fn in filenames:
    if 'combined' in fn:
        continue
    stuff = open(fn, 'r').read()
    results = json.loads(stuff)

    # Spit out info
    if 'articles' in results.keys():
        for r in results['articles']:
            entry = {}
            entry['ignore']      = False
            entry['authors']     = pull('authors', r)
            try:
                entry['year']    = int(pull('year', r))
            except ValueError:
                entry['year']    = 9999
            entry['title']       = pull('title', r)
            entry['citation_id'] = r['citation_id']
            entry['url']         = pull('link', r)
            entry['doi']         = ""
            citations            = pull('cited_by', r)
            entry['ncites']      = pull('value', citations)
            publication = pull('publication', r)
            entry = splitpub(publication, entry)
            if entry['year'] > 2011 and not entry['citation_id'] in author['taboo']:
                groomed.append(entry)
                feedback_list.append((entry['year'], entry['title']))
            
# Sort feedback_list by year and show list
feedback_list.sort()
for f in feedback_list:
    print('%s: %s' % (f[0],f[1]))

# Save the results to a file
fn = '%s-%s-combined.json' % (author['first'], author['last'])
if os.path.exists(fn):
    answer = input('overwrite "%s"? y/n --> ' % fn)
    if not answer == 'y':
        sys.exit('Aborted to avoid overwriting file.')
outf = open(fn,'w')
outf.write(json.dumps(groomed, indent=4))
outf.close()
