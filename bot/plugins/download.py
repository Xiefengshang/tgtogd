import os
import asyncio
import aiohttp
import time
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.downloader import download_file, utube_dl
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.gdrive_utils import GoogleDrive
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
import traceback

# 下载文件并上传到Google Drive
@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
async def _download(client, message):
    user_id = message.from_user.id
    if not message.media:
        sent_message = await message.reply_text('🕵️**Checking link...**', quote=True)
        if message.command:
            link = message.command[1]
        else:
            link = message.text
        if 'drive.google.com' in link:
            await sent_message.edit(Messages.CLONING.format(link))
            LOGGER.info(f'Copy:{user_id}: {link}')
            msg = await GoogleDrive(user_id).clone(link)
            await sent_message.edit(msg)
        else:
            if '|' in link:
                link, filename = link.split('|')
                link = link.strip()
                filename.strip()
                dl_path = os.path.join(f'{DOWNLOAD_DIRECTORY}/{filename}')
            else:
                link = link.strip()
                filename = os.path.basename(link)
                dl_path = DOWNLOAD_DIRECTORY
            LOGGER.info(f'Download:{user_id}: {link}')
            await sent_message.edit(Messages.DOWNLOADING.format(link))
            result, file_path = await download_file(link, dl_path)
            if result:
                await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = await GoogleDrive(user_id).upload_file(file_path)
                await sent_message.edit(msg)
                LOGGER.info(f'Deleting: {file_path}')
                os.remove(file_path)
            else:
                await sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))

# 从Telegram下载文件并上传到Google Drive
@Client.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video | filters.photo) & CustomFilters.auth_users)
async def _telegram_file(client, message):
    user_id = message.from_user.id
    sent_message = await message.reply_text('🕵️**Checking File...**', quote=True)
    if message.document:
        file = message.document
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio
    elif message.photo:
        file = message.photo
        file.mime_type = "images/png"
        file.file_name = f"IMG-{user_id}-{message.id}.png"
    await sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.file_name, humanbytes(file.file_size), file.mime_type))
    LOGGER.info(f'Download:{user_id}: {file.file_id}, name: {file.file_name}')
    try:
        file_path = await message.download(file_name=DOWNLOAD_DIRECTORY+str(file.date)+(file.file_name or ""))
        await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = await GoogleDrive(user_id).upload_file(file_path, file.mime_type)
        await sent_message.edit(msg)
        os.remove(file_path)
    except Exception as e:
        # 构造错误信息
        error_msg = f"**❌ 发生意外错误**\n\n错误类型：`{type(e).__name__}`\n错误详情：`{str(e)}`\n\n完整追踪：\n`{traceback.format_exc()}`"
        # 截断过长的错误信息（Telegram消息长度限制）
        if len(error_msg) > 4000:
            error_msg = error_msg[:4000] + "..."
        await sent_message.edit(f"{Messages.WENT_WRONG}\n\n{error_msg}")
        # 记录完整错误日志
        LOGGER.error(f"User {user_id} 遇到错误：\n{traceback.format_exc()}")
        # 清理残留文件
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                LOGGER.info(f'已清理残留文件: {file_path}')
            except Exception as cleanup_e:
                LOGGER.error(f"清理文件失败: {str(cleanup_e)}")
    
# 从YouTube下载并上传到Google Drive
@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.YtDl) & CustomFilters.auth_users)
async def _ytdl(client, message):
    user_id = message.from_user.id
    if len(message.command) > 1:
        sent_message = await message.reply_text('🕵️**Checking Link...**', quote=True)
        link = message.command[1]
        LOGGER.info(f'YTDL:{user_id}: {link}')
        await sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = await utube_dl(link,DOWNLOAD_DIRECTORY)
        if result:
            await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
            msg = await GoogleDrive(user_id).upload_file(file_path)
            await sent_message.edit(msg)
            LOGGER.info(f'Deleting: {file_path}')
            os.remove(file_path)
        else:
            await sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
    else:
        await message.reply_text(Messages.PROVIDE_YTDL_LINK, quote=True)

async def main():
    async with Client(
        "my_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=100
    ) as client:
        await client.start()
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
