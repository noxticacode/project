import config, sys, os, requests

from plugins import Database
from pyrogram import Client, enums
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats

data = []

class Bot(Client):
    def __init__(self, scheduler=None):
        super().__init__(
            'menfess_bot',
            api_id=config.api_id,
            api_hash=config.api_hash,
            plugins={
                "root": "plugins"
            },
            bot_token=config.bot_token
        )
        self.scheduler = scheduler
        
    async def start(self):
        await super().start()
        bot_me = await self.get_me()

        db = Database(bot_me.id)
        os.system('cls')
        if not await db.cek_user_didatabase():
            print(f'[!] Menambahkan data bot ke database...')
            await db.tambah_databot()
        print("[!] Database telah ready")
        print(f"[!] Link Database Kamu : {config.db_url}")
        print("================")

        # FIX: Pengecekan bot sebagai admin di semua channel yang dikonfigurasi
        channels_to_check = [
            (config.channel_1, 'channel 1'), 
            (config.channel_2, 'channel 2'), 
            (config.channel_log, 'channel log')
        ]
        
        for channel_id, channel_name in channels_to_check:
            # Lewati jika ID channel tidak diatur atau menggunakan placeholder default
            if channel_id and channel_id != -100:
                try:
                    # export_chat_invite_link akan gagal jika bot bukan admin
                    await self.export_chat_invite_link(channel_id) 
                except Exception as e:
                    print(f'Harap periksa kembali ID [ {channel_id} ] pada {channel_name}')
                    print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin. Error: {e}')
                    print('-> Bot terpaksa dihentikan')
                    sys.exit()

        self.username = bot_me.username
        self.id_bot = bot_me.id
        data.append(self.id_bot)
        await self.set_bot_commands([
            BotCommand('status', '🍃 check status'), BotCommand('talent', '👙 talent konten / vcs'),
            BotCommand('daddysugar', '👔 daddy sugar trusted'), BotCommand('moansgirl', '🧘‍♀️ moans girl'),
            BotCommand('moansboy', '🧘 moans boy'), BotCommand('gfrent', '🤵 girl friend rent'),
            BotCommand('bfrent', '🤵 boy friend rent')
        ], BotCommandScopeAllPrivateChats())

        # FIX: Memulai scheduler di dalam event loop Pyrogram
        if self.scheduler:
            self.scheduler.start()
            print("[!] Scheduler berhasil diaktifkan")
        
        print('BOT TELAH AKTIF')
    
    async def stop(self):
        await super().stop()
        # Mematikan scheduler dengan aman
        if self.scheduler:
            self.scheduler.shutdown()
        print('BOT BERHASIL DIHENTIKAN')
    
    async def kirim_pesan(self, x: str):
        db = Database(config.id_admin).get_pelanggan()
        pesan = f'<b>TOTAL USER ( {db.total_pelanggan} ) PENGGUNA 📊</b>\n'
        pesan += f'➜ <i>Total user yang mengirim menfess hari ini adalah {x}/{db.total_pelanggan} user</i>\n'
        pesan += f'➜ <i>Berhasil direset menjadi 0 menfess</i>'
        url = f'https://api.telegram.org/bot{config.bot_token}'
        a = requests.get(f'{url}/sendMessage?chat_id={config.channel_log}&text={pesan}&parse_mode=HTML').json()
        requests.post(f'{url}/pinChatMessage?chat_id={config.channel_log}&message_id={a["result"]["message_id"]}&parse_mode=HTML')
        requests.post(f'{url}/deleteMessage?chat_id={config.channel_log}&message_id={a["result"]["message_id"] + 1}&parse_mode=HTML')
