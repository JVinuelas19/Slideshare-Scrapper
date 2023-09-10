from bs4 import BeautifulSoup as bs
from PIL import Image
import requests
import shutil
import time
import random
import os

#This script downloads all the images from the book selected from slideshare.net and
#creates a PDF with the images downloaded
#It uses basic ways to scrap safely such as a time randomizer between requests and random 
#headers to avoid being banned from the website
#Use with your own discretion and please don't profit with it. 

#We will set the directory and filename to use it with no absolute paths
dirname=os.path.dirname(__file__)
filename=os.path.join(dirname, 'Book')

#To avoid straight bans we will change the Python header between these 3. You can add more if you wish to
header1 = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64)' 
           'AppleWebKit/537.36 (KHTML, like Gecko)'
           'Chrome/79.0.3945.88 Safari/537.36'
          },
header2 = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)'
           'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148' 
           'Safari/604.1'
          }
header3 = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X)'
           'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148'
           'Safari/604.1'
          }
header_list = [header1, header2, header3]
length_header_list = len(header_list)-1

#Ask for the URL and converts the book contained to a PDF file
url=input('Paste the URL book or slides from slideshare.net :')
page = requests.get(url)
soup = bs(page.content, 'html.parser')
pages = soup.find_all('picture')
page_number=0
im_1= Image.new("RGB", (1920, 1080))
page_list = []
for page in pages:
    page_string = str(page)
    page_strings = page_string.split()
    index = 0
    for strings in page_strings:
        if strings == '2048w"':
            value = index-1 
            image = page_strings[value]
            r = requests.get(image, stream = True, headers=header_list[random.randint(0,length_header_list)])
            if(r.status_code == 200):
                r.raw.decode_content = True
                #with open (f"{filename}/imagen{page_number}.jpeg", 'wb') as f:
                with open (f"{filename}/image.jpeg", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                image = Image.open(rf'{filename}/image.jpeg')
                im = image.convert('RGB')
                if page_number > 0:
                    page_list.append(im)
                else:
                    im_1 = im
            del r
            time.sleep(random.uniform(1,4))
        index = index+1
    page_number = page_number+1
    print(f'Downloading page {page_number}...')

#Save the pdf and delete the mirror image used to generate the pdf
im_1.save(rf'{filename}/Book.pdf', save_all=True, append_images=page_list)
os.remove(f"{filename}/image.jpeg")
print("Your book is ready!")
    