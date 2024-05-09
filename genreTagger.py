import os
import music_tag
from dotenv import load_dotenv

def isSupportedFile(filename):
    fn = filename.lower()
    return fn.endswith('.aac') or \
      fn.endswith('.aiff') or \
      fn.endswith('.dsf') or \
      fn.endswith('.flac') or \
      fn.endswith('.m4a') or \
      fn.endswith('.mp3') or \
      fn.endswith('.ogg') or \
      fn.endswith('.opus') or \
      fn.endswith('.wav') or \
      fn.endswith('.wv')

# returns a tuple
# (True, "") if the genre does not need to be modifies
# (True, "genre") if the genre was set
# (False, "Reason") if the genre was not set
def setGenre(folder_path, filename):
    #genre = containing folder name
    genre = os.path.basename(os.path.normpath(folder_path))

    # if the file is a .DS_Store file, return
    if filename == ".DS_Store":
        return (True, "")

    # if the file is not supported, return
    if isSupportedFile(filename):
        audio = music_tag.load_file(folder_path + filename)
    else:
        return (False, "Unsupported file type")
    
    # if the genre is not part of the metadata, add it
    if not audio['genre']:
        audio.append_tag('genre', genre)
    #if the genre is already set, return
    elif str(audio['genre']) == genre: 
        return (True, "")
    #else, set it
    else: 
      audio['genre'] = genre
    audio.save()

    #reload the file to verify the genre was set
    audio = music_tag.load_file(folder_path + filename)
    if str(audio['genre']) != genre:
        return (False, "Failed to set genre")
    
    return (True, genre)


def process_song_files(folder_path):
    unprocessed = []
    procressed = []
    # For every file in target folder
    for filename in os.listdir(folder_path):

        file_path = folder_path + filename 

        # If the file is a folder, process the files in the folder
        if os.path.isdir(file_path):
            recursiveResult = process_song_files(file_path + "/")
            unprocessed += recursiveResult[0]
            procressed += recursiveResult[1]
            continue

        # Attempt to process the file
        result = setGenre(folder_path, filename)

        # If the file failed to be processed, add it to the unprocessed list
        if not result[0]:
          unprocessed.append((filename, result[1]))
        # If the file was processed, add it to the processed list
        elif result[1] != "":
          procressed.append((filename, result[1]))

    return (unprocessed, procressed)


def printResults(unprocessed, procressed):
  if len(unprocessed) > 0:
    print("-----------------------------")
    print("Unprocessed files:")
    print("-----------------------------")
    for song in unprocessed:
        print(song[0], " Reason: ", song[1])
  else:
    print("No files failed to be altered")
     
  print()
  if len(procressed) > 0:
    print("-----------------------------")
    print("Procressed files:")
    print("-----------------------------")
    for song in procressed:
        print("Genre: ", song[1], ": ", song[0])
  else:
    print("No files needed to be altered")


def main():

  load_dotenv()

  # Provide the path to the folder containing the audio files
  folder_path = os.getenv("MUSIC_DIR")

  print("Processing...")

  # Call the function to process the song files in the folder
  results = process_song_files(folder_path)
  print("All done")
  printResults(results[0], results[1])

main()