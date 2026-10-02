# PersianLocalization (فارسی‌سازی ماتومو)

پلاگین سفارشی برای **ترجمهٔ کامل** و **رابط راست‌به‌چپ (RTL)** وقتی زبان **فارسی (fa)** در Matomo انتخاب شده است.

## چرا پلاگین جدا؟

فایل‌های هستهٔ Matomo (`lang/`، `plugins/*/lang/` و …) با هر **به‌روزرسانی** جایگزین می‌شوند. این پلاگین در `plugins/PersianLocalization/` قرار دارد و در به‌روزرسانی معمولاً **حفظ** می‌شود؛ ترجمه‌های تکمیلی در `lang/fa.json` همین پلاگین بارگذاری می‌شوند و بر ترجمه‌های قبلی **اولویت** دارند.

## فعال‌سازی

1. از **مدیریت → پلاگین‌ها**، **PersianLocalization** را فعال کنید (در نصب‌های جدید این fork ممکن است از قبل فعال باشد).
2. از منوی کاربر، زبان **فارسی** را انتخاب کنید.

## بعد از به‌روزرسانی Matomo

کلیدهای ترجمهٔ جدید انگلیسی ممکن است اضافه شوند. برای تکمیل `fa.json`:

```bash
pip install deep-translator
python3 plugins/PersianLocalization/scripts/build_translations.py
```

سپس کش Matomo را خالی کنید (System → General Settings → Delete all caches).

## محتوا

- `lang/fa.json` — ترجمه‌های مکمل (کلیدهای جاافتاده)
- `stylesheets/persian.less` — فونت Vazirmatn و RTL
- `javascripts/persian.js` — `dir=rtl` و جایگزینی «Matomo» در عنوان صفحه
