# tgtogd
一个依靠`telegram bot`的下载机器人，功能包括`上传telegram的文件到google drive`, `下载文件到google drive(链接以及使用yt-dlp下载视频)`  
修改自https://github.com/viperadnan-git/google-drive-telegram-bot;  
修改点:
- [X] 更新`Pyrogram`版本以适配大文件下载
- [X] 将`ytdl`更新为`yt-dlp`
- [X] 修改为`sqlite`模式而非`postgresql` ~~本来最开始想改成本地json,但懒得改sql请求就算了~~
- [X] 修改为`async`异步，~~理论提升性能~~
- [X] `Telegram`下载文件名修改为`时间+文件名`,以解决同名文件下载的问题。
- [X] 更新认证方式，从`urn:ietf:wg:oauth:2.0:oob`更新为`localhost` 模式
## 参数
- `BOT_TOKEN` - 与 [BotFather](https://t.me/botfather) 聊天获得(
- `APP_ID` - 请在 [my.telegram.org](https://my.telegram.org/apps) 上创建APP获得
- `API_HASH` - 同上
- `SUDO_USERS` - 具有`SUDO USER`权限的`Telegram ID`, 若有多个则用空格分开.
- `SUPPORT_CHAT_LINK` - `Telegram invite link`.
- `DATABASE_URL` - SQLite的文件位置(相对绝对路径皆可,以`sqlite:`开头).
- `DOWNLOAD_DIRECTORY` - 下载文件的位置,相对绝对路径皆可. 必须以`/`结尾. (默认为 `./downloads/`)
- `MAX_TASKS` - 最大同时下载`Telegram`文件的数量,默认为4,不建议大于4
## Bot命令支持：
`/auth` : 进行`Googled Drive`的验证,需要在填入`ClientID`和`ClientSecret`之后运行，访问`auth url`之后将`http://localhost/?code=`的认证`url`直接发送给`Bot`即可完成验证;  
`/revoke`: 取消`Google Drive`认证  
`/setfolder`: 设置`Google Drive`上传文件夹目录,直接发送例如:`/setfolder https://drive.google.com/drive/folders/*`即可;  
`/ytdl`: 使用`yt-dlp`进行视频等下载,发送如:`/ytdl https://www.youtube.com/****`即可;  
`/emptytrash`：清空`google drive`垃圾箱
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
