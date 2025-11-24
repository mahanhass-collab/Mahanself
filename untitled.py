import subprocess
import sys

# لیست کتابخانه‌هایی که می‌خوای نصب بشن
packages = ["telethon", "jdatetime", "pytz","asyncio"]

def install_packages():
    for package in packages:
        try:
            print(f"در حال نصب {package} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"خطا در نصب {package}: {e}")

if __name__ == "__main__":
    install_packages()
    print("✅ همه کتابخانه‌ها نصب شدند یا قبلاً نصب بودن.")