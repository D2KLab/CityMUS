import urllib2
import json

page = 0 
places = []
while True:
    if page%10 == 0:
        print('page: %d' % page)
    req = urllib2.Request('http://aplicaciones.localidata.com/eldaSuit/place/city/nice?_view=list&_sort=label&_pageSize=50&_page='+str(page))

    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        if e.code == 404:
            print('ERROR')
            print(e.reason)
            print(e.geturl())
            break
        else:
            print('ERROR')
            print(e.reason)
            print(e.geturl())
            break
    except urllib2.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        print('ERROR')
        print(e.reason)
        print(e.geturl())
        break
    else:
        # 200
        body = resp.read()
        result = json.loads(body)
        for item in result['result']['items']:
            #print(item)
            places.append(item)
            print(len(places))
        if len(result['result']['items']) == 0:
            break
    page += 1
print('end')


with open('data/3cixty_places_dump.json', 'w') as outfile:
    json.dump(places, outfile)