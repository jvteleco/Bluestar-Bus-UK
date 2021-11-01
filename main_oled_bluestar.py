#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
OLED display for Bluestar Bus stops

@author: jvteleco

v1.0 


Instructions:
On the bluestar bus webpage, go to your desired bus stop Departures
copy the bus stop code on the URL and paste it in the variable "url_stop_name" 



add to crontab
@reboot sleep 30 && cd /home/pi/FOLDER && /usr/bin/python ./main_oled_bluestar.py &


"""

import SH1106_oled
import time
import traceback
import RPi.GPIO as GPIO

from PIL import Image,ImageDraw,ImageFont

import Bluestar_extract



url_stop_name = "1980SN121003" #Bargate


url_head ="https://www.bluestarbus.co.uk/stops/"
url_joined =url_head + url_stop_name 


#/# Main Variables
status = False
bus_stop_bundle_main = ("","")
bus_info_stop_list_main = []



#GPIO define for keys

##This are defined in SH1106 file
##RST_PIN         = 25
##DC_PIN          = 24
##CS_PIN          = 8
##BL_PIN          = 18

KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16


#init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
## KEYS are Active Low (default idle state is True ('1') )



try:
    disp = SH1106_oled.SH1106()

    # Initialize library.
    disp.Init()
    
    max_width_oled = disp.width

    while(1):
        # Clear display.
        disp.clear()
        print("\r\nBluestar but stop script v1.0")
        
        try:
            status, bus_stop_bundle_main , bus_info_stop_list_main = Bluestar_extract.obtainData(url_joined)
        except Exception as e:
            print("there was an error in Bluestar_extract")
            status = False
            
        if status:
            image1 = Image.new('1', (disp.width, disp.height), "WHITE")
            draw = ImageDraw.Draw(image1)
            font = ImageFont.truetype('Font.ttf', 20)
            font13 = ImageFont.truetype('Font.ttf',13)
            font10 = ImageFont.truetype('Font.ttf',10)
        
        
            draw.text((0,0), "Connecting to ", font = font13, fill = 0)
            draw.text((0,15), "Bluestar Bus...", font = font13, fill = 0)
            disp.ShowImage(disp.getbuffer(image1))     
            time.sleep(2)
            draw.text((0,30), "Info received.", font = font13, fill = 0)
            draw.text((0,45), "Processing...", font = font13, fill = 0)
            disp.ShowImage(disp.getbuffer(image1))  
            time.sleep(2)
            image1.close()
            disp.clear()
            
                
            ##print(bus_stop_bundle_main  )
            ##print(bus_info_stop_list_main)
            
            print("----")
            print("BUS STOP NAME:", bus_stop_bundle_main[0] , "\tBUS NUMBERS:", bus_stop_bundle_main[1] )
            image1 = Image.new('1', (disp.width, disp.height), "WHITE")
            draw = ImageDraw.Draw(image1)
            draw.text((0,0), bus_stop_bundle_main[0], font = font10, fill = 0)
            draw.text((0,15), bus_stop_bundle_main[1], font = font10, fill = 0)
            #image1=image1.rotate(180)
            disp.ShowImage(disp.getbuffer(image1))     
            time.sleep(2)
            image1.close()
            disp.clear()
            
            
            
            index_bus_stop_max = len(bus_info_stop_list_main)
            if index_bus_stop_max > 3:
                bus_info_stop_list_main_solo3 = bus_info_stop_list_main[0:3]
            else:
                bus_info_stop_list_main_solo3 = bus_info_stop_list_main
            #print(bus_info_stop_list_main_solo3)
            
            for bus_info_stop_item in bus_info_stop_list_main_solo3:
                image2 = Image.new('1', (disp.width, disp.height), "WHITE")
                draw2 = ImageDraw.Draw(image2)
                
                
                
                
                
                
                print("BUS NUMBER:", bus_info_stop_item[0] , "\tBUS DIRECTION:", bus_info_stop_item[1]  , "\t\tTIME:", bus_info_stop_item[2])
                
                
                
                #/# This was a test to check if string was too long, if it was required to make it shorter, but it is fine. It will just dissappear to the right.
                #/# If it contains any newline characters, the text is passed on to mulitiline_text() automatically by PIL library
                ###char_maxwidth,  char_maxheight = draw.textsize("123456789012345", font=font10)
                ###print("DEBUG:string of 15 chars= char_maxwidth, char_maxheight:", char_maxwidth, char_maxheight )
                ###print("DEBUG:Bus direction", bus_info_stop_item[1], "Length string:", len(bus_info_stop_item[1]) )
                ###char_maxwidth,  char_maxheight = draw.textsize(bus_info_stop_item[1], font=font10)
                ###print("DEBUG:char_maxwidth, char_maxheight:", char_maxwidth, char_maxheight)
                ###if char_maxwidth > max_width_oled - 10:
                ###    bus_info_stop_item[1] = bus_info_stop_item[1][0:15]  #15 char at size font10 are 90 pixels wide, so OK
                
                bus_info_stop_item[1] = bus_info_stop_item[1][0:max_width_oled]
                draw2.text((0,0), bus_info_stop_item[0], font = font10, fill = 0)
                draw2.text((0,15), bus_info_stop_item[1], font = font10, fill = 0)
                draw2.text((0,30), bus_info_stop_item[2], font = font10, fill = 0)
                #####draw2.text((0,30), "12345678901234567890123456789012345678901234567890", font = font10, fill = 0)
                #####draw2.text((0,45), bus_info_stop_item[2], font = font10, fill = 0)
                #image2=image2.rotate(180)
                disp.ShowImage(disp.getbuffer(image2))     
                time.sleep(3)
                
            
            
            
            
#            #It now show the first entry
#            bus_info_stop_item_0 = bus_info_stop_list_main[0]
#            image2.close()
#            disp.clear()
#            image1 = Image.new('1', (disp.width, disp.height), "WHITE")
#            draw = ImageDraw.Draw(image1)
#            draw.text((0,0), bus_stop_bundle_main[0], font = font10, fill = 0)
#            draw.text((0,15), bus_info_stop_item_0[0], font = font10, fill = 0)
#            draw.text((0,30), bus_info_stop_item_0[1], font = font10, fill = 0)
#            draw.text((0,45), bus_info_stop_item_0[2], font = font10, fill = 0)
            #image1=image1.rotate(180)
#            disp.ShowImage(disp.getbuffer(image1))     
#            time.sleep(5)
            
            
            
            
            index_bus_stop = 0
            index_bus_stop_max = len(bus_info_stop_list_main)    
            #print("MAX", index_bus_stop_max)
            display_time_on=0  #time counter
            busUpdated= True  #First time will show the first bus stop
            firstTime = True
            
            print("DEBUG:starting loop")
            while (1):        
                if GPIO.input(KEY_UP_PIN) == 0:
                    ##button UP pressed
                    if index_bus_stop > 0:
                        #decrease one 
                        index_bus_stop = index_bus_stop -1
                        display_time_on=0
                        busUpdated= True
                        
                        
                if GPIO.input(KEY_DOWN_PIN) == 0:
                    ##button DOWN pressed
                    if index_bus_stop < index_bus_stop_max - 1:
                        #increase one 
                        index_bus_stop = index_bus_stop + 1
                        display_time_on=0
                        busUpdated= True
                            
                
                
                if GPIO.input(KEY1_PIN) == 0:
                    #First stop
                    index_bus_stop = 0
                    display_time_on=0
                    busUpdated= True
                
                if GPIO.input(KEY2_PIN) == 0:
                    print("Exit loop to Refresh bus info")
                    break
                if GPIO.input(KEY_PRESS_PIN) == 0:
                    ##button ENTER pressed
                    print("Exit loop to Refresh bus info")
                    break
                    
                if busUpdated:
                    if firstTime:
                        image1.close()
                        firstTime=False
                    else:
                        image3.close()
                    disp.clear()
                    print("DEBUG:Index:", index_bus_stop)
                    print(bus_info_stop_list_main[index_bus_stop][0], bus_info_stop_list_main[index_bus_stop][1], bus_info_stop_list_main[index_bus_stop][2] )
                    image3 = Image.new('1', (disp.width, disp.height), "WHITE")
                    draw3 = ImageDraw.Draw(image3)
                    draw3.text((0,0), bus_stop_bundle_main[0], font = font10, fill = 0)
                    draw3.text((0,15), bus_info_stop_list_main[index_bus_stop][0], font = font10, fill = 0)
                    draw3.text((0,30), bus_info_stop_list_main[index_bus_stop][1], font = font10, fill = 0)
                    draw3.text((0,45), bus_info_stop_list_main[index_bus_stop][2], font = font10, fill = 0)
                    #image3=image3.rotate(180)
                    disp.ShowImage(disp.getbuffer(image3)) 
                    busUpdated= False                    
                
                
                display_time_on=display_time_on+1
                time.sleep(0.1)
                
                if display_time_on > 1000:
                    print("DEBUG:turning screen off")
                    disp.clear()
                    while GPIO.input(KEY1_PIN) and GPIO.input(KEY2_PIN) and GPIO.input(KEY3_PIN) and GPIO.input(KEY_PRESS_PIN) and GPIO.input(KEY_UP_PIN) and GPIO.input(KEY_DOWN_PIN) and GPIO.input(KEY_LEFT_PIN) and GPIO.input(KEY_RIGHT_PIN):
                        time.sleep(0.1)
                    print("DEBUG:detected a keypress")
                    print("DEBUG:turning screen on")
                    break
                
                
        else:
            print("Status was False")
            print("Trying again in one minute")
            time.sleep(60)


except Exception as e:
    print(e)
    
except KeyboardInterrupt:    
    print("\r\nCtrl + c:")
    GPIO.cleanup()
    disp.module_exit()
    exit()
