import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup
#ynqwpxsvypkijyrv
email = os.environ.get('EMAIL')
password = os.environ.get('PASS')
notifiedPlates = False
notifiedMachined = False
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

# //collect stock status of all child products inside grouped product
#         optionStockStatus[7175] = 0 
# 45lb plate ^^
# if set to 0, out of stock, if set to 1, in stock

# urls to be scraped
url1 = "https://www.roguefitness.com/rogue-olympic-plates"

url2 = "https://www.roguefitness.com/rogue-machined-olympic-plates"

# time between checks in seconds
sleepTime = 60

# set the headers like we are a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# # download the homepage
# response = requests.get(url2, headers=headers)
# # parse the downloaded homepage and grab all text, then,
# soup = BeautifulSoup(response.text, "lxml")
# print(soup.get_text().find("optionStockStatus[47219] = 1"))
# splits = soup.get_text().split()
# count = 0
# for word in splits:
#     if word == 'Notify':
#         count += 1

while True:
    
    if not notifiedPlates:
        localTime = str(time.localtime().tm_hour) +':'+ str(time.localtime().tm_min)+':'+ str(time.localtime().tm_sec)+' '+str(time.localtime().tm_mon) +'/'+ str(time.localtime().tm_mday) +'/'+ str(time.localtime().tm_year) 

        # download the homepage
        response1 = requests.get(url1, headers=headers)
        # parse the downloaded homepage and grab all text
        soup1 = BeautifulSoup(response1.text, "lxml")

        # This is checking for 45lb plates
        if soup1.get_text().find("optionStockStatus[7175] = 1") == -1:
            print("Iron Plates out of stock at", localTime)

        else:
            print("Iron Plates in stock at", localTime)
            subject = "Plates in Stock!"
            body = "4x 45, 1x 25, 2x 10, 1x 5\n\n"+url1
            sendEmail(subject, body)
            notifiedPlates = True
        
    if not notifiedMachined:

        # download the homepage
        response2 = requests.get(url2, headers=headers)
        # parse the downloaded homepage and grab all text
        soup2 = BeautifulSoup(response2.text, "lxml")
        
        # This is checking for 45lb plates
        if soup2.get_text().find("optionStockStatus[47219] = 1") == -1:  
            localTime = str(time.localtime().tm_hour) +':'+ str(time.localtime().tm_min)+':'+ str(time.localtime().tm_sec)+' '+str(time.localtime().tm_mon) +'/'+ str(time.localtime().tm_mday) +'/'+ str(time.localtime().tm_year) 

            print("Machined plates out of stock at", localTime)
            
        else:
            print("Machined Plates in stock at", localTime)
            subject = "Machined Plates in Stock!"
            body = "4x 45, 1x 25, 2x 10, 1x 5\n\n"+url2
            sendEmail(subject, body)
            notifiedMachined = True
    
    if notifiedPlates and notifiedMachined:
        print("Both plates in stock! Program terminating.")
        break
        
    time.sleep(sleepTime)

