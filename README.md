# tgtogd
一个依靠`telegram bot`的下载机器人，功能包括`Upload telegram files to google drive, `Use yt-dlp to download video and upload to google drive`  
修改于https://github.com/viperadnan-git/google-drive-telegram-bot;  
修改点:
- [X] 更新`Pyrogram`版本以适配大文件下载
- [X] 将`ytdl`更新为`yt-dlp`
- [X] 修改为`sqlite`模式而非`postgresql` ~~本来最开始想改成本地json,但懒得改sql请求就算了~~
- [X] 修改为`async`异步，~~理论提升性能~~
- [X] 下载文件名修改为`时间+文件名`,以解决同名文件下载的问题。
## 参数
- `BOT_TOKEN` - Get it by contacting to [BotFather](https://t.me/botfather)
- `APP_ID` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `API_HASH` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `SUDO_USERS` - List of Telegram User ID of sudo users, seperated by space.
- `SUPPORT_CHAT_LINK` - Telegram invite link of support chat.
- `DATABASE_URL` - Path of sqlite file.
- `DOWNLOAD_DIRECTORY` - Custom path for downloads. Must end with a forward `/` slash. (Default to `./downloads/`)
- `MAX_TASKS` - The max tasks you want to download from the `telegram`, default number is 4.
## Bot命令支持：
`/auth` : 进行`Googled Drive`的验证,需要在填入`ClientID`和`ClientSecret`之后运行，访问`auth url`之后将`code`直接发送给`Bot`即可完成验证;  
`/revoke`: 取消`Google Drive`认证  
`/setfolder`: 设置`Google Drive`上传文件夹目录,直接发送例如:`/setfolder https://drive.google.com/drive/folders/*`即可;  
`/ytdl`: 使用`yt-dlp`进行视频等下载,发送如:`/ytdl https://www.youtube.com/****`即可;
## 其他功能:
### 上传Telegram Files到Google Drive
直接转发文件给`Bot`即可, 同时下载参数为`MAX_TASKS`, 不建议大于`4`, 可能会触发`Flood_wait`.
### 下载普通链接到Google Drive
直接发送链接即可.
## 安装(照抄原版)
- Install required modules.
```sh
apt install -y git python3 ffmpeg libpq-dev
```
- Clone this git repository.
```sh 
git clone https://github.com/Xiefengshang/tgtogd
```
- Change Directory
```sh 
cd tgtogd
```
- Install requirements with pip3
```sh 
pip3 install -r requirements.txt
