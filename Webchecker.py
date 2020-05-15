import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup

email = os.environ.get('EMAIL')
password = os.environ.get('PASS')
# time between checks in seconds
sleepTime = 60

# set the headers like we are a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def sendEmail(subject, body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email, password)

        msg = f'Subject: {subject}\n\n{body}'

        # logging.info('Sending Email...')
        smtp.sendmail(email, email, msg)
        smtp.quit()


# use this to find what to check for in a page
def printPage(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    print(soup.get_text())


def checkStatus(name, description, url, checkFor):
    localTime = str(time.localtime().tm_hour) +':'+ str(time.localtime().tm_min)+':'+ str(time.localtime().tm_sec)+' '+str(time.localtime().tm_mon) +'/'+ str(time.localtime().tm_mday) +'/'+ str(time.localtime().tm_year) 

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    if soup.get_text().find(checkFor) == -1:
        print(name+" out of stock at", localTime)
        return False
    else:
        print(name+" in stock at", localTime)
        subject = name+" in Stock!"
        body = description+"\n\n"+url
        sendEmail(subject, body)
        return True
# add new stuff here in the format:
# thing = ("name", "description", "url", "checkfor", False) <-- Should all be strings except for the last index which is False
ironPlates = ("Iron plates", "4x 45, 1x 25, 2x 10, 1x 5", "https://www.roguefitness.com/rogue-olympic-plates", "optionStockStatus[7175] = 1", False)
machinedPlates = ("Machined plates", "4x 45, 1x 25, 2x 10, 1x 5", "https://www.roguefitness.com/rogue-machined-olympic-plates", "optionStockStatus[47219] = 1", False)
coloredBumpers = ("Colored bumpers", "4x 45, 1x 25, 2x 10, 1x 5", "https://www.roguefitness.com/rogue-color-echo-bumper-plate", "optionStockStatus[45192] = 1", False)
dumbbells = ("20 lb dumbbells", "Get it!", "https://www.roguefitness.com/rogue-dumbbells","optionStockStatus[7109] = 1", False)
# don't forget to add to list below after
things = [ironPlates, machinedPlates, coloredBumpers, dumbbells]

while True:
    newThings = []
    nothing = True # if have been notified for everything
    for name, desc, url, check, notified in things:
        notif = notified
        if not notified:
            nothing = False
            if checkStatus(name, desc, url, check):
                notif = True
        new = (name, desc, url, check, notif)
        newThings.append(new)
    if nothing:
        print("Everything is in stock and you have been notified. Program terminating.")
        break
    things = newThings
    time.sleep(sleepTime)

