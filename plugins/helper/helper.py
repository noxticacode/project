import config
import pytz

import pyrogram
from pyrogram.errors import UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Update
from pyrogram import enums, Client

from datetime import datetime

from ..database import Database
from .waktu import Waktu


class Helper():
    def __init__(self, bot: Client, message: Message):
# ... __init__ methods ...

    async def escapeHTML(self, text: str):
        if text == None:
            return ''
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    async def cek_langganan_channel(self, user_id: int):
        if user_id == config.id_admin:
            return True
            
        required_channels = [config.channel_1, config.channel_2]
        
        for channel_id in required_channels:
            # Lewati jika ID channel tidak diatur atau menggunakan placeholder default
            if not channel_id or channel_id == -100:
                continue 
            
            try:
                member = await self.bot.get_chat_member(channel_id, user_id)
            except UserNotParticipant:
                # Jika user TIDAK menjadi anggota di salah satu channel yang wajib, langsung kembalikan False
                return False 
            except Exception as e:
                # Tangani kesalahan lain dan anggap sebagai kegagalan dalam pengecekan
                print(f"Error checking channel {channel_id}: {e}")
                return False 

            status = [
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.MEMBER,
                enums.ChatMemberStatus.ADMINISTRATOR
            ]
            
            # Periksa apakah status user adalah anggota aktif
            if not member.status in status:
                return False # Status user tidak valid (misalnya, DIBLOKIR, KELUAR)

        # Jika lolos semua pengecekan channel
        return True 

    async def pesan_langganan(self):
# ... rest of the file
