# Compufield Digital Marketing section

The redesigned digital marketing pages for **compufield.com**: Advanced Diploma with AI, 9 course pages, fees, centres, reviews, and a PHP free-demo form.

Plain HTML, CSS, and a little JavaScript. No WordPress, no plugins, no outside form services.

## Pages

All filenames match the old pages, so Google rankings and existing links keep working.

| File | Page |
|---|---|
| `digital_marketing_course_mumbai.html` | Main page: Advanced Diploma in Digital Marketing with AI |
| `seo-courses-in-mumbai.html` | SEO with AI search optimisation |
| `social-media-marketing-courses-in-mumbai.html` | Social media marketing |
| `adwords-training-analytics-training-mumbai.html` | Google Ads & Analytics |
| `google-analytics-course.html` | Google Analytics 4 |
| `ai-tools-for-digital-marketing.html` | AI tools for digital marketing (**new page**) |
| `wordpress-course-in-mumbai.html` | WordPress |
| `email-marketing-course.html` | Email marketing |
| `online-reputation-management-training.html` | Online reputation management |
| `digital-marketing-course-for-marketing-students.html` | For MBA, BBA & BMS students |
| `digital-marketing-course-fee.html` | Fees and programmes |
| `digital-marketing-institute-near-me.html` | Centres: Kemps Corner, Bandra West, online |
| `digital-marketing-google-certification.html` | Reviews, certificates, classroom photos |
| `digital-marketing-thank-you.html` | Shown after the demo form is sent |
| `send-demo.php` | Emails each free-demo request |

These old duplicate URLs now forward to the right page: `seo-training-institute-mumbai.html` and `social-media-marketing-smo-courses.html`.

`compufield.com/digital` is not touched: it already forwards to `digital_marketing_course_mumbai.html`, which is the new main page.

## Uploading to compufield.com

Upload everything in the ZIP to the **website root** (the same folder as `index.html`). There are no subfolders and no `.htaccess` file, so nothing else on the server is touched:

- all `.html` files (replace the old ones)
- `send-demo.php` (new)
- `compufield-dm.css` and `compufield-dm.js` (new; unique names so they can't clash with other files)

You don't need to upload `_build/` or `README.md`.

Images are loaded from the folders already on compufield.com (`marketing-resource/`, `tb-slider-img/`, `images-prettyPhoto/`, `images/`). Leave those folders in place.

## The free demo form

- Every request is emailed to **compufield@gmail.com** and **fkhairaz@gmail.com** using PHP's built-in `mail()`.
- Each email includes a one-tap WhatsApp link to reply to the student.
- A copy of each request is also saved in `demo-leads-backup.php` in the website root, created automatically on the first request. Opening it in a browser shows "not found"; to read it, download it from cPanel File Manager or FTP and open it in Excel (it is CSV after the first line).
- Spam protection uses a hidden trap field and a minimum time on the form. No captcha or outside service is involved.

**After uploading, send one test request.** If the email doesn't arrive (check Spam too):

1. Make sure the hosting supports PHP `mail()`. Most cPanel hosting does.
2. In `send-demo.php`, set `$FROM` to a real mailbox on your domain (for example `website@compufield.com`), then ask your host to confirm SPF is set up for compufield.com. This keeps Gmail from marking the leads as spam.
3. Even if email fails, requests are still saved in `demo-leads-backup.php`, so no lead is lost.

To change who receives leads, edit `$TO` at the top of `send-demo.php`.

## Changing content

All text, fees, phone numbers, modules, and FAQs live in **`_build/content.py`**. Edit that file, then run:

```
python3 _build/build.py
```

Every page is regenerated, so a number changed once is changed everywhere. Design changes go in `compufield-dm.css`.

## Contact details used on every page

- WhatsApp: +91 98201 34058
- Kemps Corner: +91 98201 34058, 022 2367 6218
- Bandra West: +91 98333 61338
- Live online classes for every course

## Tracking kept from the old site

- GA4 `G-NRECGNQ9WZ`
- Google Ads `AW-1067469824`, `AW-860701278`, `AW-958172018`
- Meta Pixel `1505440246452344`

WhatsApp and phone clicks are sent to GA4 as `whatsapp_click` and `phone_click`. Each form submission fires `generate_lead` (GA4) and `Lead` (Meta) on the thank-you page. You can import `generate_lead` into Google Ads as a conversion.

The old Universal Analytics code (`UA-2802408-5`) was removed, since Google stopped that service in 2023.
