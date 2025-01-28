# YtToMP3
.exe file with source code that downloads youtube videos as mp3 with provided youtube link to a specified folder

NOTE: the .exe file can probably run without anything installed, but to ensure that errors dont happen in the app, do the following steps

1. Install python
2. run terminal commands : pip install pytube moviepy 
			   pip install --upgrade pip
3. Place FFmpeg folder in C: && run terminal command : setx /m PATH "C:\ffmpeg\bin;%PATH%"
4. check if ffmeg works correctly :
		Open a new CMD 
		run command: ffmpeg -version
5. create  shortcut of the folder YoutubeToMP3.exe
6. Enjoy :)


