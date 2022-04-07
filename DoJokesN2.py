#MAKE SAME FPS

#RANDOM FONTS
#RANDOM BACKGROUNDS
#BACKGROUND MUSIC
#LAUGH TRACK

import string
import boto3
import random
import os
import math
from mutagen.mp3 import MP3
from string import ascii_letters
import textwrap
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
import moviepy.editor as mpe
from moviepy.editor import *


i = 1
while i < 333:
	print("JOKE NUMBER:",i)
	i += 1

	#################################################################################################################################################
	
	videobackground=random.choice(os.listdir("E:\\Projects\\JOKES\\video\\cropped"))
	videobackground="E:\\Projects\\JOKES\\video\\cropped\\"+videobackground
	print(videobackground)
	
	bdt=random.choice(os.listdir("E:\\Projects\\JOKES\\sounds"))
	bdt="E:\\Projects\\JOKES\\sounds\\"+bdt
	print(bdt)
	
	textfont=random.choice(os.listdir("E:\\Projects\\JOKES\\fonts"))
	textfont="E:\\Projects\\JOKES\\fonts\\"+textfont
	print(textfont)
	
	
	aList = ["Emma","Ivy","Kevin","Emma","Justin"]
	jv = random.sample(aList, 1)
	jokevoice=jv[0]
	print(jokevoice)
	
	jokefile="E:\\Projects\\JOKES\\listofjokes.txt"
	
	whitebackground="E:\\Projects\\JOKES\\images\\white-bck.jpg"
	#################################################################################################################################################
	
	#SPLIT JOKE LINES

	f = open(jokefile)
	linesone = f.readline()
	f.close()

	print("linesone",linesone)
	
	
	# list to store file lines
	lines = []
	# read file
	with open(jokefile, 'r') as fp:
		lines = fp.readlines()

	# Write file
	with open(jokefile, 'w') as fp:
		for number, line in enumerate(lines):
			if number not in [0]:
				fp.write(line)

	# print("LINES:",lines)		


	# with open(jokefile) as f:
	# 	lines = f.read().splitlines()
	
	
	# with open(jokefile, 'w') as fout:
	# 	fout.writelines(lines[1:])

	# swaplines=lines.copy()
	# swaplines[1:len(swaplines)]=lines[0:-1]
	# swaplines[0]=lines[-1] #DONE
	

	joke=linesone.split("#")
	JokeA=joke[0]
	JokeB=joke[1]
	print(JokeA)
	print(JokeB)
	
	#################################################################################################################################################
	
	#TEXT TO SPEACH
	########### JOKEA
	
	##TEXT TO SPEACH
	polly_client = boto3.Session(
					aws_access_key_id="AKIAW5EOSKLYSJK4YQHX",                     
		aws_secret_access_key="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",
		region_name='us-west-2').client('polly')
	
	response = polly_client.synthesize_speech(VoiceId=jokevoice,
					OutputFormat='mp3', 
					Text = JokeA,
					Engine = 'neural')
	
	file = open('E:\\Projects\\JOKES\\JOKEA.mp3', 'wb')
	file.write(response['AudioStream'].read())
	file.close()
	
	
	############ JOKEB
	
	###TEXT TO SPEACH
	polly_client = boto3.Session(
					aws_access_key_id="AKIAW5EOSKLYSJK4YQHX",                     
		aws_secret_access_key="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",
		region_name='us-west-2').client('polly')
	
	response = polly_client.synthesize_speech(VoiceId=jokevoice,
					OutputFormat='mp3', 
					Text = JokeB,
					Engine = 'neural')
	
	file = open('E:\\Projects\\JOKES\\JOKEB.mp3', 'wb')
	file.write(response['AudioStream'].read())
	file.close()
	
	
	#################################################################################################################################################
	audioA = MP3('E:\\Projects\\JOKES\\JOKEA.mp3')
	wathermp3audiolenth=audioA.info.length
	jokeAlenth=int(math.ceil(wathermp3audiolenth))
	print(jokeAlenth)
	
	audioB = MP3('E:\\Projects\\JOKES\\JOKEB.mp3')
	wathermp3audiolenth=audioB.info.length
	jokeBlenth=int(math.ceil(wathermp3audiolenth))
	print(jokeBlenth)
	
	totalaudiolenth=jokeAlenth+jokeBlenth+1
	print("TotalAudioLenth:",totalaudiolenth)
	
	#################################################################################################################################################
	
	##################IMAGE JOKEA
	img = Image.open(fp=whitebackground, mode='r')
	font = ImageFont.truetype(font=textfont, size=70)
	draw = ImageDraw.Draw(im=img)
	text = JokeA
	avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
	max_char_count = int(img.size[0] * .618 / avg_char_width)
	text = textwrap.fill(text=text, width=max_char_count,break_long_words=False)
	draw.text(xy=(img.size[0]/2, img.size[1] / 2), text=text, font=font, fill='#000000', anchor='mm', stroke_width=5, stroke_fill="#CACACA")
	JOKEAtxt="E:\\Projects\\JOKES\\images\\JOKEA.png"
	img.save(JOKEAtxt)
	
	
	##################IMAGE JOKEB
	img = Image.open(fp=whitebackground, mode='r')
	font = ImageFont.truetype(font=textfont, size=70)
	draw = ImageDraw.Draw(im=img)
	text = JokeB
	avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
	max_char_count = int(img.size[0] * .618 / avg_char_width)
	text = textwrap.fill(text=text, width=max_char_count,break_long_words=False)
	draw.text(xy=(img.size[0]/2, img.size[1] / 2), text=text, font=font, fill='#000000', anchor='mm', stroke_width=5, stroke_fill="#CACACA")
	JOKEBtxt="E:\\Projects\\JOKES\\images\\JOKEB.png"
	img.save(JOKEBtxt)
	
	
	#TEXT TO SPEACH
	#################################################################################################################################################
	
	video = (mpe.VideoFileClip(videobackground)
				.set_duration(jokeAlenth+jokeBlenth+6)
			)
	
	joketextA = (mpe.ImageClip(JOKEAtxt)
			.set_duration(jokeAlenth+1)
			)    
	
	joketextB = (mpe.ImageClip(JOKEBtxt)
			.set_duration(jokeBlenth+4)
			.set_start(jokeAlenth+1)
			)    
	
	maskA = mpe.vfx.mask_color(joketextA,color=[255,255,255])
	maskB = mpe.vfx.mask_color(joketextB,color=[255,255,255])
	
	audioclipA = AudioFileClip('E:\\Projects\\JOKES\\JOKEA.mp3')
	audioclipB = AudioFileClip('E:\\Projects\\JOKES\\JOKEB.mp3')
	audiobadumtss = AudioFileClip(bdt)
	new_audioclip = CompositeAudioClip([audioclipA,audioclipB.set_start(jokeAlenth+1),audiobadumtss.set_start(jokeAlenth+jokeBlenth+1)])
	video.audio = new_audioclip
	
	a_string = JokeA
	finfilename = a_string.translate(str.maketrans('', '', string.punctuation))
	finfilename.replace(" ", "")
	
	print(finfilename)
	
	finfilename="E:\\Projects\\JOKES\\finjokes\\"+finfilename+".mp4"
	
	final = mpe.CompositeVideoClip([video, maskA, maskB])
	final.write_videofile(finfilename)
	
	
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	
	#################################################################################################################################################
	
	# #MAKING JOKE A
	# #################################
	# video = (mpe.VideoFileClip(videobackground)
	#             .set_duration(jokeAlenth+1)
	#         )
	
	# logo = (mpe.ImageClip(JOKEAtxt)
	#           .set_duration(jokeAlenth+1)
	#         )
	
	# mask = mpe.vfx.mask_color(logo,color=[255,255,255])
	
	# audioclip = AudioFileClip('E:\\Projects\\JOKES\\JOKEA.mp3')
	# new_audioclip = CompositeAudioClip([audioclip])
	# video.audio = new_audioclip
	
	# final = mpe.CompositeVideoClip([video, mask])
	# final.write_videofile("E:\\Projects\\JOKES\\JOKEA.mp4")
	
	
	# #MAKING JOKE A
	# #################################
	# video = (mpe.VideoFileClip(videobackground)
	#             .set_duration(jokeBlenth+1)
	#         )
	
	# logo = (mpe.ImageClip(JOKEBtxt)
	#           .set_duration(jokeBlenth+1)
	#         )
	
	# mask = mpe.vfx.mask_color(logo,color=[255,255,255])
	
	# audioclip = AudioFileClip('E:\\Projects\\JOKES\\JOKEB.mp3')
	# new_audioclip = CompositeAudioClip([audioclip])
	# video.audio = new_audioclip
	
	# final = mpe.CompositeVideoClip([video, mask])
	# final.write_videofile("E:\\Projects\\JOKES\\JOKEB.mp4")
	
	# #################################################################################################################################################
	
	# ###COMBINE
	
	# video_1 = VideoFileClip("E:\\Projects\\JOKES\\JOKEA.mp4")
	# video_2 = VideoFileClip("E:\\Projects\\JOKES\\JOKEB.mp4")
	
	# # final_video= CompositeVideoClip([video_1, video_2])
	
	# final_video = CompositeVideoClip([video_1, # starts at t=0
	#                             video_2.set_start(jokeAlenth+1)]) # start at t=9s
								
	
	# final_video.write_videofile("E:\\Projects\\JOKES\\FinalJoke.mp4")
	
	#################################################################################################################################################