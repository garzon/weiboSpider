import os, json, networkx, parmap

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

def filename2uid(filename):
    return find_inner_text(filename, '/', '.json')
    
def file_reader(filename):
    f = open(filename, 'rb')
    res = json.loads(f.read())
    f.close()
    return res
        
file_list = os.popen('ls watches_data/*.json').read().split('\n')
json_list = {filename2uid(i):file_reader(i) for i in file_list if len(i) > 0}