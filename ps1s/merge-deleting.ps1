# Use this to merge diffs when dowloading playlists with yt-dlp
# YT DLP command
# yt-dlp.exe --rm-cache-dir -ciw --embed-thumbnail --embed-metadata --extract-audio --audio-format mp3 -o "/%(playlist_index)s - %(title)s.%(ext)s" $playlistURL

$children = Get-ChildItem *.mp3
echo ("Items: " + $children.Count)
for($i = 0; $i -lt $children.Count; $i++) {
	$current = $children[$i]
	$Index,$NewName = $split = $current.Name -split " - ",2
	$matches = Get-ChildItem *.mp3 | Where-Object { $_.Name -like "*$NewName*" }
	
	if ($matches.Count -gt 1) {
		echo "Found duplicate, deleting"
		Remove-Item -Path $current.FullName
	}
}