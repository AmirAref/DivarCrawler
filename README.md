<h1 dir="rtl">Crawler دیوار</h1>

این یک اسکریپت برای crawl کردن سایت [divar.ir](https://divar.ir) است، می تواند آگهی ها را بر اساس شهر یا دسته بندی  با اعمال محدودیت تعداد جمع آوری کند و می تواند لینک های آگهی ها و تلفن صاحبان آگهی ها را استخراج کند.
اسکریپت با کتابخانه‌ی selenium کار می کند که نیاز به web driver یک مرورگر دارد، من از مرورگر edge استفاده کردم اما می توانید با کمی ویرایش آن را با مرورگر خود تغییر دهید.
اسکریپت برای اینکه بتواند شماره تلفن ها را استخراج کند ، به یک شماره ایران نیاز دارد 



## راه اندازی برنامه

<h3 dir="rtl">config برنامه :</h3>

در فایل «config.py» متغیرها را برای cralwer شخصی سازی کنید

### نصب requirements:

```bash
pip install -r requirements.txt
```

### اجرای برنامه :

```bash
python bot.py
```

### اطلاعات مرورگر :

Microsoft edge (Version 93.0.961.52 (Official build) (64-bit) )


<br>
<hr>
<br>


# Divar.ir Crawler

This is a script to crawl on the site [divar.ir](https://divar.ir), can collect ads by city or category with restrictions on the number and can be ads and phone links Extract banner owners.
The script works with selenium which requires a browser web driver, I used the edge browser but you can modify it with your browser with a little editing.
The script needs an Iranian number to be able to extract phone numbers



## Start the app

### Config the app :

in `config.py` make customize the variables to crawler

### Install requirements :

```bash
pip install -r requirements.txt
```

### Run the app :

```bash
python bot.py
```

### Browser Info :

Microsoft edge (Version 93.0.961.52 (Official build) (64-bit) )
