from flask import Flask,after_this_request
import time
import metadata_parser
from youtubesearchpython import VideosSearch
import urllib.request
from googlesearch import search
import urllib.parse
import re
import requests
from yarl import URL
from datetime import date,timedelta,datetime
from ecommercetools import seo
def same_link(d1,d2):
    return bool(d1==d2)
def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1
def translate_link(arr):
    arr0 = []
    for l in arr.split():
        for x in l:
            if x == '`':
                x = '/'
            arr0.append(x)
    return listToString(arr0)

def keyword_extraction(query):
    from bs4 import BeautifulSoup

    query = urllib.parse.quote_plus(query)
    req = requests.get("https://www.google.co.uk/search?q=" +'types of'+ query)
   # req = requests.get('https://www.google.com/search?q=types+of+data+science&rlz=1C1SQJL_enUS934US934&sxsrf=ALiCzsayQHqu7_7SLqLxq_NVZ-uvjTNtDw%3A1668304663832&ei=F09wY-GfMpGzqtsPks6qwAs&ved=0ahUKEwihh_WWh6r7AhWRmWoFHRKnCrgQ4dUDCBA&uact=5&oq=types+of+data+science&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQyBQgAEIAEMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjoKCAAQRxDWBBCwAzoNCAAQRxDWBBDJAxCwAzoICAAQkgMQsAM6BwgAELADEEM6DQgAEOQCENYEELADGAE6EgguEMcBENEDEMgDELADEEMYAjoHCCMQsAIQJzoHCAAQgAQQDUoECE0YAUoECEEYAEoECEYYAVC1Cli9G2DgHGgDcAF4AIABU4gB2wSSAQE5mAEAoAEByAERwAEB2gEGCAEQARgJ2gEGCAIQARgI&sclient=gws-wiz-serp')
    soup = BeautifulSoup(req.content,'html.parser')
    body = soup.find('body')
    divs = body.find_all('div')
    focus_div = divs[7]
    target_div = focus_div.find_all('div',class_='Lt3Tzc')
    #class_='Lym8W.xCgLUe'
#def is_a_match(clas):
    #BNeawe
    #return clas.startswith('BNeawe')
#HTML breakpoint
    keyword_parent_div = focus_div
    types_divs_section = keyword_parent_div.find('div',class_='P1NWSe')
    subsection_divs = keyword_parent_div.find('div',class_='Xdlr0d')
    subsection_divs_1 = subsection_divs.find('div',class_='idg8be')
#machine learning
    subsection_divs_2 = subsection_divs_1.select_one(':nth-child(1)')
#computer security
    subsection_divs_3 = subsection_divs_1.select_one(':nth-child(3)')
#Information Engineering
    subsection_divs_4 = subsection_divs_1.select_one(':nth-child(4)')
    tags_of_interest = keyword_parent_div.find('div',class_='AzWLW')
    try:
        toi = tags_of_interest.find_all('div')[0]
        data_tags = toi.find_all('div',class_='BNeawe s3v9rd AP7Wnd')
        print(data_tags)
        keywords = []
        for i in data_tags:
            keywords.append(i.text)
        return [len(keywords),keywords]
    except:
        return 'The educational search you made is specific,use  google search field for it located at the top'

def bubbleSort(arr):
    n = len(arr)
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    swapped = False
    # Traverse through all array elements
    for i in range(n - 1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j].lower() > arr[j + 1].lower():
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return


def bubbleSortWParam(arr, param):
    n = len(arr)
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    swapped = False
    # Traverse through all array elements
    for i in range(n - 1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j][param].lower() > arr[j + 1][param].lower():
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return


def disect_array(test_array, test_array_1):
    entire_array = []
    init = 0
    i = -1
    for x in test_array:
        i += 1
        if test_array_1[i - 1][0].lower() != test_array_1[i][0].lower():
            entire_array.append(test_array[init:i])
            init = i
    if test_array_1[i - 1][0].lower() != test_array_1[i][0].lower():
        entire_array.append(test_array[init:])
    else:
        entire_array.pop(0)
        entire_array.append(test_array[init:])
    for i in entire_array:
        if i == []:
            entire_array.remove(i)
    return (entire_array)

app = Flask(__name__)

firebaseConfig = {
  'apiKey': "AIzaSyCGvp-4gW3nC3fAHmnJDAx3Fbwsdzn_LRQ",
  'authDomain': "espark-356318.firebaseapp.com",
  'databaseURL': "https://espark-356318-default-rtdb.firebaseio.com",
  'projectId': "espark-356318",
  'storageBucket': "espark-356318.appspot.com",
  'messagingSenderId': "615921346526",
  'appId': "1:615921346526:web:6a37c444f53906c90c9f4f"
}
import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("./espark-a18da-firebase-adminsdk-s233j-0ad1627f54.json")
firebase_admin.initialize_app(cred)
fd = firestore.client()
fd.collection('data').document('info').set({'data':1})
@app.route('/sign_in/<input_name>/<input_name_0>/<password>/<email>/<user_type>',methods=['GET'])
def sign_in(input_name,input_name_0,password,email,user_type):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    lastname = input_name_0
    password = password
    email = email
    db.child(f'Users/{input_name}').set({
        'firstname':input_name,
        'lastname':lastname,
        'password':password,
        'email':email,
        'no_of_folders':0,
        'user_type':user_type
    })
    return {
        'firstname':input_name,
        'lastname':lastname,
        'password':password,
        'email':email
    }
@app.route('/get_user_type/<name>',methods=['GET'])
def get_user_type(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        referance = db.child('Users/'+str(name)).get()
        print(referance.val())
        return {"data":dict(referance.val())['user_type']}
    except:
        return {"data":"username not found"}
@app.route('/login/<first_name>',methods=['GET'])
def login(first_name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        referance = db.child('Users/'+str(first_name)).get()
        print(referance.val())
        return {"data":referance.val()['password']}
    except:
        return {"data":"username not found"}
@app.route('/add_folder/<name>/<foldername>',methods=['GET'])
def add_folder(name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        fd.collection(name).document(foldername).set({'foldername':foldername})
        return {'data':'doable'}

    except:
        print('cannot do so')    
        return {'data':"undoable"}
@app.route('/update_no_of_folders/<name>',methods=['GET'])
def update_no_of_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    no_of_folders = db.child(f'Users/{name}/no_of_folders').get().val()
    db.child(f'Users/{name}').update({
        'no_of_folders':int(no_of_folders)+1
    })
    return {'data':200,'no_of_folders':no_of_folders}
@app.route('/get_folders/<name>',methods=['GET'])
def get_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        d = fd.collection(name).get()
        print(d)
        data = []

        for _ in d:
            print("The value im looking for : ")

            print(_.to_dict())
            data.append(_.to_dict()['foldername'])
        return {'data':data}


    except:
        print('cannot do so')
        return {'data':"undoable"}


@app.route('/get_google_content/<query>',methods=['GET'])
def get_google_content(query):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    description_array = []

    df = seo.get_serps(query, pages=3)
    description_array = list(df['text'])
    name_array = list(df['title'])
    site_urls_array = list(df['link'])
    return {
        'description':description_array,
         'names':name_array,
            'urls': site_urls_array
    }

    '''
    jsonified_data = []

    array = [urllib.parse.urlparse(name).netloc for name in list(search(query))]

    page = ''
    pages = []

    for _ in list(search(query)):
        try:
            page = metadata_parser.MetadataParser(_)
            pages.append(page)
        # pages = [metadata_parser.MetadataParser(_) for _ in list(search(query))]
        except:
            jsonified_data.append("The description is hidden by the website")
    print(pages)
    for data in pages:
        try:
            jsonified_data.append(data.metadata['meta']['description'])
        except:
            jsonified_data.append("The description is hidden by the website")

    return {'description': jsonified_data, 'names': array, 'urls': list(search(query))}
'''

@app.route('/add_google_content/<name>/<foldername>/<sourcename>/<sourcepath>/<description>',methods=['GET'])
def add_google_content(name,foldername,sourcename,sourcepath,description):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").document(name+foldername+sourcename).set({'link':sourcepath,'name':sourcename,'delete':False,'type':'google','description':description})
    time.sleep(3)

    return{"status":sourcepath}
@app.route('/add_youtube_content/<name>/<foldername>/<sourcename>/<sourcepath>/<thumbnail>',methods=['GET'])
def add_youtube_content(name,foldername,sourcename,sourcepath,thumbnail):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").document(name+foldername+sourcename).set({'link':'https:``www.youtube.com`watch?v='+sourcepath,'name':sourcename,'delete':False,'type':'youtube','thumbnail':thumbnail})

    return{"status":sourcepath}
@app.route('/get_youtube_data/<query>',methods=['GET'])
def get_youtube_data(query):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    videosSearch = VideosSearch(query, limit = 20).result()

    videosSearch = videosSearch['result']
    titlearray=[]
    thumbnailarray = []
    linkarray = []


    for i in videosSearch:
        print(i)
        titlearray.append(i['title'])
        thumbnailarray.append(i['thumbnails'][0]['url'])
        linkarray.append(i['link'])
    return{
    'titles':titlearray,
    'thumbnail':thumbnailarray,
    'link':linkarray,
    'length':len(titlearray)==len(thumbnailarray)==len(linkarray)
    }
@app.route("/load_data/<name>/<foldername>",methods=['GET'])
def load_data(name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    stored_data = fd.collection(name).document(foldername).collection('content_stored').where(u'delete','==',False).get()
    stored_data = list(stored_data)
    array = []
    for _ in stored_data:
        array.append(_.to_dict())
    print(stored_data)

    return{'data':array}
@app.route('/get_last_name_and_email/<name>',methods=['GET'])
def get_last_name_and_email(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    return {
        'email':db.child(f'Users/{name}/email').get().val(),
        'lastname':db.child(f"Users/{name}/lastname").get().val()
    }
@app.route('/verify_sign_in_information/<email>/<firstname>/<lastname>',methods=['GET'])
def verify_sign_in_information(email,firstname,lastname):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child('Users/').get().val()
    resp = 'good to go!'
    if data:
        for i in data:
            if (data[i]['email']) == (email):
                resp = 'change the associated email to continue,account already exists'
                break
            elif(data[i]['firstname']) == firstname:
                resp = 'Change the given firstname in order to continue'
                break
            elif(data[i]['lastname']) == lastname:
                resp = 'Change the given lastname in order to continue'
                break



        return {
      'data':resp,
      'info':data
    }
    if not data:
        return{
            'data':'good to go!',
            'info':data,
            'status':200
        }
@app.route('/get_stored_links/<name>/<foldername>',methods=['GET'])
def get_stored_links(name, foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    stored_data = fd.collection(name).document(foldername).collection('content_stored').where('delete','==',False).get()
    stored_data = list(stored_data)

    array = []
    for _ in stored_data:
        array.append(_.to_dict())
    name_extracted = []
    title_extracted = []
    print(name_extracted)
    for _ in array:
        name_extracted.append(_['link'])
        title_extracted.append(_['name'])
    print(name_extracted)
    name_extracted_1 = []
    for _ in name_extracted:
        if _ == '`':
            _ = '/'
            print(_)
        name_extracted_1.append(_)
    print(title_extracted)
    return {
        'data':name_extracted_1,
        'names_data':title_extracted
    }
@app.route('/find_similarity_links/<arr1>/<arr2>',methods=['GET'])
def find_similarity_links(arr1,arr2):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    disabled = []
    i1 = 0
    i2 = 0

    arr1 = arr1.split(',')
    arr2 = arr2.split(',')
    print(list(arr1),list(arr2))

    for i in list(arr1):
        if i in list(arr2):
            disabled.append(True)
        else:
            disabled.append(False)
    return{
        'data':disabled
    }
@app.route('/delete_folder/<name>/<foldername>',methods=['GET'])
def delete_folder(name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    d = fd.collection(name).document(foldername).delete()

    return{
        'status':200
    }

@app.route('/delete_saved_data/<name>/<foldername>/<sourcename>',methods=['GET'])
def delete_saved_data(name,foldername,sourcename):
    @after_this_request
    def add_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    _data_ = fd.collection(name).document(foldername).collection('content_stored').document(name+foldername+sourcename)
    _data_.update({'delete':True})
    return {'status':200}
@app.route('/view_student_data_alph_order/<user_type>',methods=['GET'])
def view_student_data_alph_order(user_type):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child('/Users/').get().val()
    data2 = []
    print(data)
    data_names = []
    for i in data:
        if user_type == 'student':
            try:
                if dict(data)[i]['email'].split('@')[1]=='k12.prosper-isd.net':
                    data2.append(dict(data)[i])
                    data_names.append(dict(data)[i]['email'])
            except:
                pass
        if user_type == 'teacher':
            try:
                if dict(data)[i]['email'].split('@')[1]=='prosper-isd.net':
                    data2.append(dict(data)[i])
                    data_names.append(dict(data)[i]['email'])
            except:
                pass
    #last name sort
    graph_data = []

    try:
        bubbleSort(data_names)
        bubbleSortWParam(data2,'email')
        disect_array(data2,data_names)
        result = disect_array(data2,data_names)
        result_1 = []
        for i in result:
            bubbleSortWParam(i,'email')
            result_1.append(i)
        for i in result:
            y = len(i)
            x = i[0]['email'][0]
            graph_data.append({
                'x': x, 'y': y
            })
    except:
        result = [data2]
        for i in result:
            y = len(i)
            x = i[0]['email'][0]
            graph_data.append({
                'x': x, 'y': y
            })
    x,y = '',''

    return{'data':result,'graph_data':graph_data}

@app.route('/get_no_of_stored_content/<name>/<folderarray>',methods=['GET'])
def get_no_of_stored_content(name,folderarray):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    total_yt_data = []
    total_google_data = []
    print('data is'+folderarray)
    for foldername in folderarray.split('-'):
        data = fd.collection(name).document(foldername).collection('content_stored').where('delete','==',False).get()
        print(data)
        data = [i.to_dict() for i in data]
        print(data)
        youtube_data = []
        google_data = []
        for i in data:

            print(i['link'].split('`'))
            if 'www.youtube.com' in i['link'].split('`'):
                youtube_data.append(i)
            else:            google_data.append(i)
        total_yt_data.append(len(youtube_data))
        total_google_data.append(len(google_data))
    return {'data':[total_yt_data,total_google_data]}
@app.route('/delete_no_of_folders/<name>',methods=['GET'])
def delete_no_of_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    no_of_folders = db.child(f'Users/{name}/no_of_folders').get().val()
    db.child(f'Users/{name}').update({
        'no_of_folders': int(no_of_folders) - 1
    })
@app.route('/load_data_by_param/<param>',methods=['GET'])
def load_data_by_param(param):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child('/Users/').get().val()
    student_data =[]
    for i in data:
        try:
            if dict(data)[i]['email'].split('@')[1] == 'k12.prosper-isd.net':
                student_data.append(dict(data)[i][param])
            bubbleSort(student_data)
        except:
            pass
    return {
        'data':student_data
    }
@app.route('/email_to_firstname/<email>',methods=['GET'])
def email_to_firstname(email):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    ref = db.child('Users/').get().val()
    ref = dict(ref)
    data = ''
    for i in ref:
        print(ref[i]['firstname'])
        try:
            if(ref[i]['email']==email):
                data = ref[i]['firstname']
                break
        except:
            pass
    return {
        'data':data
    }
@app.route("/store_timestamp_for_paid_version",methods=['GET'])
def store_timestamp_for_paid_version():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    db.child(f'Users/admin').update({
        'timestamp_payment':str(date.today())
    })
    return {
        'data':str(date.today())
    }
@app.route("/date_subtraction_for_paid_version",methods=['GET'])
def date_subtraction_for_paid_version():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    strfdate = db.child(f"Users/admin/timestamp_payment").get().val()
    print(strfdate)
    strfdate = str(strfdate)
    strfdate = strfdate.split('-')
    array = []
    for i in strfdate:
        array.append(int(i))
    timestamp = date(array[0],array[1],array[2])
    current_date = date.today()
    subtracted_date = current_date-timestamp
    subtracted_date = str(subtracted_date)
    subtracted_date = subtracted_date.split('d')[0]
    return {
        "data":int((subtracted_date).split(':')[0])
    }
@app.route('/get_results_on_conceptual_search/<query>/<name>/<foldername>',methods=['GET'])
def get_results_on_conceptual_search(query,name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    description_array = []
    name_array = []
    link_array = []
    keywords = keyword_extraction(query)[1]
    for i in keywords:
        df = seo.get_serps(i,pages=1)

        description_array.append(list(df['text']))
        name_array.append(list(df['title']))
        link_array.append(list(df['link']))
    data = requests.get(f'http://localhost:8000/get_stored_links/{name}/{foldername}').json()
    stored_data = data['data']
    stored_data_1 = []
    stored_data_2 = []
    index = 0
    for i in stored_data:
        stored_data_1.append(translate_link(i))
    index +=1
    sl = ''
    for i in link_array:
        ta = []
        try:
            for j in i:
                sl = same_link(j,stored_data_1[index])
                ta.append(sl)
            stored_data_2.append(ta)
        except:
            for j in i:
                ta.append(False)
            stored_data_2.append(ta)
    print(type(link_array[0])==type([]))
    jda = []
    jsondata = {
        'link':link_array[0],
        'descriptions':description_array[0],
        'titles':name_array[0],
        'stored_data':stored_data_2[0]
    }
    i = 0
    for link in link_array:
        jda.append(
            {
                'subtopic':keywords[i],
                'link': link,
                'descriptions': description_array[i],
                'titles': name_array[i],
                'stored_data': stored_data_2[i]
            }
        )
        i+=1
    return{
        'data':jda,
    }
@app.route('/enroll_admin/<firstname>/<lastname>/<email>/<password>',methods=['GET'])
def enroll_admin(firstname,lastname,email,password):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    db.child(f'Users/{firstname}').set({
        'firstname':firstname,
        'lastname':lastname,
        'password':password,
        'email':email,
        'user_type':'admin'
    })
    return {
        'data':{
        'firstname':firstname,
        'lastname':lastname,
        'password':password,
        'email':email,
        'user_type':'admin',
        'transactions':[],
        'payment_timestamp':''
    }
    }
@app.route('/monthly_fee',methods=['GET'])
def monthly_fee():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    count = 0
    data = db.child('/Users/').get().val()
    data2 = []
    print(data)
    data_names = []
    for i in data:
        if data[i]['user_type'] == 'student':
            count += 1
    return {'data':count*10,'data_str':str(count*10)}
if __name__=='__main__':
    app.run(debug=True,host="localhost",port=8000)

