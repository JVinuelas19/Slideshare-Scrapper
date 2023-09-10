from bs4 import BeautifulSoup as bs
from PIL import Image
import requests
import shutil
import time
import random
import os

#This script downloads all the images from the book selected from slideshare.net
#It uses a randomizer between petitions to avoid being banned from the website
#Afterwards the script creates a PDF with the images downloaded
#Use with your own discretion and please don't profit with it. 
#pdf = FPDF()
dirname=os.path.dirname(__file__)
filename=os.path.join(dirname, 'Book')

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)' 
           'AppleWebKit/537.36 (KHTML, like Gecko)'
           'Chrome/79.0.3945.88 Safari/537.36'}

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
            r = requests.get(image, stream = True)
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
im_1.save(rf'{filename}/Book.pdf', save_all=True, append_images=page_list)
os.remove(f"{filename}/image.jpeg")
print("Your book is ready!")
#pdf.output("Bookname.pdf", "F")
    