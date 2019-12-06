from workspace.models import Record, Log, Crawler
from django.db.models import Q

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta, date
from workspace.engine import Engine

genre_list = ["Blues", "Classical", "Country", "Dance", "Electronic", "Folk", "Hip Hop", "House", "Indie", "Jazz", "Latin", "Metal", "Pop", "Punk", "R&B", "Reggae", "Rock", "World"]

class GreenNote:
    def __init__(self):
        self.url = "https://www.greennote.co.uk/events-page/"
        self.crawler_name = "GreenNote"
        self.crawler_id = 0
        
    def get_urls(self):
        ''' getting urls from source website '''
        source = requests.get(self.url).text
        soup = BeautifulSoup(source,'lxml')
        list_content = soup.find('div',{'class':'et_pb_code_inner'})
        items = list_content.findAll('div',{'class':'wp_theatre_event'})
        url_list = []
        for item in items:
            title = item.find('div',{'class':'wp_theatre_event_title'})
            link = title.find('a')['href']
            ticket = item.find('div',{'class':'wp_theatre_event_tickets'}).text
            status = False
            if ticket.find('Sold out') != -1:
                status = True
            item = {}
            item['link'] = link
            item['soldOut'] = status
            canceled = False
            if ticket.find("Cancelled") != -1:
                canceled = True
            item['canceled'] = canceled
            url_list.append(item)
        return url_list 
    
    def filter_day(self,day_str):
        ''' extracting date from string'''
        array = day_str.split(" ")
        day = array[1]
        day = day.replace("st","")
        day = day.replace("rd","")
        day = day.replace("th","")
        day = day.replace("nd","")
        day = day.zfill(2)
        array[1] = day
        thumbnail = " ".join(str(x) for x in array)
        datetime_object = datetime.strptime(thumbnail, '%a %d %B %I:%M%p')
        return datetime_object
    
    def remove_sp(self,input_str):
        ''' replacing crazy letters '''
#        input_str = input_str.encode('utf-8')
        input_str = input_str.replace(u'\xa0',' ')
        input_str = input_str.replace(u'\x8B','')
        input_str = input_str.replace(u'\x82','')
        input_str = input_str.replace("‘","'")
        input_str = input_str.replace("’","'")
        input_str = input_str.replace("–","-")
        input_str = input_str.replace("—","-")
        input_str = input_str.replace('…','...')
        input_str = input_str.replace(':','')
        input_str = input_str.replace('“','"')
        input_str = input_str.replace('”','"')
#        input_str = input_str.decode('utf-8')
        return input_str
        
    def make_format(self,input_str):
        '''make first letter as uppercase, rest letters as lowercase'''
        parsed = ''
        if len(input_str) > 1:
            array = input_str.split(" ")
            for item in array:
                temp = ''
                if item != '':
                    first_str = item[0].upper()
                    last_str = item[1:].lower()
                    temp = first_str + last_str
                parsed += temp + " "
        parsed = parsed.strip()
        return parsed
    
    def scrape(self):
        today = datetime.now()
        url_list = self.get_urls()
        
        new_url_list = []
        changed_url_list = []
        error_url_list = []
        canceled_url_list = []
        
        crawler = Crawler.objects.get(pk = self.crawler_id)
        last_records = Record.objects.filter(crawler_id = crawler.pk)
        log = Log(status='P',crawler=crawler)
        log.save()
        total_count = 0
        error_count = 0
        new_record = 0
        canceled_count = 0
        changed_record = 0
        filter_list = []
        for url_item in url_list:
            try:
                print(url_item)
                if url_item['link'] in filter_list:
                    print("duplicated !!!-   --------- ")
                    continue
                filter_list.append(url_item['link'])
                sub_source = requests.get(url_item['link']).text
                sub_soup = BeautifulSoup(sub_source,'lxml')
                content = sub_soup.find('div',{'id':'left-area'})
                img = content.find('div',{'class':'et_post_meta_wrapper'})
                img_link = img.find('img')['src']
                title = content.find('h1',{'class':'entry-title'}).text
                title = title.strip()
                venue = ''
                try:
                    venue = content.find('div',{'class':'wp_theatre_event_location'}).text
                    venue = venue.strip()
                except Exception:
                    pass
                date_time_obj = None
                try:
                    date_time = content.find('div',{'class':'wp_theatre_event_datetime'}).text
                    date_time = date_time.strip()
                    date_time_obj = self.filter_day(date_time)
                    if date_time_obj.month < today.month:
                        date_time_obj = date_time_obj.replace(year=today.year+1)
                    else:
                        date_time_obj = date_time_obj.replace(year=today.year)
                except Exception:
                    pass
                price = ''
                try:
                    price = content.find('div',{'class':'wp_theatre_event_prices'}).text
                    price = price.replace("£","")
                    price = price.strip()
                except Exception:
                    pass
                ticket = content.find('div',{'class':'wp_theatre_event_tickets'})
                book_link= ''
                try:
                    book_link = ticket.find('a')['href']
                except Exception:
                    pass

                entry = content.find('div',{'class':'entry-content'})
                divs = entry.findAll('p')
                names = entry.findAll('strong')
                main_act = ''
                support_act = ''
                promoter = ''
                show = ''
                try:
                    main_act = names[0].text
                    main_act = self.make_format(main_act)
                    show = main_act
                except Exception:
                    pass
                try:
                    support_act = names[1].text
                    support_act = self.make_format(support_act)
                    show += " + " + support_act
                except Exception:
                    pass
                try:
                    promoter = names[2].text
                    promoter = self.make_format(promoter)
                except Exception:
                    pass

                description = ''
                for div in divs:
                    description += div.text + "\n"
                description = description.strip()
                
                genre = ""
                for genre_item in genre_list:
                    if description.find(genre_item) != -1:
                        genre += genre_item + ","
                    elif description.find(genre_item.lower()) != -1:
                        genre += genre_item + ","
                genre = genre[:len(genre)-1]
                
                videos = entry.findAll('iframe')
                video_list = []
                for video in videos:
                    video_list.append(video['src'])
                price = price.replace("£","")
                price_float = None
                try:
                    price_float = float(price)
                except Exception:
                    pass
                img_list = []
                img_list.append(img_link)

                show = self.remove_sp(show)
                date_obj = None
                time_obj = ''
                if date_time_obj:
                    date_obj = date_time_obj.date()
                    time_obj = date_time_obj.strftime("%H:%M:%S")

                main_act = self.remove_sp(main_act)
                support_act=self.remove_sp(support_act)
                description = self.remove_sp(description)
                promoter = self.remove_sp(promoter)

                check_record = None
                if last_records:
                    check_record = last_records.filter(info_url=url_item['link'])
                changed_flag = False
                if check_record:
                    change_type = 'C'
                    cur_record = check_record[0]
                    if url_item["canceled"] == True:
                        print("canceled")
                        if cur_record.status != 'C':
                            cur_record.status = 'C'
                            cur_record.save()
                            canceled_count += 1
                            canceled_url_list.append(url_item['link'])
                    if cur_record.date != date_obj:
                        print(cur_record.date)
                        print(date_obj)
                        cur_record.date = date_obj
                        cur_record.date_flag = True
                        changed_flag = True
                        print("1")
                    if cur_record.doors != time_obj:
                        print(cur_record.doors)
                        print(time_obj)
                        cur_record.doors = time_obj
                        cur_record.doors_flag = True
                        changed_flag = True
                        print("2")
                    # elif cur_record.venue != venue:
                    #     cur_record.venue = venue
                    #     cur_record.venue_flag = True
                    #     changed_flag = True
                    #     print("3")
                    # elif cur_record.main_act != main_act:
                    #     cur_record.main_act = main_act
                    #     cur_record.main_act_flag = True
                    #     changed_flag = True
                    #     print("4")
                    # elif cur_record.support_act != support_act:
                    #     cur_record.support_act = support_act
                    #     cur_record.support_act_flag = True
                    #     changed_flag = True
                    #     print("5")
                    # elif cur_record.show_description != description:
                    #     cur_record.show_description = description
                    #     cur_record.show_description_flag = True
                    #     changed_flag = True
                    #     print("6")
                    # elif cur_record.promoter != promoter:
                    #     cur_record.promoter = promoter
                    #     cur_record.promoter_flag = True
                    #     changed_flag = True
                    #     print("7")
                    # elif cur_record.ticket_url != book_link:
                    #     cur_record.ticket_url = book_link
                    #     cur_record.ticket_url_flag = True
                    #     changed_flag = True
                    #     print("8")
                    # elif cur_record.ticket_price != price_float:
                    #     cur_record.ticket_price = price_float
                    #     cur_record.ticket_price_flag = True
                    #     changed_flag = True
                    #     print("9")
                    if cur_record.sold_out != url_item['soldOut']:
                        cur_record.sold_out = url_item['soldOut']
                        cur_record.sold_out_flag = True
                        changed_flag = True
                        print("10")
                    # elif cur_record.listing_main_image != json.dumps(img_list):
                    #     cur_record.listing_main_image = json.dumps(img_list)
                    #     cur_record.listing_main_image_flag = True
                    #     changed_flag = True
                    #     print("11")
                    # elif cur_record.listing_thumbnail != json.dumps(video_list):
                    #     cur_record.listing_thumbnail = json.dumps(video_list)
                    #     cur_record.listing_thumbnail_flag = True
                    #     changed_flag = True
                    #     print("12")
                    if changed_flag == True:
                        cur_record.change_type = change_type
                        cur_record.save()
                        changed_record += 1
                        changed_url_list.append(url_item['link'])
                else:
                    today = date.today() + timedelta(days=1)
                    if today <= date_obj:
                        record = Record(change_type='N', show=show, genre=genre, date=date_obj, doors=time_obj, venue=venue,
                                        main_act=main_act, support_act=support_act, show_description=description,
                                        promoter=promoter, info_url=url_item['link'], ticket_url=book_link,
                                        ticket_price=price_float, sold_out=url_item['soldOut'],status="P",
                                        listing_main_image=json.dumps(img_list), listing_thumbnail=json.dumps(video_list),
                                        crawler=crawler)
                        print("--------------------------- New Record ----------------------------")

                        record.save()
                        new_record += 1
                        new_url_list.append(url_item['link'])
                        print(record.pk)
                total_count += 1
            except Exception:
                error_count += 1
                error_url_list.append(url_item['link'])

        #set number for each status
        log.changed_record = changed_record
        log.new_record = new_record
        log.error_record = error_count
        log.total_record = total_count
        log.canceled_record = canceled_count
        
        # delete expired records.
        t = datetime.today()-timedelta(days=1)
        Record.objects.filter(Q(date__lt=t)).delete()
        
        # generating log details
        detail_json = {}
        detail_json['crawler_id'] = crawler.pk
        detail_json['venue'] = crawler.name
        detail_json['domain'] = crawler.domain
        detail_json['start_time'] = today.strftime("%m/%d/%Y, %H:%M:%S")
        detail_json['end_time'] = datetime.today().strftime("%m/%d/%Y, %H:%M:%S")
        detail_json['new_list'] = new_url_list
        detail_json['changed_list'] = changed_url_list
        detail_json['canceled_list'] = canceled_url_list
        detail_json['error_list'] = error_url_list
        engine = Engine()
        log.detail = engine.generate_log_detail(detail_json)
        log.save()
        
        
        
        
