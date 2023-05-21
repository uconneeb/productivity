# Usage:
# To perform Google Scholar search on Elizabeth Jockusch:
#   python3 scrape.py Jockusch search
# To combine json files from previous search, omit "search" from command line:
#   python3 scrape.py Jockusch

import json, glob, re, sys, os
from serpapi import GoogleSearch

authors = {}
authors['Adams']    = {'first':'Eldridge',  'last':'Adams',    'startyear':2015, 'taboo':['rBZQAg4AAAAJ','01qlNGcAAAAJ', 'dqEjzwUAAAAJ', 'EG1ADlUAAAAJ', 'p89zeI4AAAAJ', 'panLJB4AAAAJ', 'PArNBlIAAAAJ', 'pUSKdewAAAAJ', 'emVEsYkAAAAJ', 'k6VE2KEAAAAJ', 'J-qhKWkAAAAJ']}
authors['Bush']     = {'first':'Andrew',    'last':'Bush',     'startyear':2015, 'taboo':['OsQOa7sAAAAJ','SwYlxJ4AAAAJ','SiVfZFYAAAAJ','YccjWNoAAAAJ']}
authors['Diggle']   = {'first':'Pamela',    'last':'Diggle',   'startyear':2015, 'taboo':[]}
authors['Elphick']  = {'first':'Chris',     'last':'Elphick',  'startyear':2015, 'taboo':[]}
authors['Henry']    = {'first':'Charles',   'last':'Henry',    'startyear':2015, 'taboo':['rS2kfWMAAAAJ']}
authors['Fry']      = {'first':'Adam',      'last':'Fry',      'startyear':2015, 'taboo':[]}
authors['Jockusch'] = {'first':'Elizabeth', 'last':'Jockusch', 'startyear':2015, 'taboo':[]}
#                                                   Kraemer (no ID)
authors['Likens']   = {'first':'Gene',      'last':'Likens',   'startyear':2015, 'taboo':[]}
#                                                   Preston-Berlin (no ID)
#                                                   Wilson (no ID)

assert len(sys.argv) > 1, 'specify last name on command line'
focal_scholar_id = sys.argv[1]
try:
    author = authors[focal_scholar_id]
except ValueError:
    sys.exit('No entry for %s' % sys.argv[1])
    
do_search = False
if len(sys.argv) > 2 and sys.argv[2] == 'search':
    do_search = True

start = 0
if len(sys.argv) > 3:
    start_arg = sys.argv[3]
    try:
        start = int(start_arg)
    except ValueError:
        sys.exit('aborted because %s could not be interpreted as an int' % start_arg)

if do_search:
    answer = input('About to perform search for papers from %s %s. OK to continue? y/n --> ' % (author['first'], author['last']))
    if not answer == 'y':
        sys.exit('Aborted at user request.')
else:
    print('Combining existing json files into a combined, groomed json file for %s %s' % (author['first'], author['last']))

num       = 20

def pull(what, result):
    if what in result.keys():
        return result[what]
    else:
        return ''
        
def extractPublicationInfo(info, last_name, taboo_authors):
    # process string like this:
    # \u2026, TC Boothby, I Giovannini, L Rebecchi, EL Jockusch\u2026 - Current Biology, 2016 - Elsevier
    d = {'authors':'', 'year':'', 'success':True}

    # Extract info from summary
    m = re.match('(.+?)\s+[-]\s+(.+?)\s+[-]\s+(.+?)', info['summary'])
    if m is not None:
        authors = m.group(1)
        journal_year = m.group(2)
        other = m.group(3)
        try:
            journal,year = journal_year.split(',')
        except ValueError:
            m = re.search('\b(\d\d\d\d)\b', journal_year)
            if m is not None:
                year = m.group(1)
                journal = journal_year
            else:
                journal = journal_year
                year = '9999'
            print('*** failed to split "%s" into journal and year' % journal_year)
        authors = re.sub('\u2026', '...', authors)
        d['authors'] = authors
        d['year'] = year.strip()
        d['journal'] = journal.strip()
    
    # Check whether last_name is an author in the taboo list
    try:
        for a in info['authors']:
            name_same = re.search(r'\b%s\b' % last_name, a['name']) is not None
            is_taboo = a['author_id'] in taboo_authors
            if name_same and is_taboo:
                print('Taboo author: %s (%s)' % (a['name'],a['author_id']))
                d['success'] = False
            elif name_same:
                print('Should be on taboo list? %s (%s)' % (a['name'],a['author_id']))
            
    except KeyError:
        pass   
            
    return d

def getNumValid(organic_results, last_name, taboo):
    nvalid = 0

    for r in organic_results:
        publication_info = extractPublicationInfo(pull('publication_info', r), last_name, taboo)
        ok = False
        if publication_info['success']:
            ok = True
            authors = pull('authors', publication_info)
            if len(authors.strip()) > 0:
                m = re.search(r'\b%s\b' % author['last'], authors, re.I)
                if m is None:
                    ok = False
            else:
                ok = False
            
        if ok:
            nvalid += 1
            
    return nvalid

if do_search:
    search_string = '%s %s' % (author['first'], author['last'])
    done = False
    while not done:
        params = {
          "engine": "google_scholar",
          "q": search_string,
          "as_ylo": '%d' % author['startyear'],
          "hl": "en",
          "start": start,
          "num": num,
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
        if 'organic_results' in results.keys():
            narticles = len(results['organic_results'])
            if narticles < num:
                done = True
            else:
                start += num
                
                # A valid article is one in which author['last'] appears in list of authors
                # For example, many Google search results for Pam Diggle are returned because 
                # Pam was acknowledged, not because she was an author
                valid_articles = getNumValid(results['organic_results'], author['last'], author['taboo'])
                
                answer = input('number of valid articles in last batch was %d: continue? y/n --> ' % valid_articles)
                if not answer in ['y','Y']:
                    done = True
        else:
            print('Could not find any articles in "%s"' % fn)
            done = True
else:
    print('Not doing google scholar search because do_search = False')

    filenames = glob.glob('%s-%s-*.json' % (author['first'], author['last']))
    for fn in filenames:
        fnroot,fnext = os.path.splitext(fn)
        print('fn = "%s" | fnhead = "%s" | fntail = "%s"' % (fn, fnroot, fnext))
        stuff = open(fn, 'r').read()
        results = json.loads(stuff)
        outf = open('%s.txt' % fnroot,'w')
        outf.write(json.dumps(results, indent=4))
        outf.close()
            
# Get filenames
filenames = glob.glob('%s-%s-*.json' % (author['first'], author['last']))

# Read results from json files and transfer to combined json file
groomed = []
feedback_list = []
for fn in filenames:
    if 'combined' in fn:
        continue
    stuff = open(fn, 'r').read()
    results = json.loads(stuff)
    
    print('~~~ processing "%s"' % fn)
    
    # Spit out info
    if 'organic_results' in results.keys():
        for r in results['organic_results']:
            publication_info     = extractPublicationInfo(pull('publication_info', r), author['last'], author['taboo'])
            if not publication_info['success']:
                print('***   for position %d' % pull('position',r))
            authors = pull('authors', publication_info)
            inline_links = pull('inline_links', r)
            total_citations = None
            cites_id = None
            if inline_links:
                cited_by = pull('cited_by', inline_links)
                if cited_by:
                    total_citations = pull('total', cited_by)
                    cites_id = pull('cites_id', cited_by)
            ok = True
            if len(authors.strip()) > 0:
                m = re.search(r'\b%s\b' % author['last'], authors, re.I)
                if m is None:
                    ok = False
            else:
                ok = False

            if ok:
                entry = {}
                entry['ignore']      = False
                entry['position']    = pull('position', r)
                entry['title']       = pull('title', r)
                entry['url']         = pull('link', r)
                entry['authors']     = authors
                try:
                    entry['year']    = int(pull('year', publication_info))
                except ValueError:
                    entry['year']    = 9999
                    y =  pull('year', publication_info)
                    print('**** failed to convert "%s" to an int' % y)
                    print('**** position %s' % entry['position'])
                    print('**** begin publication_info dict')
                    print(publication_info)
                    print('**** end publication_info dict')
                entry['journal']     = pull('journal', publication_info)
                entry['ncites']       = total_citations
                entry['citation_id']  = cites_id
                #entry['volume']      = volume
                #entry['number']      = number
                #entry['bpage']       = bpage
                #entry['epage']       = epage
                #entry['article']     = article
                print('YEAR = ',entry['year'])
                if entry['year'] > 2014:
                    groomed.append(entry)
                    feedback_list.append((entry['year'], entry['title']))
            else:
                print('#### ok = False: publication_info follows:')
                print(publication_info)
            
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
