import urllib2

def getMatchingEmailWS(self, match, callback='?'):
    response = urllib2.urlopen('https://ws.it.uwosh.edu/getMatchingEmailCX?match=%s&type=json&callback=%s' % (match, callback))
    html = response.read()
    return html
