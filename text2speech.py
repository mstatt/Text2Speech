import os
import re
import shutil


proc_dir = os.getcwd()+'//articles//'
out_dir = os.getcwd()+'//mp3-out//'
post_proc = os.getcwd()+'//already-processed//'

#Assign file names in the directory to a list for processing
article_list = os.listdir(proc_dir)
#Sort the list
article_list.sort()

##--------------------------------------------------------------------
def getContents(filename):
	with open(os.path.join(proc_dir, filename)) as f:
		content_list = f.readlines()
	f.close()
	contents = " ".join(content_list)
	return contents

##--------------------------------------------------------------------
def synthesize_text(text, title):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    # The response's audio_content is binary.
    with open(os.path.join(out_dir, title+".mp3"), "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file '+title+'.mp3"')

##--------------------------------------------------------------------
#Post processing clean up
def clear_out(filename):
	shutil.move(os.path.join(proc_dir, filename),os.path.join(post_proc, filename))


for file in article_list:
	text ="" #clear out text var
	basename = os.path.splitext(file)[0] #extract only file name
	print('Synthesizing file: '+file) # Alert current status
	text = getContents(file) #Extract contents of file
	synthesize_text(text,basename) #process contents into mp3
	clear_out(file) #Move processed file



