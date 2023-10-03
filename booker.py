from bs4 import BeautifulSoup as bs
from PIL import Image
import requests
import shutil
import time
import random
import os

#This script downloads all the images from the book selected from slideshare.net and creates a PDF with the images downloaded. 
#It also features a download timer, pathing info about the book and some basic error scenarios management (URL is not valid).
#It uses basic ways to scrap safely such as a time randomizer between requests and random headers to avoid being banned from the website.
#Use with your own discretion and please don't profit with it. 

#We will set the directory and filename to use it with no absolute paths
dirname=os.path.dirname(__file__)
filename=os.path.join(dirname)

#To avoid straight bans we will change the Python header between these 3. Doing so will result in stealthing the python script header. You can add more if you wish to
header1 = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64)' 
           'AppleWebKit/537.36 (KHTML, like Gecko)'
           'Chrome/79.0.3945.88 Safari/537.36'
          }
header2 = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)'
           'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148' 
           'Safari/604.1'
          }
header3 = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X)'
           'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148'
           'Safari/604.1'
          }
header_list = [header1, header2, header3]

def download_book(url, save_path):
    page = requests.get(url)
    if (requests.get(url).status_code !=200):
        print("URL is not valid. Check if the URL is correct and try again.")
    else:
        #Starts the timer, gets all picture labels (which contains each page) and sets the first image of the PDF 
        #(PIL library requires the first image and then appends other images from page_list)
        time_start = time.time()
        soup = bs(page.content, 'html.parser')
        pages = soup.find_all('picture')
        page_number=0
        im_1= Image.new("RGB", (1920, 1080))
        page_list = []
        for page in pages:
            #For each page we split its html content in substrings to search for the 2048w substring
            page_string = str(page)
            page_strings = page_string.split()
            index = 0
            for strings in page_strings:
                #2048w is the highest resolution image. The index searches for the substring 2048w and extracts the previous value which contains the URL with the image
                if strings == '2048w"':
                    value = index-1 
                    image = page_strings[value]
                    #Now requests the image URL, overwrites it in a temporary mirror image and queues it to page_list
                    r = requests.get(url = image, stream = True, headers = header_list[random.randint(0,len(header_list)-1)])
                    if(r.status_code == 200):
                        r.raw.decode_content = True
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

        #Stops the timer, extracts the title from URL, shapes it and save the pdf. Then deletes the mirror image used to generate the pdf and display some info
        time_elapsed = round(time.time() - time_start, 2)
        os.remove(f"{filename}/image.jpeg")
        ugly_bookname = url.split('/')
        nice_bookname = ugly_bookname[-1].replace("-", " ").capitalize()
        if save_path == "":
            im_1.save(rf'{filename}/{nice_bookname}.pdf', save_all=True, append_images=page_list)
            print(f"\nYour book '{nice_bookname}' is ready!\n"
            f"You can find it in the next location: {filename}\{nice_bookname}.pdf\n"
            f"Time elapsed to download the book: {time_elapsed} seconds\n")
        else:
            im_1.save(rf'{save_path}/{nice_bookname}.pdf', save_all=True, append_images=page_list)
            print(f"\nYour book '{nice_bookname}' is ready!\n"
            f"You can find it in the next location: {save_path}\{nice_bookname}.pdf\n"
            f"Time elapsed to download the book: {time_elapsed} seconds\n")

option = 0
while (option!=3):
    option = int(input('Choose an option:\n1 - Download a book/slideshare\n2 - Download books from a txt file\n3 - Exit\n'))

    if option == 1:
        #Ask for the URL and converts the book contained to a PDF file if the URL returns a 200 code. Otherwise the script won't do anything.
        url=input('Paste the URL book or slides from slideshare.net : ')
        save_path = input ('Enter the path you where you want to store the books/slides (Press Enter for a default location): ')
        download_book(url, save_path)
        
    elif option == 2:
        path = input('Enter the path of your txt file: ')
        save_path = input ('Enter the path you where you want to store the books/slides (Press Enter for a default location): ')
        #Leer URLS de un txt
        with open(path, 'r') as urls:
            url_list = urls.read().splitlines()
            for url in url_list:
                download_book(url, save_path)

    elif option == 3:
        print('Thank you for using my code!\n'
              'If you enjoy my work please consider donating me at: https://www.paypal.com/donate/?hosted_button_id=7QSS3APP4TSGE \n'
              'Meet my other works and feedback me at: https://github.com/JVinuelas19\n'
              'Goodbye!')

    else:
        print("Option not available. Please try again.")

    