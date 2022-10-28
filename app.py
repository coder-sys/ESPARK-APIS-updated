from flask import Flask,after_this_request
import time
import metadata_parser
from youtubesearchpython import VideosSearch
import urllib.request
from googlesearch import search
import urllib.parse

from bs4 import BeautifulSoup
import requests




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
@app.route('/sign_in/<input_name>/<input_name_0>/<password>/<email>',methods=['GET'])
def sign_in(input_name,input_name_0,password,email):
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
        'no_of_folders':0
    })
    return {
        'firstname':input_name,
        'lastname':lastname,
        'password':password,
        'email':email
    }

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
@app.route('/add_folder/<name>',methods=['GET'])
def update_no_of_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    no_of_folders = db.child(f'Users/{name}/no_of_folders').get().val()
    db.child(f'Users/{name}').update({
        'no_of_folders':no_of_folders+1
    })
    return {'data':200,'no_of_folders':no_of_folders}
@app.route('/get_folders/<name>')
def get_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        d = fd.collection(name).get()
        print(d)
        data = []
        if len(d)==0:
            return {'data':[]}
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
    jsonified_data = []

    array = [urllib.parse.urlparse(name).netloc for name in list(search(query))]
    array_description = []
    
    page = ''
    pages = []
    for _ in list(search(query)):
        try:
            page = metadata_parser.MetadataParser(_)
            pages.append(page)
        except:
            jsonified_data.append("The description is hidden by the website")
    print(pages)
    for data in pages:
        try:
            jsonified_data.append(data.metadata['meta']['description'])
        except:
            jsonified_data.append("The description is hidden by the website")
    return {'description':jsonified_data,'names':array,'urls': list(search(query)),'equality':len(jsonified_data)==len(array)}
    



@app.route('/add_google_content/<name>/<foldername>/<sourcename>/<sourcepath>',methods=['GET'])
def add_google_content(name,foldername,sourcename,sourcepath):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").document(name+foldername+sourcename).set({'link':sourcepath,'name':sourcename,'delete':False})
    time.sleep(3)
    
    return{"status":sourcepath}
@app.route('/add_youtube_content/<name>/<foldername>/<sourcename>/<sourcepath>',methods=['GET'])
def add_youtube_content(name,foldername,sourcename,sourcepath):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").document(name+foldername+sourcename).set({'link':'https:``www.youtube.com`watch?v='+sourcepath,'name':sourcename,'delete':False})
    
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
        thumbnailarray.append(i['thumbnails'])
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
    stored_data = db.child(f'Users/{name}/email').get().val()
    stored_data1 = db.child(f"Users/{name}/lastname").get().val()
    return {
        'email':stored_data,
        'lastname':stored_data1
    }
@app.route('/verify_sign_in_information/<name>/<lname>',methods=['GET'])
def verify_sign_in_information(name,lname):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child('Users/').get().val()
    resp = '-'
    if data:
        for i in data:
            if (data[i]['lastname']+data[i]['firstname']) == (lname+name):
                resp = 'change either of the names to continue'
                break
            else:
                resp = 'good to go!'
        
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
    def add_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    _data_ = fd.collection(name).document(foldername).collection('content_stored').document(name+foldername+sourcename)
    _data_.update({'delete':True})
    return {'status':200}



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
if __name__=='__main__':
    app.run(debug=True,host="localhost",port=8000)
 
