# Use this to merge diffs when dowloading youtube playlists with yt-dlp
$files = (ls).Count
$counter = 0

$list =  New-Object string[] $files

$children = Get-ChildItem *.mp3


for($i = 0; $i -lt $files; $i++) {
	$current = $children[$i]
	$index,$NewName = $split = $current.Name -split " - ",2

	try {
		#Try to rename
		Rename-Item -Path $current.FullName -NewName $NewName -ErrorAction Stop
		
		# If rename successful, add to list & increment counter
		$list[$counter] = $NewName
		$counter++
	} catch {
		# The file already exists, meaning the song most likely already is here
		# so delete duplicate
		echo "REMOVING"
		Remove-Item -Path $current.FullName
	}
}

$taken = $list[0..$count]

$pth = (Get-Item .).FullName + "/000 playlist.m3u8"
New-Item -Path $pth -ItemType File

Add-Content -Path $pth -Value "#EXTM3U"

for($i = 0; $i -lt $count; $i++) {
	$current = $taken[$i]
	
	Add-Content -Path $pth -Value ("#EXTINF:" + $i.ToString())
	Add-Content -Path $pth -Value $current -Encoding UTF8
}
