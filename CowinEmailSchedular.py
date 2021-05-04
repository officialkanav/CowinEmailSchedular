# Instructions
# Step1: pip3 install requests
# Step2: Enter your email and password in line 27 and 28
# Step2: cd Command Prompt/Terminal to this file's folder and run python3 CowinEmailSchedular.py
# Step3: Follow the instructions in command prompt (Don't repeat your email here)
from datetime import date
import requests
import json
import smtplib
import time

def print_states():
  states_url = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
  r = requests.get(states_url).content.decode('utf8').replace("'", '"')
  states = json.loads(r)
  for state in states['states']:
    print(state['state_name'], ': ', state['state_id'])

def print_districts(state_id):
  districts_url = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/%s' %(state_id)
  r = requests.get(districts_url).content.decode('utf8').replace("'", '"')
  districts = json.loads(r)
  for district in districts['districts']:
    print(district['district_name'], ': ', district['district_id'])

def sendEmail(bodyList, email):
  gmail_user = 'ENTER YOU EMAIL HERE'
  gmail_password = 'ENTER EMAILs PASSWORD'

  sent_from = gmail_user
  to = [email]
  subject = 'Cowin Vaccine Available'
  body = '\n\n\n'.join(bodyList)
  try:
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.ehlo()
      server.login(gmail_user, gmail_password)
      server.sendmail(sent_from, to, body)
      server.close()

  except:
      print ('Something went wrong...\n Stop the script')

def start(district_id, email, min_age):
  while True:
    body = []
    today = date.today()
    request_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=%s&date=%s' %(district_id, today.strftime("%d-%m-%Y"))
    r = requests.get(request_url).content.decode('utf8').replace("'", '"')
    data = json.loads(r)
    centers = data['centers']
    for center in centers:
      for session in center['sessions']:
        if int(session['min_age_limit']) == min_age and int(session['available_capacity']) > 0:
          body.append('Vaccine available at %s, %s \n Date:%s, Availability: %s' %(center['block_name'], center['name'], session['date'], session['available_capacity']))
    if len(body) > 0:
      sendEmail(body, email )
    print('Number of vaccination sessions found: ', len(body))
    time.sleep(1800)

print('\n')
time.sleep(3)
print_states()
state_id = input('\n\nEnter StateId: ')
print('\n\n')
print_districts(state_id)
district_id = input('\n\nEnter DistrictId: ')
email = input('\n\nEnter EmailId: ')
min_age = input('\n\nEnter Minimum Age(Either 18 for 18+ or 45 for 45+): ')
print('\n\n')
start(district_id, email, int(min_age))
