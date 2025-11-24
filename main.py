import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import jdatetime
import calendar
import logging
import pytz
import os

# اطلاعات API تلگرام
api_id = 39396253
api_hash = 'cda50600795c48679b321223103d9443'

client = TelegramClient('session2', api_id, api_hash)

# آی‌دی تلگرام شما
allowed_user_id = 7254809297  # آی‌دی خودتان را اینجا وارد کنید

# لیست دشمنان و دوستان
enemies = {}
friends = {}

# پاسخ‌های دشمنان
enemy_responses = [
    "یا الله کیرم به قلب مادرت",
    "مادرتو میدم سگ بگاد",
    "با کیرم ناموستو پاره میکنم",
    "کیرمو حلقه میکنم دور گردن مادرت",
    "کسخارتو بتن ریزی کردم",
    "ننتو تو پورن هاب دیدم",
    "کیر و خایه هام به کل اجدادت",
    "فیلم ننت فروشی",
    "کسننت پدرتم",
    "میرم تو کسمادرت با بیل پارش میکنم",
    "کیر به ناموس گشادت",
    "خسته نشدی ننتو گاییدم؟",
    "کیرم شلاقی به ناموس جندت",
    "با ناموست تریسام زدم",
    "برج خلیفه تو مادرت",
    "دو پایی میرم تو کسمادرت",
    "داگی استایل ننتو گاییدم",
    "هندل زدم به کون مادرت گاییدمش",
    "یگام دو گام ننتو میگام",
    "کیرمو نکن تو کسمادرت",
    "کیر و خایم به توان دو تو کسمادرت",
    "قمه تو کسمادرت",
    "نود ننتو دارم مادرکسده",
    "با کله میرم تو کسمادرت",
    "دستام تو کسمادرت",
    "کیرم به استخون های ننت",
    "مادرتو حراج زدم مادرجنده",
    "بریم برای راند بعد با ننت",
    "کیرم به رحم نجس ننت",
    "کیرم به چش و چال ننت",
    "کیروم به فرق سر ناموست",
    "مادرجنده کیری ناموس",
    "با کون ننت ناگت درست کردم",
    "خایه هام به کسمادرت",
    "برج میلاد تو کسمادرت",
    "یخچال تو کسمادرت",
    "کیرم به پوزه مادرت",
    "مادرتو زدم به سیخ",
    "کسمادرت","کیر شتر تو ناموست","نودا ننت فروشی",
    "خایه با پرزش تو ننت","چشای ننت تو کون خارت بره","ننتو ریدم",
    "لال شو مادرجنده اوبنه ای","اوب از کون ننت میباره","ماهی تو کسمادرت",
    "کیر هرچی خره تو کسمادرت","کیر رونالدو به کس خار و مادرت",
    "مادرت زیر کیرم شهید شد","اسپنک زدم به کون مادر جندت",
    "کیرم یهویی به مردع و زندت","کیر به فیس ننت","برو مادرجنده بی غیرت",
    "استخون های مرده هات تو کسمادرت","اسپرمم تو نوامیست",
    "مادرتو با پوزیشن های مختلف گاییدم","میز و صندلی تو کسمادرت",
    "کیر به ناموس دلقکت","دمپایی تو کون ننت",
    "دماغ پینوکیو رو گذاشتم جلو کص مادرت و بهش گفتم که بگه مادرت جنده نیست تا با دراز شدن دماغش کص مادرت پاره بشه",
    "مادر فلش شده جوری با کیر میزنم ب فرق سر ننت ک حافظش بپره","كيرم شيك تو كس ننت",
    "مادرتو کردم تو بشکه نفت از بالا کوه قل دادم پایین",
    "با کیرم مادرتو هیپنوتیزم کردم","ناموستو تو کوچه موقع عید دیدنی دیدم رفتم خونه به یادش جق زدم",
    "با خیسی عرق کون مادرت جقیدم",
    "با سرعت نور تو فضا حرکت میکنم تا پیر نشم و بزارم آبجی کوچیکت بزرگ بشه تا وقتی بزرگ شد باهاش سکس کنم",
    "مادرتو پودر میکنم ازش سنگ توالت میسازم هر روز صبح رو مادرت میرینم",
    "مادرتو مجبور میکنم خودکشی کوانتومی کنه تا در بی نهایت جهان موازی یتیم بشی",
    "دیدی چه لگدی به مادرت زدم ؟",
    "فرشی که مادرت روش کونشو گذاشته بو کردم",
    "مادرتو جوری گاییدم که همسایه ها فکر کردن اسب ترکمن اومده خونتون"
]

# پاسخ‌های دوستان
friend_responses = [
    "کیرتم مشتی","بشاش شنا کنم","شق کن بارفیکس برم","کیرتو بخورم ستون",
    "جات رو کیرمه مشتی","کیرتو بده لیس بزنیم","خایه هام مال خودت مشتی",
    "داشمی","تاج سری ستونم","کیرت تو کسمادر بدخات","مادر بدخاتو گاییدم",
    "ایدی بدخا بده ننشو بگام","کیر تو ناموس کسی که ازت بدش بیاد","خایتو بخورم ستونم",
    "بمولا که عشقمی","دوست دارم داپشی","ناموس بدخاتو گاییدم","کیرت تو دنیا",
    "بکش پایین بکنمت","رفاقت ابدی داپش","کیرتو الکسیس بخوره","امار ننه بدخاتو دربیارم؟",
    "بدخات ننش شب خوابه","کیرت تو هرچی ادم مادرجندس","کیرمون تو کسمادر بدخات",
    "کسخار دنیا داپش","هعی مشتی کیر تو روزگار","رفاقت پابرجا",
    "گاییدن کونت بهترین لذته","کیرم به کونت بیب"
]

user_response_queue = {}

# روزها و ماه‌ها
day_names_fa = {
    "Sunday": "یکشنبه","Monday": "دوشنبه","Tuesday": "سه‌شنبه",
    "Wednesday": "چهارشنبه","Thursday": "پنج‌شنبه","Friday": "جمعه","Saturday": "شنبه"
}

month_names_fa = {
    "January": "ژانویه","February": "فوریه","March": "مارس",
    "April": "آوریل","May": "مه","June": "ژوئن","July": "جولای",
    "August": "اوت","September": "سپتامبر","October": "اکتبر",
    "November": "نوامبر","December": "دسامبر"
}

jalali_month_names_fa = [
    "فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور",
    "مهر","آبان","آذر","دی","بهمن","اسفند"
]

# تابع دریافت زمان تهران
def get_date_time_info():
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)

    gregorian_date = now.strftime("%Y/%m/%d")
    time_now = now.strftime("%H:%M:%S")
    jalali_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
    jalali_month_index = int(jdatetime.datetime.now().strftime("%m")) - 1
    day_name_en = calendar.day_name[now.weekday()]
    month_name_en = calendar.month_name[now.month]
    day_name_fa = day_names_fa[day_name_en]
    month_name_fa = month_names_fa[month_name_en]
    jalali_month_name_fa = jalali_month_names_fa[jalali_month_index]
    utc_date = datetime.utcnow().strftime("%A %Y-%m-%d %H:%M:%S")

    return {
        'gregorian_date': gregorian_date,'jalali_date': jalali_date,
        'time_now': time_now,'day_name_en': day_name_en,'day_name_fa': day_name_fa,
        'month_name_en': month_name_en,'month_name_fa': month_name_fa,
        'jalali_month_name_fa': jalali_month_name_fa,'utc_date': utc_date
    }

# تابع ارسال پاسخ‌ها
async def send_ordered_reply(event, responses_list):
    sender_id = event.sender_id
    if sender_id not in user_response_queue: user_response_queue[sender_id] = 0
    index = user_response_queue[sender_id]
    if index < len(responses_list):
        response = responses_list[index]
        await event.reply(response)
        user_response_queue[sender_id] = index + 1

# تابع ذخیره مدیا
async def save_media_to_saved(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        if event.raw_text.strip().lower() == "سیو" and replied_message.media:
            try:
                await event.message.delete()
                media = await client.download_media(replied_message.media)
                await client.send_file('me', media)
                await client.send_message('me', "مدیا مورد نظر با موفقیت ذخیره شد✓")
            except Exception as e:
                print(f"خطا در پردازش مدیا: {e}")

# تغییر نام
async def handle_name_change(event):
    match = re.match(r"اسم عوض بشه به (.+)", event.raw_text)
    if match:
        new_name = match.group(1)
        try: await client(UpdateProfileRequest(first_name=new_name))
        except Exception as e: logging.error(f"خطا در تغییر نام پروفایل: {e}")

# لیست دستورات
async def send_and_replace_command_list(event):
    command_list_text = """
لیست دستورات سلف Terminator ⩐

✚تنظیم بدخا (با ریپلای روی فرد اضافه شود)
✚حذف بدخا (با ریپلای روی فرد حذف شود)
✚تنظیم مشتی (با ریپلای روی فرد اضافه شود)
✚حذف مشتی (با ریپلای روی فرد حذف شود)
✚تاریخ و ساعت
✚سیو
✚تایم روشن
✚تایم خاموش
✚اسم عوض بشه به x
"""
    await event.message.edit(command_list_text)

# مدیریت لیست‌ها
async def manage_lists_via_reply(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        if replied_message is not None:
            sender_id = replied_message.sender_id
        if 'تنظیم بدخا' in event.raw_text: enemies[sender_id] = 'دشمن'; await event.message.edit("کاربر به لیست بدخات اضافه شد ننش گاییدس")
        elif 'تنظیم مشتی' in event.raw_text: friends[sender_id] = 'دوست'; await event.message.edit("کاربر به لیست مشتیا اضافه شد")
        elif 'حذف بدخا' in event.raw_text: enemies.pop(sender_id, None); await event.message.edit("کاربر از لیست دشمنان حذف شد")
        elif 'حذف مشتی' in event.raw_text: friends.pop(sender_id, None); await event.message.edit("کاربر از لیست دوستان حذف شد")

# کنترل تایم
time_enabled = False
def convert_to_classic_font(text):
    font_map = str.maketrans('0123456789','𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿')
    return text.translate(font_map)

async def update_profile_name(client):
    global time_enabled
    while True:
        if time_enabled:
            tehran_tz = pytz.timezone("Asia/Tehran")
            now = datetime.now(tehran_tz)
            time_now_classic = convert_to_classic_font(f"{now.hour}:{now.minute:02d}")
            me = await client.get_me()
            current_name = me.first_name
            new_name = re.sub(r'\s*[𝟶-𝟿]{1,2}:[𝟶-𝟿]{2}\s*', '', current_name)
            new_name = f"{new_name.strip()} {time_now_classic}"
            try: await client(UpdateProfileRequest(first_name=new_name))
            except Exception as e: print(f"خطا در به‌روزرسانی نام پروفایل: {e}")
        await asyncio.sleep(35)

# دستورات تایم
async def handle_commands(event):
    global time_enabled
    if event.text.lower() == "تایم روشن":
        time_enabled = True
    elif event.text.lower() == "تایم خاموش":
        time_enabled = False
        me = await event.client.get_me()
        current_name = me.first_name
        new_name = re.sub(r'\s*[𝟶-𝟿]{1,2}:[𝟶-𝟿]{2}\s*', '', current_name)
        try: await event.client(UpdateProfileRequest(first_name=new_name.strip()))
        
# رویداد جدید
@client.on(events.NewMessage)
async def new_message_handler(event):
    await send_and_replace_command_list(event)
    await handle_name_change(event)
    await manage_lists_via_reply(event)
    await save_media_to_saved(event)
    await handle_commands(event)
    sender = event.sender_id
    if sender in enemies: await send_ordered_reply(event, enemy_responses)
    elif sender in friends: await send_ordered_reply(event, friend_responses)

async def main():
    await client.start()
    asyncio.create_task(update_profile_name(client))
    print("ربات در حال اجراست...")
    await asyncio.Future()  # نگه داشتن برنامه

if __name__ == "__main__":
    asyncio.run(main())
