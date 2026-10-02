# PersianLocalization (فارسی‌سازی ماتومو)

پلاگین سفارشی برای **ترجمهٔ کامل** و **رابط راست‌به‌چپ (RTL)** وقتی زبان **فارسی (fa)** در Matomo انتخاب شده است.

## چرا پلاگین جدا؟

فایل‌های هستهٔ Matomo (`lang/`، `plugins/*/lang/` و …) با هر **به‌روزرسانی** جایگزین می‌شوند. این پلاگین در `plugins/PersianLocalization/` قرار دارد و در به‌روزرسانی معمولاً **حفظ** می‌شود؛ ترجمه‌های تکمیلی در `lang/fa.json` همین پلاگین بارگذاری می‌شوند و بر ترجمه‌های قبلی **اولویت** دارند.

---

## نصب روی هاست اشتراکی (بدون SSH — فقط PHP / FTP / File Manager)

**روی سرور هیچ Python یا SSH لازم نیست.** فایل `lang/fa.json` از قبل داخل پلاگین آماده است.

### ۱) Matomo را مثل همیشه نصب کنید

از نصب‌کنندهٔ هاست یا آپلود رسمی Matomo استفاده کنید (همان PHP + MySQL).

### ۲) پوشهٔ پلاگین را آپلود کنید

یکی از این روش‌ها:

- **FTP / File Manager:** پوشهٔ `PersianLocalization` (همین محتوای `plugins/PersianLocalization/`) را داخل مسیر  
  `matomo/plugins/PersianLocalization/`  
  روی هاست کپی کنید.
- **ZIP:** پوشه را zip کنید، در File Manager داخل `plugins/` extract کنید تا مسیر نهایی شود:  
  `plugins/PersianLocalization/plugin.json`

### ۳) از داخل Matomo فعال کنید

1. ورود به Matomo → **Administration (مدیریت)** → **Plugins (پلاگین‌ها)**  
2. **PersianLocalization** را **Activate (فعال)** کنید  
3. منوی کاربر (گوشه) → **Choose language** → **فارسی**  
4. **System → General Settings → Delete all caches** (یک بار)

بعد از این، با زبان فارسی باید RTL و ترجمه‌های مکمل اعمال شوند.

### ۴) بعد از به‌روزرسانی Matomo روی هاست

- معمولاً پوشهٔ `plugins/PersianLocalization/` **پاک نمی‌شود**.
- اگر هاست کل `plugins` را overwrite کرد، **دوباره همان پوشه را آپلود** کنید (نسخهٔ جدید از GitHub / PR).
- کش را از پنل Matomo پاک کنید.

**اسکریپت `scripts/build_translations.py` فقط برای توسعه‌دهنده است** (روی کامپیوتر شخصی، نه روی هاست). کاربر هاست فقط فایل‌های آمادهٔ پلاگین را آپلود می‌کند.

---

## فعال‌سازی (سرور با دسترسی کامل)

1. **مدیریت → پلاگین‌ها** → **PersianLocalization**  
2. زبان کاربر → **فارسی**

## بازسازی ترجمه (اختیاری — فقط روی PC، نه هاست)

اگر خودتان Matomo را از سورس به‌روز کردید و کلیدهای انگلیسی جدید اضاف شد:

```bash
pip install argostranslate
# یک بار: نصب مدل en→fa (دستور در مستندات argostranslate)
python3 plugins/PersianLocalization/scripts/build_translations.py
```

سپس `lang/fa.json` به‌روز را دوباره روی هاست آپلود کنید و کش Matomo را پاک کنید.

## محتوا

- `lang/fa.json` — ترجمه‌های مکمل (کلیدهای جاافتاده)
- `stylesheets/persian.less` — فونت Vazirmatn و RTL
- `javascripts/persian.js` — `dir=rtl` و جایگزینی «Matomo» در عنوان صفحه
