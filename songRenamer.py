import os
from tinytag import TinyTag
from dotenv import load_dotenv

def getNewFilename(artist, title):
    return (title+ " - " + artist).replace('/', ' ')

def renameFile(folder_path, filename, new_filename):
    file_path = folder_path + filename
    file_extension = os.path.splitext(filename)[1]
    new_filename += file_extension
    new_file_path = os.path.join(folder_path, new_filename) #folder_path + new_filename
    os.rename(file_path, new_file_path)
    # print(f"Renamed file: {filename} -> {new_filename}")

def processWithTinyTag(folder_path, filename):
    tag = TinyTag.get(folder_path + filename)
    song_title = tag.title
    artist = tag.artist
    if artist is None:
        artist = tag.albumartist
    if artist is None or song_title is None:
        return "No metadata for artist or song name"
    if artist.replace(' ', '') == "" or song_title.replace(' ', '') == "":
        return "Artist or song title blank. Atrist: " + artist + " Song Title: " + song_title
    
    newFileName = getNewFilename(artist, song_title)
    renameFile(folder_path, filename, newFileName)
    return ""



def process_song_files(folder_path):
    unprocessed = []
    for filename in os.listdir(folder_path):

        file_path = folder_path + filename #os.path.join(folder_path, filename)

        if os.path.isdir(file_path):
            # print("-----------------------------")
            # print(f"Processing folder: {filename}")
            unprocessed += process_song_files(file_path + "/")
            # print("-----------------------------")
            continue

        failureReason = ""
        if TinyTag.is_supported(folder_path + filename):
          try:
            failureReason = processWithTinyTag(folder_path, filename)
          except Exception as e:
            failureReason = f"Error processing file {filename}: {str(e)}"
             

        if failureReason != "":
          unprocessed.append((filename, failureReason))

    return unprocessed


load_dotenv()

# Provide the path to the folder containing the audio files
folder_path = os.getenv("STAGING_AREA")

print("Processing...")

# Call the function to process the song files in the folder
unprocessed = process_song_files(folder_path)
print("All done")
if len(unprocessed) > 0:
  print("-----------------------------")
  print("Unprocessed files:")
  print("-----------------------------")
  for song in unprocessed:
      print(song[0], " Reason: ", song[1])




# def processMP3(folder_path, filename):
#     audio = File(folder_path + filename, easy=True)
#     if isinstance(audio, list):
#         audio = audio[0]
#     if audio is None or not audio.mime[0].startswith('audio/'):
#        return
#     # Print the available metadata tags for debugging
#     # print(f"Metadata tags for file: {filename}")
#     # for tag, value in audio.items():
#     #     print(f"- {tag}: {value[0]}")

#     # Extract the song title and artist from the metadata
#     if 'title' in audio and 'artist' in audio:
#       song_title = audio['title'][0]
#       artist = audio['artist'][0]
#       #remove everything after the slash
#       # print(artist.split('/')[0])
#       artist = artist.split('/')[0]

#       # Create the new filename by combining the song title and artist
#       new_filename = getNewFilename(artist, song_title)
#       renameFile(folder_path, filename, new_filename)