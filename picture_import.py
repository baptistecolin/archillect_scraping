from urllib.request import *
from urllib.error import URLError
from bs4 import BeautifulSoup as bs
from math import floor
import socket

socket.setdefaulttimeout(30) #the request is considered to have timed out after 30 seconds

start = 20000
end   = 20100

n = 1 #this will be incremented each time we download a pic

gif_dl = True  #do we want to download .gif files ?
pic_dl = False #do we want to download .png and .jpg files ?

#initiating the error_log.txt file
log = open('error_log.txt', 'w')
log.write('The following caused errors :\n\n')

#we are going to do the same thing for each picture
for i in range(start, end+1) :
	
	j = 1
	k = 1
	progression = floor(100*((i-start)/(end-start))) # just so the user knows how long he has to wait
	
	url_i = 'http://archillect.com/' + str(i) #archillect.com URLs are really handy


	#opening the url and retrieving the HTML code
	while(True):
		try:
			content = urlopen(url_i)
			url_open_successful = True
			break
		except (socket.timeout, URLError, ConnectionResetError) :
			if (k<3): 
				#if the request times out, we try it again up to 3 times
				k = k+1
				print('timeout error. ' + url_i + ' opening attempt n°' + str(k) )

			else: 
				#if it times out a third time, we just give up
				url_open_successful = False
				break



	if(not(url_open_successful)):
		#the fact that the URL opening has failed is being notified, both in the terminal and in the error log
		log.write(url_i + ' failed to open.\n')
		print('timeout error. ' + url_i + ' opening aborted.')
	else:
		
		#formatting the content into a strutured string using Beautiful Soup
		html = content.read()
		soup = bs(html, "lxml")

		tag = soup.find(attrs={"name":"twitter:image"}) #outputs a Tag, which can be treated as a dictionary using tag.attrs
		img_url = tag.attrs['content'] #the url of the picture is now stored as a string in 'img_url'

		extension = img_url[-4:] #the 4 last character will be either '.jpg', '.png' or '.gif'
		
		#deciding wether to download the picture or not
		if ((extension == '.gif') and (gif_dl == False)):
			skip = True
		elif (((extension == '.jpg') or (extension == '.png')) and (pic_dl == False)):
			skip = True
		else:
			skip = False


		if (not(skip)):
			# from here is the part where we actually download the pic,
			# which only happens when skip == False
			
			#creating the file name
			if(n<10):
				filename = 'img00000' + str(n)
			elif (i<100):
				filename = 'img0000'  + str(n)
			elif (i<1000):
				filename = 'img000'   + str(n)
			elif (i<10000):
				filename = 'img00'    + str(n)
			else:
				filename = 'img0'     + str(n)


			#attempting to download the picture	
			while(True):
				try:
					urlretrieve(img_url, './gifs/' + filename + extension) # if this line throws an error, the 3 lines below won't be
										   # executed and we'll move on to the 'except' section

					pic_download_successful = True 		   # we've reached this line : it means the image has been downloaded ! 
					n = n + 1 				   # we can increment the counter
					break 					   # since the download was succesful, we can get out of the while loop

				except (socket.timeout, URLError, ConnectionResetError) :
					if (j<3):
						#if the request times out, we try it again up to 3 times
						j = j+1
						print('timeout error. ' + 'pic #' + str(i) + ' (' + extension + ') download attempt n°' + str(j) )
					else:
						pic_download_successful = False    # we've tryed 3 times and failed 3 times ...
						break 				   # we're giving up and getting out of the loop :(


			if (pic_download_successful):
				print('pic #' + str(i) + ' downloaded as ' + filename + extension + ' - ' + str(progression) + '%')
			else:
				log.write('pic #' + str(i) + ' (' + extension + ') failed to download.\n')
				print('timeout error. ' + 'pic #' + str(i) + ' (' + extension + ') download aborted.')
	
		else:
			print('pic #' + str(i) + ' (' + extension + ') skipped. - ' + str(progression) + '%')



log.write('\n' + str(n-1) + ' files downloaded')
print('Done')
