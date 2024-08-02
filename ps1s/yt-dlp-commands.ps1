# Single Video
yt-dlp.exe --rm-cache-dir --extract-audio --audio-format mp3 --embed-thumbnail --embed-metadata -o "/<directory>/%(title)s.%(ext)s" <video url>

# Single Video with Chapters (seperate file per chapter)
#   This is unfortunately the best that can be done, cannot change the metadata of each file to match the song
yt-dlp.exe --rm-cache-dir --extract-audio --audio-format mp3 --embed-thumbnail --embed-metadata --split-chapters -o "chapter:/<directory>/%(title)s/%(section_title)s.%(ext)s" <video url>

# Playlist
yt-dlp.exe --rm-cache-dir -ciw --embed-thumbnail --embed-metadata --extract-audio --audio-format mp3 -o "/%(playlist_index)s - %(title)s.%(ext)s" <playlist url>
