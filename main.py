import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import jdatetime
import calendar
import logging
import os
import pytz

# اطلاعات API تلگرام
api_id = 39396253
api_hash = 'cda50600795c48679b321223103d9443'

client  = TelegramClient('session2', api_id, api_hash)

# آی‌دی تلگرام شما
allowed_user_id = 7254809297  # آی‌دی خودتان را اینجا وارد کنید

# لیست دشمنان و دوستان
enemies = {}
friends = {}

# لیست متون برای پاسخ به دشمنان و دوستان
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
    "کسمادرت","کیر شتر تو ناموست","نودا ننت فروشی","خایه با پرزش تو ننت",
    "چشای ننت تو کون خارت بره","ننتو ریدم","لال شو مادرجنده اوبنه ای","اوب از کون ننت میباره",
    "ماهی تو کسمادرت","کیر هرچی خره تو کسمادرت","کیر رونالدو به کس خار و مادرت",
    "مادرت زیر کیرم شهید شد","اسپنک زدم به کون مادر جندت","کیرم یهویی به مردع و زندت",
    "کیر به فیس ننت","برو مادرجنده بی غیرت","استخون های مرده هات تو کسمادرت",
    "اسپرمم تو نوامیست","مادرتو با پوزیشن های مختلف گاییدم","میز و صندلی تو کسمادرت",
    "کیر به ناموس دلقکت","دمپایی تو کون ننت","دماغ پینوکیو رو گذاشتم جلو کص مادرت و بهش گفتم که بگه مادرت جنده نیست تا با دراز شدن دماغش کص مادرت پاره بشه",
    "مادر فلش شده جوری با کیر میزنم ب فرق سر ننت ک حافظش بپره","كيرم شيك تو كس ننت","مادرتو کردم تو بشکه نفت از بالا کوه قل دادم پایین",
    "با کیرم مادرتو هیپنوتیزم کردم","ناموستو تو کوچه موقع عید دیدنی دیدم رفتم خونه به یادش جق زدم",
    "با خیسی عرق کون مادرت جقیدم","با سرعت نور تو فضا حرکت میکنم تا پیر نشم و بزارم آبجی کوچیکت بزرگ بشه تا وقتی بزرگ شد باهاش سکس کنم",
    "مادرتو پودر میکنم ازش سنگ توالت میسازم هر روز صبح رو مادرت میرینم","مادرتو مجبور میکنم خودکشی کوانتومی کنه تا در بی نهایت جهان موازی یتیم بشی",
    "دیدی چه لگدی به مادرت زدم ؟","فرشی که مادرت روش کونشو گذاشته بو کردم","مادرتو جوری گاییدم که همسایه ها فکر کردن اسب ترکمن اومده خونتون"
]

friend_responses = [
    "کیرتم مشتی","بشاش شنا کنم","شق کن بارفیکس برم","کیرتو بخورم ستون","جات رو کیرمه مشتی",
    "کیرتو بده لیس بزنیم","خایه هام مال خودت مشتی","داشمی","تاج سری ستونم","کیرت تو کسمادر بدخات",
    "مادر بدخاتو گاییدم","ایدی بدخا بده ننشو بگام","کیر تو ناموس کسی که ازت بدش بیاد","خایتو بخورم ستونم",
    "بمولا که عشقمی","دوست دارم داپشی","ناموس بدخاتو گاییدم","کیرت تو دنیا","بکش پایین بکنمت",
    "رفاقت ابدی داپش","کیرتو الکسیس بخوره","امار ننه بدخاتو دربیارم؟","بدخات ننش شب خوابه","کیرت تو هرچی ادم مادرجندس",
    "کیرمون تو کسمادر بدخات","کسخار دنیا داپش","هعی مشتی کیر تو روزگار","رفاقت پابرجا","گاییدن کونت بهترین لذته","کیرم به کونت بیب"
]

user_response_queue = {}

# timezone ایران
iran_tz = pytz.timezone('Asia/Tehran')

day_names_fa = {
    "Sunday": "یکشنبه","Monday": "دوشنبه","Tuesday": "سه‌شنبه","Wednesday": "چهارشنبه",
    "Thursday": "پنج‌شنبه","Friday": "جمعه","Saturday": "شنبه"
}

month_names_fa = {
    "January": "ژانویه","February": "فوریه","March": "مارس","April": "آوریل",
    "May": "مه","June": "ژوئن","July": "جولای","August": "اوت",
    "September": "سپتامبر","October": "اکتبر","November": "نوامبر","December": "دسامبر"
}

jalali_month_names_fa = [
    "فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور",
    "مهر","آبان","آذر","دی","بهمن","اسفند"
]

def convert_to_classic_font(text):
    font_map = str.maketrans('0123456789','𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿')
    return text.translate(font_map)

def get_date_time_info():
    now = datetime.now(iran_tz)
    gregorian_date = now.strftime("%Y/%m/%d")
    time_now = now.strftime("%H:%M:%S")
    jalali_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
    day_name_en = calendar.day_name[now.weekday()]
    month_name_en = calendar.month_name[now.month]
    day_name_fa = day_names_fa[day_name_en]
    month_name_fa = month_names_fa[month_name_en]
    jalali_month_index = int(jdatetime.datetime.now().strftime("%m")) - 1
    jalali_month_name_fa = jalali_month_names_fa[jalali_month_index]
    utc_date = datetime.utcnow().strftime("%A %Y-%m-%d %H:%M:%S")
    return {
        'gregorian_date': gregorian_date,'jalali_date': jalali_date,'time_now': time_now,
        'day_name_en': day_name_en,'day_name_fa': day_name_fa,'month_name_en': month_name_en,
        'month_name_fa': month_name_fa,'jalali_month_name_fa': jalali_month_name_fa,'utc_date': utc_date
    }

time_enabled = False
is_client_active = True

async def send_ordered_reply(event,responses_list):
    sender_id = event.sender_id
    if sender_id not in user_response_queue: user_response_queue[sender_id]=0
    index = user_response_queue[sender_id]
    if index < len(responses_list):
        await event.reply(responses_list[index])
        user_response_queue[sender_id] = index + 1

async def save_media_to_saved(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        if event.raw_text.strip().lower()=="سیو" and replied_message.media:
            try:
                await event.message.delete()
                media = await client.download_media(replied_message.media)
                await client.send_file('me',media)
                await client.send_message('me',"مدیا مورد نظر با موفقیت ذخیره شد✓")
            except Exception as e:
                print(f"خطا در پردازش مدیا: {e}")

async def handle_name_change(event):
    match = re.match(r"اسم عوض بشه به (.+)", event.raw_text)
    if match:
        new_name = match.group(1)
        try:
            await client(UpdateProfileRequest(first_name=new_name))
            await event.message.edit("اسم مورد نظر با موفقیت عوض شد✓")
        except Exception as e:
            logging.error(f"خطا در تغییر نام پروفایل: {e}")

async def send_and_replace_command_list(event):
    command_list_text = """لیست دستورات سلف Terminator ⩐

✚تنظیم بدخا (با ریپلای کردن دستور روی فرد مورد نظر، کاربر به لیست بدخاها اضافه می‌شود و به ازای هر پیامی که از کاربر ارسال شود، پیام‌های مربوط به بخش بدخا به ترتیب روی کاربر ریپلای می‌شود.)

✚حذف بدخا (با ریپلای کردن این دستور روی کاربر مورد نظر، کاربر از لیست بدخاها حذف می‌شود.)

✚تنظیم مشتی (با ریپلای کردن این دستور روی کاربر مورد نظر، کاربر به لیست مشتی‌ها اضافه می‌شود و به ازای هر پیامی که از کاربر ارسال شود، پیام‌های مربوط به بخش مشتی به ترتیب روی کاربر ریپلای می‌شود.)

✚حذف مشتی (با ریپلای کردن این دستور روی کاربر مورد نظر، کاربر از لیست مشتی‌ها حذف می‌شود.)

✚تاریخ و ساعت (با ارسال این دستور، تاریخ و ساعت به میلادی و شمسی با دو زبان فارسی و انگلیسی ارسال می‌شود.)

✚سیو (با ریپلای کردن این دستور روی مدیا مورد نظر در گپ پرایوت، مدیا به سیو مسیج ارسال می‌شود.)

✚تایم روشن (با ارسال این دستور، ساعت و دقیقه به میلادی با فونت کنار اسم ظاهر و هر دقیقه بروز می‌شود.)

✚تایم خاموش (با ارسال این دستور، ساعت و دقیقه به میلادی از کنار اسم حذف و دیگر نمایان نمی‌شود.)

✚اسم عوض بشه به x (با ارسال این دستور، اسم اکانت به اسمی تغییر می‌کند که بجای x قرار داده شود.)
"""
    await event.message.edit(command_list_text)

async def manage_lists_via_reply(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        if replied_message is not None:
            sender_id = replied_message.sender_id
        if 'تنظیم بدخا' in event.raw_text: enemies[sender_id]='دشمن';response_text="کاربر به لیست بدخات اضافه شد ننش گاییدس"
        elif 'تنظیم مشتی' in event.raw_text: friends[sender_id]='دوست';response_text="کاربر به لیست مشتیا اضافه شد"
        elif 'حذف بدخا' in event.raw_text:
            if sender_id in enemies: del enemies[sender_id];response_text="کاربر بهش رحم شد و از لیست بدخاها حذف شد"
            else: response_text="کاربر در لیست دشمنان نیست."
        elif 'حذف مشتی' in event.raw_text:
            if sender_id in friends: del friends[sender_id];response_text="کاربر از لیست مشتیا حذف شد کون لقش"
            else: response_text="کاربر در لیست دوستان نیست."
        else: return
        try: await event.message.edit(response_text)
        except Exception as e: print(f"خطا در ویرایش پیام: {e}")

async def update_profile_name(client):
    global time_enabled
    while True:
        if time_enabled:
            now = datetime.now(iran_tz)
            hour,minute=now.hour,now.minute
            time_now = f"{hour}:{minute:02d}"
            time_now_classic = convert_to_classic_font(time_now)
            me = await client.get_me()
            current_name = me.first_name
            new_name = re.sub(r'\s*[𝟶-𝟿]{1,2}:[𝟶-𝟿]{2}\s*','',current_name)
            new_name = f"{new_name.strip()} {time_now_classic}"
            try: await client(UpdateProfileRequest(first_name=new_name))
            except Exception as e: print(f"خطا در به‌روزرسانی نام پروفایل: {e}")
        await asyncio.sleep(35)

async def handle_commands(event):
    global time_enabled
    if event.text.lower()=="تایم روشن":
        time_enabled=True
        await event.message.edit("تایم فعال شد✓")
        now = datetime.now(iran_tz)
        hour,minute=now.hour,now.minute
        time_now = f"{hour}:{minute:02d}"
        time_now_classic = convert_to_classic_font(time_now)
        me = await event.client.get_me()
        current_name = me.first_name
        new_name = re.sub(r'\s*[𝟶-𝟿]{1,2}:[𝟶-𝟿]{2}\s*','',current_name)
        new_name = f"{new_name.strip()} {time_now_classic}"
        try: await event.client(UpdateProfileRequest(first_name=new_name))
        except Exception as e: print(f"خطا در به‌روزرسانی نام پروفایل: {e}")
    elif event.text.lower()=="تایم خاموش":
        time_enabled=False
        await event.message.edit("تایم خاموش‌ شد✘")
        me = await event.client.get_me()
        current_name = me.first_name
        new_name = re.sub(r'\s*[𝟶-𝟿]{1,2}:[𝟶-𝟿]{2}\s*','',current_name)
        try: await event.client(UpdateProfileRequest(first_name=new_name.strip()))
        except Exception as e: print(f"خطا در به‌روزرسانی نام پروفایل: {e}")

async def handle_new_message(event):
    global is_client_active
    if "لیست دستورات" in event.raw_text: await send_and_replace_command_list(event)
    elif "تاریخ و ساعت" in event.raw_text:
        info = get_date_time_info()
        response_text = (
            f"ساعت : ({info['time_now']})\n"
            f"تاریخ : ({info['jalali_date']} - {info['gregorian_date']})\n"
            f"روز : ({info['day_name_fa']} - {info['day_name_en']})\n"
            f"ماه : ({info['jalali_month_name_fa']} - {info['month_name_en']})\n"
            f"روزهای باقی‌مانده تا پایان ماه: ({info['remaining_days_in_month']})\n"
            f"روزهای باقی‌مانده تا پایان سال: ({info['remaining_days_in_year']})\n"
            f"UTC :\n   ({info['utc_date']})"
        )
        await event.message.edit(response_text)
    elif event.sender_id in enemies:
        if is_client_active: await send_ordered_reply(event,enemy_responses)
    elif event.sender_id in friends:
        if is_client_active: await send_ordered_reply(event,friend_responses)
    await handle_name_change(event)
    await handle_commands(event)
    await save_media_to_saved(event)
    await manage_lists_via_reply(event)

async def main():
    await client.start()
    print("ربات در حال اجرا است...")
    asyncio.create_task(update_profile_name(client))
    await client.run_until_disconnected()  # ← اضافه شد تا برنامه زنده بمونه

@client.on(events.NewMessage)
async def new_message_handler(event):
    await handle_new_message(event)

if __name__=="__main__":
    asyncio.run(main())
