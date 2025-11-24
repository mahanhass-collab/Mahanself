import os
import subprocess
import sys

# اسم محیط مجازی
venv_dir = "myenv"

def run(cmd):
    print(f"▶ اجرا: {' '.join(cmd)}")
    subprocess.check_call(cmd)

def main():
    # اگر محیط وجود نداره، بساز
    if not os.path.exists(venv_dir):
        run([sys.executable, "-m", "venv", venv_dir])

    # مسیر pip داخل محیط
    pip_path = os.path.join(venv_dir, "bin", "pip")

    # لیست کتابخانه‌ها
    packages = ["telethon", "jdatetime", "pytz"]

    # نصب کتابخانه‌ها
    for pkg in packages:
        try:
            run([pip_path, "install", pkg])
        except subprocess.CalledProcessError as e:
            print(f"❌ خطا در نصب {pkg}: {e}")

    print("✅ همه کتابخانه‌ها نصب شدند یا قبلاً نصب بودن.")

if __name__ == "__main__":
    main()