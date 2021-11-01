#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Created on Mon Aug 19 08:42:15 2019
Nov 2021: Updated to python3 and new bus stop format

@author: jvteleco
"""

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

import urllib
from urllib.request import urlopen
import re


MAX_NUMBER_TO_SHOW = 10

url_stop_name = "1980SN121003" #Bargate


url_head ="https://www.bluestarbus.co.uk/stops/"
url_joined =url_head + url_stop_name 


#/# Main Variables
status = False
bus_stop_bundle_main = ("","")
bus_info_stop_list_main = []


def obtainData(url):
    bus_stop_bundle = ("","")
    bus_info_stop_list = []
    
    print("Obtaining data from url", url, "...\r\n")


    try:
        connection = urllib.request.urlopen(url)
        html = connection.read()
        connection.close()
        
        
        
        ###print(html)
        
        #/# To Debug and check the HTML
        #f= open("bluestarbus_response.html","w")
        #f.write(html)
        #f.close()
         
        parsed_html = BeautifulSoup(html)
        #parsed_html = BeautifulSoup(html, "lxml")
        ###print(parsed_html.body)
    except Exception as e:
        print("There was an error during the connection"  )
        print(e)        
        return False, ("",""), []



    try:
        print("Converting data...")
        #/# Need to get bus stop info from   single-stop__header
        #bus_stop_header = parsed_html.body.find('div', attrs={'class':'single-stop__header'})
        bus_stop_header = parsed_html.body.find('h1', attrs={'class':'place-info-banner__name'})
        #print(bus_stop_header)
        #print(bus_stop_header.contents)
        #print(bus_stop_header.text)
        
        
        
        #/# The bust stop name is in   h1 class="place-info-banner__name"
        ###bus_stop_header.find('h1', attrs={'class':'place-info-banner__name'})
        
        ##bus_stop_header.h1.contents
        #bus_stop_name = bus_stop_header.h1.contents[0]
        bus_stop_name_1 = bus_stop_header.contents[0].strip()
        bus_stop_name_2 = bus_stop_header.contents[1].text.strip()
        #print(bus_stop_name_1)
        #print(bus_stop_name_2)
        
        bus_stop_name = bus_stop_name_1 + "," + bus_stop_name_2
        
        #OLD WEBSITE; had numbers of buses, eg:  3,16,18. 
        #bus_stop_number_header = parsed_html.body.find('p', attrs={'class':'place-info-banner__meta'})
        #bus_stop_name_code = bus_stop_number_header.text
        
        #bus_stop_name = bus_stop_name.strip()
        #print("BUS STOP NAME:", bus_stop_name , "CODE:", bus_stop_name_code)
        
        
        #2021 now they are blue buttons:
        #<div class="place-info-banner__row">  
        #  <ul                  class="place-info-banner__block-list
        bus_stop_number_header = parsed_html.body.find('ul', attrs={'class':'place-info-banner__block-list'})
        
        buses_stop_list_li = bus_stop_number_header.find_all('li')
        bus_stop_name_code =""
        
        for child in buses_stop_list_li:
            bus_stop_name_code = bus_stop_name_code + child.text.strip() + " "
         
        
        bus_stop_bundle = (bus_stop_name, bus_stop_name_code)
        
        
        
        
        #/# Now grab departure buses and times
        single_stop_body = parsed_html.body.find('div', attrs={'class':'single-stop__body'})
        
        #/# Sometime they are div class="single-visit"  and others they are   a class="single-visit"
        ###all_bus_items = single_stop_body.findAll("div", "single-visit")
        
        list_elements= single_stop_body.div.contents

        all_bus_items = []  
        for item in list_elements:
            if len(item) > 1:
                #only save "good ones" 
                all_bus_items.append(item)
                ####print(item.find("div", "single-visit") )
                ####print(item.find("a", "single-visit")  )

            
        
        if len(all_bus_items) == 0:
            print("ERROR, no info.")
            print("try again in 1 minute or recheck bus stop name")
            
        else:
            #/# Truncate to the next 5 buses
            #print(all_bus_items)
            #print(len(all_bus_items))
        
            if len(all_bus_items) > MAX_NUMBER_TO_SHOW:
                all_bus_items= all_bus_items[0:MAX_NUMBER_TO_SHOW]
            
            #need to now separate by "single-visit" items
            for item in all_bus_items:
                ###print(item)
                #bus_info = item.find('div', attrs={'class':'single-visit__content'})
                #print(bus_info)
                bus_info_stop_number= item.find('p', attrs={'class':'single-visit__name'}).text
                bus_info_stop_name= item.find('p', attrs={'class':'single-visit__description'}).text
                
                
                bus_info_stop_time_list = item.find('div', attrs={'class':'single-visit__time'})
                #/# If it is realtime,  <div class="single-visit__time single-visit__time--expected"> 59 mins</div>
                #/# If it not realtime  <div class="single-visit__time single-visit__time--aimed"> 10:06</div>    
                ###print(bus_info_stop_time_list)
                bus_info_stop_time_text = bus_info_stop_time_list.text
                bus_info_stop_time_text= bus_info_stop_time_text.strip()
        
                #print("BUS NUMBER:", bus_info_stop_number, "BUS_NAME", bus_info_stop_name  , "TIME:", bus_info_stop_time_text     )
                bus_info_stop_list.append( [bus_info_stop_number, bus_info_stop_name, bus_info_stop_time_text]  )        

        return True, bus_stop_bundle, bus_info_stop_list
    except Exception as e:
        print("There was an error finding the bus info, probably wrong bus url code")
        print(e)
        return False, ("",""), []


if __name__ == '__main__':
    status, bus_stop_bundle_main, bus_info_stop_list_main = obtainData(url_joined)
    if status:
        ##print(bus_stop_bundle_main  )
        ##print(bus_info_stop_list_main)
        
        print("----" )
        print("BUS STOP NAME:", bus_stop_bundle_main[0] , "\tBUS NUMBERS:", bus_stop_bundle_main[1] )
        for bus_info_stop_item in bus_info_stop_list_main:
            print("BUS NUMBER:", bus_info_stop_item[0] , "\tBUS DIRECTION:", bus_info_stop_item[1]  , "\t\tTIME:", bus_info_stop_item[2] )
    else:
        print("Status was False")
        
