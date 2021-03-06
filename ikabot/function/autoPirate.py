#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import sys
import requests
import re
import traceback
from ikabot.helpers.pedirInfo import *
from ikabot.helpers.gui import *
from ikabot.config import *
from ikabot.helpers.getJson import *
from ikabot.helpers.botComm import *
from ikabot.helpers.varios import wait
from ikabot.helpers.process import run


t = gettext.translation('buyResources',
                        localedir,
                        languages=languages,
                        fallback=True)
_ = t.gettext

def autoPirate(session, event, stdin_fd):
    """
    Parameters
    ----------
    session : ikabot.web.session.Session
    event : multiprocessing.Event
    stdin_fd: int
    """
    sys.stdin = os.fdopen(stdin_fd)
    banner()
    print('{}⚠️ USING THIS FEATURE WILL EXPOSE YOUR IP ADDRESS TO A THIRD PARTY FOR CAPTCHA SOLVING ⚠️{}\n\n'.format(bcolors.WARNING, bcolors.ENDC))
    print('How many pirate raid should I do? (min = 1)')
    pirateCount = read(min = 1, digit = True)
    print('Do you want me to automatically conver all capture points to crew strength? (Y|N)')
    autoConvert = read(values = ['y','Y','n','N'])

    print('YAAAAAR!') #get data for options such as auto-convert to crew strength, time intervals, number of piracy attempts...
    enter()
    event.set()
    try:
        while (pirateCount > 0):
            pirateCount -= 1
            banner()
            piracyCities = getPiracyCities(session)
            html = session.post(city_url + str(piracyCities[0]['id'])) #this is needed because for some reason you need to look at the town where you are sending a request from in the line below, before you send that request
            if '"showPirateFortressShip":0' in html: # this is in case the user has manually run a capture run, in that case, there is no need to wait 150secs instead we can check every 5
                wait(5)
                pirateCount += 1 #don't count this as an iteration of the loop
                continue
            url = 'action=PiracyScreen&function=capture&buildingLevel={0}&view=pirateFortress&cityId={1}&position=17&activeTab=tabBootyQuest&backgroundView=city&currentCityId={1}&templateView=pirateFortress&actionRequest={2}&ajax=1'.format(piracyCities[0]['position'][17]['level'], piracyCities[0]['id'], actionRequest)
            html = session.post(url)
            
            if 'Security word:' in html:
                try:
                    for i in range(20):
                        if i == 19:
                            raise Exception("Failed to resolve captcha too many times")
                        picture = session.s.get(session.urlBase + 'action=Options&function=createCaptcha').content
                        captcha = resolveCaptcha(picture)
                        if captcha == 'Error':
                            continue
                        session.post(city_url + str(piracyCities[0]['id']))
                        params = {'action': 'PiracyScreen', 'function': 'capture', 'cityId': piracyCities[0]['id'], 'position': '17', 'captchaNeeded': '1', 'buildingLevel': piracyCities[0]['position'][17]['level'], 'captcha': captcha, 'activeTab': 'tabBootyQuest', 'backgroundView': 'city', 'currentCityId': piracyCities[0]['id'], 'templateView': 'pirateFortress', 'actionRequest': actionRequest, 'ajax': '1'}
                        html = session.post(payloadPost = params, noIndex = True)
                        if '"showPirateFortressShip":1' in html: #if this is true, then the crew is still in the town, that means that the request didn't succeed
                            continue
                    
                        break
                except Exception:
                    info=''
                    msg = _('Error in:\n{}\nCause:\n{}').format(info, traceback.format_exc())
                    sendToBot(session, msg)
                    break
            if autoConvert.lower() == 'y':
                convertCapturePoints(session, piracyCities)
            wait(150)

    except Exception:
        event.set
        return

def resolveCaptcha(picture):
    
    text = run('nslookup -q=txt ikagod.twilightparadox.com ns2.afraid.org').decode('utf-8').strip()
    address = text.split('"')[1] #in the future this will be only 1 option out of multiple such as 9kw.eu and anti-captcha, 2captcha etc...

    files = {'upload_file': picture}
    captcha = requests.post('http://{0}'.format(address), files=files).text
    return captcha
    

def getPiracyCities(session):
	"""Gets all user's cities which have a pirate fortress in them
	Parameters
	----------
	session : ikabot.web.session.Session

	Returns
	-------
	piracyCities : list[dict]
	"""
	cities_ids = getIdsOfCities(session)[0]
	piracyCities = []
	for city_id in cities_ids:
		html = session.get(city_url + city_id)
		city = getCity(html)
		for pos, building in enumerate(city['position']):
			if building['building'] == 'pirateFortress':
				piracyCities.append(city)
				break
	return piracyCities

def convertCapturePoints(session, piracyCities):
    """Converts all the users capture points into crew strength
	Parameters
	----------
	session : ikabot.web.session.Session
    piracyCities: a list containing all cities which have a pirate fortress
	"""
    html = session.get('view=pirateFortress&activeTab=tabCrew&cityId={0}&position=17&backgroundView=city&currentCityId={0}&templateView=pirateFortress'.format(piracyCities[0]['id']))
    rta = re.search(r'\\"capturePoints\\":\\"(\d+)\\"', html)
    capturePoints = int(rta.group(1))
    if 'conversionProgressBar' in html: #if a conversion is still in progress
        return
    data = {'action': 'PiracyScreen', 'function': 'convert', 'view': 'pirateFortress', 'cityId': piracyCities[0]['id'], 'islandId': piracyCities[0]['islandId'], 'activeTab': 'tabCrew', 'crewPoints': str(int(capturePoints/10)), 'position': '17', 'backgroundView': 'city', 'currentCityId': piracyCities[0]['id'], 'templateView': 'pirateFortress', 'actionRequest': actionRequest, 'ajax': '1'}
    html = session.post(payloadPost = data, noIndex = True)