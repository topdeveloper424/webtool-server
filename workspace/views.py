from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,Http404
from django.conf import settings

import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime,date
import csv
from pymongo import MongoClient
import urllib.parse
from workspace.green_note import GreenNote
from workspace.models import Crawler, Log, Record

username = urllib.parse.quote_plus('alex')
password = urllib.parse.quote_plus('qzTXeMwD')
api_url = "https://camden-api.v8.lionwood.software/api/v1/"
#dbcon = MongoClient('mongodb://3.9.162.15:27017',username=username,password=password,authSource='camden-dev')
dbcon = MongoClient('mongodb://alex:qzTXeMwD@3.9.162.15:27017/camden-dev')
mydb = dbcon.get_database()
print(mydb.name)

# Create your views here.

###################################################### Page views #######################################################
def home(request):
    crawlers = Crawler.objects.all()
    logs = Log.objects.all().order_by('-run_time')
    return render(request,'home.html',{'crawlers':crawlers,'logs':logs})

def log_view(request):
    log_id = request.GET['log_id']
    try:
        log = Log.objects.get(pk=log_id)
        crawler_id = log.crawler.id
        logs = Log.objects.filter(crawler_id=crawler_id).order_by('-run_time')
        return render(request,'log-view.html',{'logs':logs,'crawler':log.crawler})
    except Exception:
        return redirect("workspace:home")
    
def log_detail(request):
    log_id = request.GET['log_id']
    try:
        log = Log.objects.get(pk=log_id)
        return render(request, 'log-detail.html',{'detail':log.detail})
    except Exception:
        return redirect("workspace:home")
        
def review(request):
    mode = None
    try:
        mode = request.GET['mode']
    except Exception:
        pass
    try:
        crawler_id = request.GET['crawler_id']
        log = Log.objects.filter(crawler_id=crawler_id).latest('pk')
        records = Record.objects.filter(crawler_id=crawler_id).order_by('date')
        return render(request,'review.html',{'records':records,'log':log,'mode':mode})
    except Exception:
        pass
    log_id = request.GET['log_id']
    log = Log.objects.get(pk=log_id)
    records = None
    if mode:
        if int(mode) == 1:
            records = Record.objects.filter(crawler_id=log.crawler_id,status='A').order_by('date')
        else:
            records = Record.objects.filter(crawler_id=log.crawler_id).order_by('date')
    else:
        records = Record.objects.filter(crawler_id=log.crawler_id).order_by('date')

    return render(request,'review.html',{'records':records,'log':log,'mode':mode})


def edit_script(request):
    crawler_id = request.GET['crawler_id']
    crawler = Crawler.objects.get(pk=crawler_id)
    file_path = settings.BASE_DIR + "/workspace/" + crawler.script
    file_content = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as fout:
            file_content = fout.read()
    return render(request,'edit-script.html',{'file_content':file_content,'crawler_id':crawler_id})

def source(request):
    return render(request, 'source.html')

######################################################## end page view code section ##############################################

@csrf_exempt
def crawl_now(request):
    crawler_id = request.POST['crawler_id']

    crawl(crawler_id)
    response={}
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")


def crawl(crawler_id):
    crawler = Crawler.objects.get(pk=crawler_id)
    if crawler.running_flag == False:
        crawler.running_flag = True
        crawler.save()
        if crawler.name == 'GreenNote':
            green_note = GreenNote()
            green_note.crawler_id = crawler_id
            green_note.scrape()
        crawler.running_flag = False
        crawler.save()

@csrf_exempt
def delete_log(request):
    log_id = request.POST['log_id']
    Log.objects.get(pk=log_id).delete()
    response={}
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def save_script(request):
    crawler_id = request.POST['crawler_id']
    file_content = request.POST['file_content']
    crawler = Crawler.objects.get(pk=crawler_id)
    file_path = settings.BASE_DIR + "/workspace/" + crawler.script
    if os.path.exists(file_path):
        with open(file_path, "w", encoding='utf-8') as writer:
            writer.write(file_content)

    response={}
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def get_source(request):
    record_id = request.POST['record_id']
    record = Record.objects.get(pk=record_id)
    url = record.info_url
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    content = soup.find('div',{'id':'main-content'})
    sidebar = content.find('div',{'id':'sidebar'})
    content_source = content.decode_contents(formatter="html")
    sidebar_contents = sidebar.decode_contents(formatter="html")
    content_source = content_source.replace(sidebar_contents,"")

    response = {}
    response['source'] = content_source


    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def approve(request):
    response={}
    try:
        log_id = request.POST['log_id']
        log = Log.objects.get(pk=log_id)
        log.status = 'A'
        log.save()
        
        checked_array = request.POST['checked_array']
        checked_list = json.loads(checked_array)
        for checked_id in checked_list:
            record = Record.objects.get(pk=int(checked_id))
            record.status = 'A'
            record.save()
            
    except Exception:
        pass
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

def convert_str_datetime(date_str):
    date_processing = date_str.replace('T', '-').replace(':', '-').split('-')
    date_processing = [int(v) for v in date_processing]
    date_out = datetime(*date_processing)
    return date_out

@csrf_exempt
def save_record(request):
    response={}
    record_id = request.POST['record_id']
    record = Record.objects.get(pk=record_id)
    try:
        show = request.POST['show']
        record.show = show
    except Exception:
        pass
    try:
        date_str = request.POST['date']
        date_obj = datetime.strptime(date_str,'%Y-%m-%d')
        record.date = date_obj
    except Exception:
        pass
    try:
        doors = request.POST['doors']
        record.doors = doors
    except Exception:
        pass
    try:
        date_str = request.POST['mainActShowTime']
        mainActShowTime = convert_str_datetime(date_str)
        record.main_act_show_time = mainActShowTime
    except Exception:
        pass
    try:
        mainAct = request.POST['mainAct']
        record.main_act = mainAct
    except Exception:
        pass
    try:
        genre = request.POST['genre']
        record.genre = genre
    except Exception:
        pass
    try:
        supportAct = request.POST['supportAct']
        record.support_act = supportAct
    except Exception:
        pass
    try:
        promoter = request.POST['promoter']
        record.promoter = promoter
    except Exception:
        pass
    try:
        festival = request.POST['festival']
        record.festival = festival
    except Exception:
        pass
    try:
        description = request.POST['description']
        record.show_description = description
    except Exception:
        pass
    try:
        ticketPrice = request.POST['ticketPrice']
        price = float(ticketPrice)
        record.ticket_price = price
    except Exception:
        pass
    try:
        date_str = request.POST['ticketOnsalDate']
        time_str = request.POST['ticketOnsalTime']
        temp = date_str+"@"+time_str
        print(temp)
        ticketOnsalDatetime = datetime.strptime(temp,'%Y-%m-%d@%H:%M')
        record.ticket_onsale_datetime = ticketOnsalDatetime
    except Exception:
        pass
    try:
        ticketsAtDoorOnly = request.POST['ticketsAtDoorOnly']
        door_bool = False
        if ticketsAtDoorOnly == 'True':
            door_bool = True
        record.tickets_at_door_only = door_bool
    except Exception:
        pass
    try:
        free = request.POST['free']
        free_bool = False
        if free == 'True':
            free_bool = True
        record.free = free_bool
    except Exception:
        pass
    try:
        soldout_str = request.POST['soldOut']
        soldOut = False
        if soldout_str == 'True':
            soldOut = True
        record.sold_out = soldOut

    except Exception:
        pass
    try:
        showType = request.POST['showType']
        record.show_type = showType
    except Exception:
        pass
    try:
        listingMainImage = request.POST['listingMainImage']
        record.listing_main_image = listingMainImage
    except Exception:
        pass
    try:
        listingThumnail = request.POST['listingThumnail']
        record.listing_thumbnail = listingThumnail
    except Exception:
        pass

    try:
        venue = request.POST["venue"]
        record.venue = venue
    except Exception:
        pass
    record.save()

    response['response'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

def db_process(record):

    support_actors = record.support_act
    support_array = []
    if support_actors.strip() != '':
        temp_array = support_actors.split(",")
        for item in temp_array:
            if item.strip() != '':
                support_array.append(item)
    
    date_str = ''
    date_object = None
    if record.date:
        date_str = record.date.strftime("%Y-%m-%dT")
        if record.doors and record.doors != "":
            date_str += record.doors
        else:
            date_str += "00:00:00"
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    main_act_show_time = record.main_act_show_time
    if main_act_show_time:
        main_act_show_time = record.main_act_show_time
    else:
        main_act_show_time = datetime.today().utcnow()

    on_sale_soon = record.on_sale_soon
    if on_sale_soon == None:
        on_sale_soon = False


    created_date = datetime.today().utcnow()
    
        
    listing_data = { 
        "Show" : record.show, 
        "Date" : date_object, 
        "Doors" : date_object, 
        "VenueName" : record.venue, 
        "VenueAddress" : "", 
        "Genres" : record.genre,
        "MainActShowTime" : main_act_show_time, 
        "MainActName" : record.main_act, 
        "SupportActs" : support_array, 
        "ShowDescription" : record.show_description, 
        "PromoterName" : record.promoter, 
        "FestivalName" : record.festival, 
        "InfoURL" : record.info_url, 
        "TicketURL" : record.ticket_url, 
        "TicketsOnSaleDate" : record.ticket_onsale_datetime, 
        "TicketsOnSaleTime" : record.ticket_onsale_datetime, 
        "TicketsOnDoors" : record.tickets_at_door_only, 
        "TicketsOnSaleSoon" : on_sale_soon,
        "TicketsFree" : record.free, 
        "TicketsSoldOut" : record.sold_out,
        "ShowType" : "",
        "CreatedAt" : created_date,
        "UpdatedAt" : created_date
    }
    insert_listing(listing_data)
            
                    
    record.status = 'S'
    record.save()


@csrf_exempt
def send_import(request):
    response={}
    try:
        log_id = request.POST['log_id']
        log = Log.objects.get(pk=log_id)
        log.status = 'S'
        log.save()
        checked_array = request.POST['checked_array']
        checked_list = json.loads(checked_array)
        for checked_id in checked_list:
            record = Record.objects.get(pk=int(checked_id))
            db_process(record)
    except TimeoutError:
        pass
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def approve_record(request):
    response = {}
    record_id = request.POST['record_id']
    try:
        record = Record.objects.get(pk=int(record_id))
        record.status = 'A'
        record.save()
    except Exception:
        pass
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def send_record(request):
    response = {}
    record_id = request.POST['record_id']
    log_id = request.POST['log_id']
    try:
        record = Record.objects.get(pk=int(record_id))
        db_process(record)
        record.status = 'S'
        record.save()
    except TimeoutError:
        pass
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def delete_record(request):
    response = {}
    record_id = request.POST['record_id']
    log_id = request.POST['log_id']
    try:
        record = Record.objects.get(pk=int(record_id))
        record.status = 'D'
        record.save()
    except Exception:
        pass
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def cancel_record(request):
    response = {}
    record_id = request.POST['record_id']
    log_id = request.POST['log_id']
    try:
        record = Record.objects.get(pk=int(record_id))
        record.status = 'P'
        record.save()
    except Exception:
        pass
    response['status'] = 'success'
    return HttpResponse(json.dumps(response),content_type="application/json")



##################################################### DATABASE PROCESS ##################################################################

def get_actor_id(actor_name):
    actor_collection = mydb.Actor
    print("-------------------insert actor--------------------")
    data = {"Name": actor_name}
    print(data)
    actors = actor_collection.find(data)
    if actors.count() > 0:
        cur_id = actors[0]['_id']
        return cur_id
    x = actor_collection.insert_one(data)
    new_id = x.inserted_id
    print(str(new_id))
    return new_id

def get_promoter_id(promoter_name):
    promoter_collection = mydb["Promoter"]
    print("-------------------insert promoter--------------------")

    data = {"Name": promoter_name}
    print(data)
    promoters = promoter_collection.find(data)
    if promoters.count() > 0:
        cur_id = promoters[0]['_id']
        return cur_id
    x = promoter_collection.insert_one(data)
    new_id = x.inserted_id
    print(str(new_id))
    return new_id

def get_venue_id(venue_name,website):
    venue_collection = mydb["Venue"]
    print("-------------------insert venue--------------------")
    data = {"Name": venue_name, "Website": website}
    print(data)
    venues = venue_collection.find({"Name": venue_name})
    if venues.count() > 0:
        cur_id = venues[0]['_id']
        return cur_id
    x = venue_collection.insert_one(data)
    new_id = x.inserted_id
    print(str(new_id))
    return new_id

def get_festival_id(festival_data):
    festival_collection = mydb["Festival"]
    print("-------------------insert festival--------------------")

    festivals = festival_collection.find({"Name": festival_data["Name"]})
    print(festival_data)
    if festivals.count() > 0:
        cur_id = festivals[0]['_id']
        return cur_id
    x = festival_collection.insert_one(festival_data)
    new_id = x.inserted_id
    print(str(new_id))
    return new_id

def insert_listing(listing_data):
    listing_collection = mydb["ParsedListings"]
    print("-------------------insert listing--------------------")
    print(listing_data)
    x = listing_collection.insert_one(listing_data)
    new_id = x.inserted_id
    print(str(new_id))
    return new_id
