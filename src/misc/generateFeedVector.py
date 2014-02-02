import feedparser
import re


def getwordcounts(url):
    d = feedparser.parse(url)
    wordCount = {}

    for entry in d.entries:
        if 'summary' in entry:
            summary = entry.summary
        else:
            summary = entry.description

        words = getWords(entry.title + ' ' + summary)

        for word in words:
            wordCount.setdefault(word, 0)
            wordCount[word] += 1

        return d.feed.title, wordCount


def getWords(html):
    # remove html tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    #split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    #convert to lowercase
    return [word.lower() for word in words if word != '']

#holds number of blogs each word appeared in.
apcount = {}

#holds dictionary mapping title of blog to word count
wordCounts = {}
feedlist = [line for line in file('feedlist.txt')]
for feedurl in feedlist:
    try:
        title, wc = getwordcounts(feedurl)
        wordCounts[title] = wc

        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1
    except:
        print 'Failed to parse %s' % feedurl


wordList = []

for word, blogCount in apcount.items():
    frac = float(blogCount) / len(feedlist)

    if frac > 0.1 and frac < 0.5:
        wordList.append(word)

out = file('blogData.txt', 'w')
out.write('Blog')
for word in wordList:
    out.write('\t%s' % word)

out.write('\n')
for blog, wordCount in wordCounts.items():
    out.write(blog)

    for word in wordList:
        if word in wordCount:
            out.write('\t%d' % wordCount[word])
        else:
            out.write('\t0')
    out.write('\n')

