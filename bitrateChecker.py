import os
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3



def process_song_files(folder_path):
    for filename in os.listdir(folder_path):
        # print(filename)
        # file_path = os.path.join(folder_path, filename)
        # new_file_path = os.path.join(folder_path, "eeeeeeeee.mp3")
        # os.rename(file_path,  new_file_path)
        # return

        file_path = folder_path + filename #os.path.join(folder_path, filename)

        # Check if the file is an audio file
        if file_path.endswith('.mp3'):
            audio = MP3(file_path)
            
            # Get the bitrate
            bit_rate = audio.info.bitrate / 1000 if audio.info.bitrate else None

            if bit_rate:
                if bit_rate >= 320:
                  continue
                # Get other metadata if available
                if 'title' in audio:
                  song_title = audio['title'][0]
                  print(f"{bit_rate} kbps : {song_title}")
                else:
                    
                  print(f"{bit_rate} kbps : {filename}")
            else:
                print(f"No bitrate information available for {file_path}")



# Provide the path to the folder containing the audio files
folder_path = '/Users/nicholassantini/Documents/need to redownload/'

# Call the function to process the song files in the folder
process_song_files(folder_path)
