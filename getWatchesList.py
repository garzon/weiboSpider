import requests, json, time, BeautifulSoup, os, os.path, secret
import parmap

def find_inner_text(haystack, prefix, suffix):
    try:
        stpos = haystack.index(prefix)
        haystack = haystack[stpos+len(prefix):]
        endpos = haystack.index(suffix)
        haystack = haystack[:endpos]
        return haystack
    except:
        print '[WARNING] In %s\nprefix: %s, suffix: %s not found' % (haystack, prefix, suffix)
        raise Exception
        return ''

def max_num_per_interval_wrapper(interval):
    global created_time
    created_time = 0.0
    global counter
    counter = 0
    def max_num_per_interval(num):
        global created_time, counter
        now = time.time()
        if now-created_time < interval:
            counter += 1
            if counter > num:
                sleepTime = interval-(now-created_time)
                print '[INFO] max number limit(%d) per %fs exceeded, sleep for %fs...' % (num, interval, sleepTime)
                time.sleep(sleepTime)
                counter = 0
                created_time = time.time()
        else:
            created_time = now
            counter = 1
    return max_num_per_interval

def debug_save(html):
    with open('d:\\1.html','wb') as f:
        f.write(html)
        
def parseTr(tr):
    tds = tr.findAll('td')
    td = tds[1]
    nickname = td.find('a').text
    avatar_url = tds[0].find('img')['src']
    nameAndWatchLink = td.findAll('a')
    if len(nameAndWatchLink) >= 2:
        uid = find_inner_text(nameAndWatchLink[1]['href'],'uid=','&')
    else:
        # watched people comes here
        myWatchesList = getWatchesList(secret.myUid)
        uid = None
        for i in myWatchesList:
            if i['nickname'] == nickname:
                uid = i['uid']
                break
        if uid is None:
            if nickname == secret.myNickName:
                uid = secret.myUid
            else:
                raise RuntimeError('cannot fetch uid of watched people %s' % nickname)
    ext = ''
    for i in avatar_url[::-1]:
        if i != '.':
            ext = i + ext
        else:
            break
    avatar_path = 'user_avatar/%s' % uid
    if not os.path.isfile(avatar_path):
        avatar_binary = requests.get(avatar_url).content
        with open(avatar_path, 'wb') as f:
            f.write(ext)
        with open(avatar_path + '.' + ext, 'wb') as f:
            f.write(avatar_binary)
    print '%s(%s) parsed!' % (nickname, uid)
    return {
        'nickname': nickname,
        'uid': uid
    }
        
def getWatchesList(uid):
    page = 1
    file_path = 'watches_data/%s.json' % uid
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        res = json.loads(f.read())
        f.close()
        return res
    def getPage(page):
        print 'Fetching watches list of user %s(page %d)...' % (uid, page)
        global s, header
        url = 'http://weibo.cn/%s/follow?page=%d'  % (uid, page)
        max_num_per_sec(1)
        resp = s.get(url, headers=header)
        if resp.status_code != 200: raise Exception("%d - status code err" % resp.status_code)
        soup = BeautifulSoup.BeautifulSoup(resp.text)
        try:
            trs = [i.find('tr') for i in soup.findAll('table')]
        except:
            print soup
            debug_save(resp.content)
            print 'GET %s error, cookies: ' % url
            print s.cookies.get_dict()
            exit()
        res = parmap.map(parseTr, trs)
        pagelist_div = soup.find(id='pagelist')
        if pagelist_div is not None:
            totalpage = int(find_inner_text(pagelist_div.find('div').text, '/',u'\u9875'))
        else:
            totalpage = 1
        return res, totalpage
    res, totalpage = getPage(page)
    for i in xrange(2, totalpage+1):
        res += getPage(i)[0]
    with open(file_path, 'wb') as f:
        f.write(json.dumps(res))
    return res

if __name__ == "__main__":

    max_num_per_sec = max_num_per_interval_wrapper(2.0)

    s = requests.session()
    header = { 'Connection' : 'keep-alive',  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36', 'Cookie': secret.COOKIES  }
    
    myWatchesList = getWatchesList(secret.myUid)
    for user in myWatchesList:
        print 'Fetching watchlist of %s(%s)...' % (user['nickname'], user['uid']) 
        getWatchesList(user['uid'])