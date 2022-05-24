import os
import random
import requests
import shutil

class CSPIXELS:
    def __init__(self):
        self.curdir = os.path.dirname(__file__)
        self.api_keys = ['563492ad6f91700001000001dd97ba156f3a4518a14e2ef28a489ee9']
        self.tmp_image = None

    def random_image(self,keyword,w=1200,h=675,img_name='cspixels_temporary.jpg',orientation = None):
        # orientation = landscape/portrait/square
        # Get total search result 
        keyword = requests.utils.quote(keyword)
        url = 'https://api.pexels.com/v1/search?query='+str(keyword)+'&page=1&per_page=1'
        url = url + ('&orientation='+orientation if orientation != None else '')
        # print(url)
        res = requests.get(url, headers= {'Authorization':random.choice(self.api_keys)})
        # print(res.headers)


        if res.status_code != 200:
            return False
        res_json = res.json()
        total_results = res_json['total_results']
        print('Total search results: '+str(total_results))

        # Random from total search result 
        rand_page = random.randint(1,int(total_results))
        print('Random choice image: '+str(rand_page))
        url = 'https://api.pexels.com/v1/search?query='+str(keyword)+'&page='+str(rand_page)+'&per_page=1'
        url = url + ('&orientation='+orientation if orientation != None else '')
        res = requests.get(url, headers= {'Authorization':random.choice(self.api_keys)})
        res_json = res.json()
        photo = res_json['photos'][0]
        photo_path = photo['src']['original']
        print('Image id: '+str(photo['id']))

        # Download image to temporary file
        photo_path = photo_path+'?auto=compress&cs=tinysrgb&fit=crop&h='+str(h)+'&w='+str(w)
        tmp_path = os.path.join(self.curdir,img_name)
        res = requests.get(photo_path, stream=True)
        with open(tmp_path, 'wb') as out_file:
            shutil.copyfileobj(res.raw, out_file)
        print('Download image completed!')
        self.tmp_image = tmp_path
        return tmp_path
    def clear(self):
        try:
            os.remove(self.tmp_image)
        except:
            pass

# px = CSPIXELS()
# img = px.random_image('female and rain')
# print(img)


