import urllib2
from urlparse import urljoin
from BeautifulSoup import *

class crawler:
    def __init__(self,database):
        self.database = database

    def __del__(self):
        self.database.close()

    def dbcommit(self):
        self.database.dbcommit()

    #auxilliary function for getting an entry id and addign it if its not present
    def getentryid(self,table,field,value,createnew=True):
        return None

    #index individual page
    def addtoindex(self,url,soup):
        print 'Indexing %s' % url

    #extract text from html page (no tags)
    def gettextonly(self,soup):
        soup_string = soup.string

        if soup_string==None:
            contents = soup.contents
            resulttext=''
            for text in contents:
                subtext = self.gettextonly(text)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return soup_string.strip()

    #seperate words by any non-whitespare characters
    def seperatewords(self,text):
        splitter = re.compile('\\W*')
        return [word.lower for word in splitter.split(text) if word != '']
    #return true if url already indexed
    def isindexed(self,url):
        return False

    #add a link between two pages
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass

    #starting with a list of pages, do a breadth
    #first search to the given depth, indexing pages as we go
    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages=set()

            for page in pages:
                try:
                    pageConnection = urllib2.urlopen(page)
                except:
                    print "Could not open page %s" %page
                    continue
                soup = BeautifulSoup(pageConnection.read())
                self.addtoindex(page,soup)

                links=soup('a')

                for link in links:
                    if 'href' in dict(link.attrs):
                        url=urljoin(page,link['href'])

                        if url.find("'")!=-1:   #unsure why this is required
                            continue
                        url = url.split('#')[0]
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)

                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)
                self.dbcommit()
            pages=newpages



    #create the database tables
    def createindextables(self):
        self.database.execute('create table urllist(url)')
        self.database.execute('create table wordlist(word)')
        self.database.execute('create table wordlocation(urlid,wordid,location)')
        self.database.execute('create table link(fromid integer,toid integer)')
        self.database.execute('create table linkwords(wordid,linkid)')
        self.database.execute('create index wordidx on wordlist(word)')
        self.database.execute('create index urlidx on urllist(url)')
        self.database.execute('create index wordurlidx on wordlocation(wordid)')
        self.database.execute('create index urltoidx on link(toid)')
        self.database.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()

