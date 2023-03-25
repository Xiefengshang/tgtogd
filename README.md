# tgtogd
一个依靠`telegram bot`的下载机器人，功能包括`Upload telegram files to google drive, `Use yt-dlp to download video and upload to google drive`  
修改于https://github.com/viperadnan-git/google-drive-telegram-bot;  
修改点:
- [X] 更新`Pyrogram`版本以适配大文件下载
- [X] 将`ytdl`更新为`yt-dlp`
- [X] 修改为`sqlite`模式而非`postgresql` ~~本来最开始想改成本地json,但懒得改sql请求就算了~~
- [X] 修改为`async`异步，~~理论提升性能~~
