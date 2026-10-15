# -*- coding: utf-8 -*-
"""Builds every page of the Compufield Digital Marketing section.

    python3 _build/build.py

Reads _build/content.py and writes plain .html files to the repository root,
ready to upload to compufield.com (same filenames as the old pages).
"""
import json
import os
import sys
from html import escape
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HUB = "digital_marketing_course_mumbai.html"
FEES = "digital-marketing-course-fee.html"
CONTACT = "digital-marketing-institute-near-me.html"
REVIEWS = "digital-marketing-google-certification.html"
THANKS = "digital-marketing-thank-you.html"
YEAR = "2026"
ASSET_V = "20261015"


def e(s):
    return escape(s, quote=True)


def img(path):
    return f"{C.IMG}/{path}"


def wa(text):
    return f"https://wa.me/{C.WHATSAPP}?text={quote(text)}"


WA_ICON = ('<svg viewBox="0 0 32 32" aria-hidden="true" fill="currentColor"><path d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.2.6 4.4 1.7 6.3L3.2 29l7.3-1.9a12.7 12.7 0 0 0 5.5 1.3c7 0 12.7-5.7 12.7-12.7S23 3 16 3zm0 23.2c-1.9 0-3.8-.5-5.4-1.5l-.4-.2-4.3 1.1 1.1-4.2-.3-.4a10.5 10.5 0 1 1 9.3 5.2zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.3 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>')
SEARCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>'


# ---------------------------------------------------------------------------
# Head, tracking, header, footer
# ---------------------------------------------------------------------------
def tracking(lead=False):
    ads = "\n".join(f"  gtag('config', '{i}');" for i in C.GOOGLE_ADS_IDS)
    lead_js = ""
    if lead:
        lead_js = "\n  gtag('event', 'generate_lead', {event_category: 'demo_form'});"
    fb_lead = "\n  fbq('track', 'Lead');" if lead else ""
    return f"""<!-- Google tag (GA4 + Google Ads) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={C.GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{C.GA4_ID}');
{ads}{lead_js}
  document.addEventListener('click', function (ev) {{
    var a = ev.target.closest && ev.target.closest('a[href*="wa.me"], a[href^="tel:"]');
    if (!a) return;
    var wa = a.href.indexOf('wa.me') > -1;
    gtag('event', wa ? 'whatsapp_click' : 'phone_click', {{link_url: a.href}});
    if (window.fbq) fbq('track', 'Contact');
  }});
</script>
<!-- Meta Pixel -->
<script>
  !function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
  document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '{C.META_PIXEL}');
  fbq('track', 'PageView');{fb_lead}
</script>
<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id={C.META_PIXEL}&amp;ev=PageView&amp;noscript=1"></noscript>"""


def head(title, description, file, schema=None, noindex=False, lead=False):
    seo = getattr(C, "SEO", {}).get(file, {})
    title = seo.get("title", title)
    description = seo.get("description", description)
    keywords = seo.get("keywords", "")
    canonical = f"{C.SITE}/{file}"
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    ld = ""
    for block in (schema or []):
        ld += '\n<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False, indent=1) + "</script>"
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{f'<meta name="keywords" content="{e(keywords)}">' if keywords else ''}
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#15244b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Compufield">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{C.IMG}/images/dm-post.png">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{C.IMG}/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="compufield-dm.css?v={ASSET_V}">
{tracking(lead)}{ld}
</head>
"""


def header(active=""):
    items = "".join(
        f'<li><a href="{c["file"]}"><b>{e(c["menu"])}</b><small>{e(c["menu_desc"])}</small></a></li>'
        for c in C.COURSES
    )
    items = f'<li><a href="{HUB}"><b>Advanced Diploma with AI</b><small>All 21 modules, about 3 months</small></a></li>' + items

    def cur(f):
        return ' aria-current="page"' if active == f else ""

    calls = " ".join(
        f'<a href="tel:{c["phones"][0][1]}">{c["name"]}: {c["phones"][0][0]}</a>' for c in C.CENTRES
    )
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap">
  <span>Classroom batches at Kemps Corner and Bandra West, or live online from anywhere</span>
  <span class="strip-calls">{calls}</span>
</div></div>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{HUB}"><img src="{img('images/education/header-logo.png')}" alt="Compufield Computer Institute" width="139" height="48"></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <div class="nav-courses">
        <button type="button" aria-expanded="false" aria-haspopup="true">Courses</button>
        <ul class="menu">{items}</ul>
      </div>
      <a href="{FEES}"{cur(FEES)}>Fees</a>
      <a href="{REVIEWS}"{cur(REVIEWS)}>Reviews</a>
      <a href="{CONTACT}"{cur(CONTACT)}>Centres</a>
      <a href="https://www.compufield.com/blog/">Blog</a>
      <a class="btn btn--demo" href="#demo">Free demo class</a>
    </nav>
  </div>
</header>
<main id="main">
"""


def footer():
    centre_cols = ""
    for c in C.CENTRES:
        phones = "".join(f'<li><a href="tel:{p[1]}">{p[0]}</a></li>' for p in c["phones"])
        centre_cols += f"""<div>
      <h3>{c['name']}</h3>
      <address>{c['address']}</address>
      <p class="small">{c['landmark']}</p>
      <ul>{phones}</ul>
    </div>"""
    course_links = "".join(f'<li><a href="{c["file"]}">{e(c["menu"])}</a></li>' for c in C.COURSES[:6])
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      {centre_cols}
      <div>
        <h3>Courses</h3>
        <ul><li><a href="{HUB}">Advanced Diploma with AI</a></li>{course_links}</ul>
      </div>
      <div>
        <h3>Talk to us</h3>
        <ul>
          <li><a href="{wa('Hi Compufield, I would like details about your digital marketing courses.')}">WhatsApp {C.WHATSAPP_SHOW}</a></li>
          <li><a href="mailto:{C.EMAIL_SHOW}">{C.EMAIL_SHOW}</a></li>
          <li><a href="{FEES}">Course fees</a></li>
          <li><a href="{CONTACT}">Directions to our centres</a></li>
          <li><a href="{REVIEWS}">Reviews and certificates</a></li>
        </ul>
        <p class="small">Live online classes available for every course.</p>
      </div>
    </div>
    <div class="foot-base">
      <span>&copy; {YEAR} Compufield Computer Institute, Mumbai. Training since 1985.</span>
      <a href="https://compufield.com/index.html">All Compufield courses</a>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa('Hi Compufield, I would like to book a free demo class for digital marketing.')}" aria-label="Chat with Compufield on WhatsApp">{WA_ICON}<span>WhatsApp us</span></a>
<script src="compufield-dm.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def demo_form(selected=None, heading="Book your free demo class", sub=None):
    selected = selected or C.COURSE_OPTIONS[0]
    sub = sub or "Sit in on a real class before you decide. Our team will call you to fix a time."
    copts = "".join(
        f'<option value="{e(o)}"{" selected" if o == selected else ""}>{e(o)}</option>' for o in C.COURSE_OPTIONS
    )
    centre = "".join(f'<option value="{e(o)}">{e(o)}</option>' for o in C.CENTRE_OPTIONS)
    batch = "".join(f'<option value="{e(o)}">{e(o)}</option>' for o in C.BATCH_OPTIONS)
    return f"""<aside class="demo" id="demo" aria-labelledby="demo-title">
  <h2 id="demo-title">{heading}</h2>
  <p>{sub}</p>
  <form class="demo-form" action="send-demo.php" method="post">
    <div class="field"><label for="d-name">Your name</label><input id="d-name" name="name" type="text" autocomplete="name" required maxlength="80"></div>
    <div class="field-row">
      <div class="field"><label for="d-phone">Mobile number</label><input id="d-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="20" placeholder="98XXXXXXXX"></div>
      <div class="field"><label for="d-email">Email <span class="opt">(optional)</span></label><input id="d-email" name="email" type="email" autocomplete="email" maxlength="120"></div>
    </div>
    <div class="field"><label for="d-course">Course</label><select id="d-course" name="course">{copts}</select></div>
    <div class="field"><label for="d-centre">Where would you like to learn?</label><select id="d-centre" name="centre" required>{centre}</select></div>
    <div class="field"><label for="d-batch">Preferred batch</label><select id="d-batch" name="batch">{batch}</select></div>
    <div class="hp" aria-hidden="true"><label for="d-website">Leave this empty</label><input id="d-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
    <input type="hidden" name="ts" value="">
    <input type="hidden" name="page" value="">
    <button class="btn btn--demo" type="submit">Book my free demo class</button>
  </form>
  <p class="demo-alt">Prefer chatting? <a href="{wa('Hi Compufield, I would like to book a free demo class for ' + selected + '.')}">WhatsApp {C.WHATSAPP_SHOW}</a></p>
</aside>"""


def syllabus(modules, numbered=True, open_first=True):
    out = []
    for i, m in enumerate(modules):
        name, line, topics, ai = m
        tag = '<span class="tag-ai">AI</span>' if ai else ""
        lis = "".join(f"<li>{e(t)}</li>" for t in topics)
        small = f"<small>{e(line)}</small>" if line else ""
        op = " open" if (open_first and i == 0) else ""
        n = f'<span class="n">{i + 1:02d}</span>' if numbered else '<span class="n"></span>'
        out.append(f"""<details{op}>
  <summary>{n}<span>{e(name)}{tag}{small}</span></summary>
  <div class="body"><ul>{lis}</ul></div>
</details>""")
    return f'<div class="syllabus">{"".join(out)}</div>'


def faq(faqs):
    items = "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faqs)
    return f'<div class="faq">{items}</div>'


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "Compufield Computer Institute",
        "url": f"{C.SITE}/{HUB}",
        "logo": img("images/education/header-logo.png"),
        "foundingDate": "1985",
        "email": C.EMAIL_SHOW,
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": C.RATING, "reviewCount": C.REVIEWS.rstrip("+"), "bestRating": "5"},
        "department": [
            {
                "@type": "EducationalOrganization",
                "name": f"Compufield {c['name']}",
                "telephone": c["phones"][0][1],
                "address": {"@type": "PostalAddress", "streetAddress": c["street"], "addressLocality": c["locality"], "postalCode": c["pin"], "addressRegion": "Maharashtra", "addressCountry": "IN"},
            }
            for c in C.CENTRES
        ],
    }


def course_schema(name, description, file, fee=None):
    d = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": name,
        "description": description,
        "url": f"{C.SITE}/{file}",
        "provider": {"@type": "EducationalOrganization", "name": "Compufield Computer Institute", "url": f"{C.SITE}/{HUB}"},
        "inLanguage": "en-IN",
        "hasCourseInstance": [
            {"@type": "CourseInstance", "courseMode": "Onsite", "location": {"@type": "Place", "name": f"Compufield {c['name']}", "address": c["address_plain"]}}
            for c in C.CENTRES
        ] + [{"@type": "CourseInstance", "courseMode": "Online"}],
    }
    if fee:
        d["offers"] = {"@type": "Offer", "price": fee.replace("₹", "").replace(",", ""), "priceCurrency": "INR", "category": "Paid"}
    return d


def breadcrumb(items):
    lis = "".join(
        f'<li><a href="{href}">{e(label)}</a></li>' if href else f'<li aria-current="page">{e(label)}</li>' for label, href in items
    )
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{lis}</ol></div></nav>'


def modes_block(course_name="digital marketing"):
    out = []
    for c in C.CENTRES:
        phones = "".join(f'<a class="call" href="tel:{p[1]}">{p[0]}</a>' for p in c["phones"])
        out.append(f"""<div class="mode">
  <h3>{c['name']} classroom</h3>
  <p class="where">{c['area']}. {c['landmark']}.</p>
  <p>Small batches on a computer each, with the trainer beside you.</p>
  {phones}
</div>""")
    out.append(f"""<div class="mode mode--online">
  <h3>Live online</h3>
  <p class="where">From anywhere in India or abroad</p>
  <p>Live, instructor-led classes with the same trainer, syllabus, projects and certificate. Not recorded videos.</p>
  <a class="call" href="{wa('Hi Compufield, I would like to join the ' + course_name + ' course online.')}">Ask about online batches on WhatsApp</a>
</div>""")
    return f'<div class="modes">{"".join(out)}</div>'


def quotes_block(n=6):
    out = []
    for name, role, photo, text in C.TESTIMONIALS[:n]:
        out.append(f"""<figure class="quote">
  <blockquote><p>{e(text)}</p></blockquote>
  <figcaption><img src="{img(photo)}" alt="" width="52" height="52" loading="lazy"><span><b>{e(name)}</b><span>{e(role)}</span></span></figcaption>
</figure>""")
    return f'<div class="quotes">{"".join(out)}</div>'


def videos_block(ids):
    return '<div class="videos">' + "".join(
        f'<button class="yt" type="button" data-id="{v}" aria-label="Play student review video {i + 1}"><span></span></button>' for i, v in enumerate(ids)
    ) + "</div>"


def logos_block():
    return '<div class="logos">' + "".join(
        f'<div><img src="{img("marketing-resource/images/logos/" + l + ".png")}" alt="Logo of a company that hired a Compufield student" loading="lazy"></div>' for l in C.PLACEMENT_LOGOS
    ) + "</div>"


def gallery_block(items, certs=False):
    cls = "gallery gallery--certs" if certs else "gallery"
    return f'<div class="{cls}">' + "".join(
        f'<a href="{img(p)}" target="_blank" rel="noopener"><img src="{img(p)}" alt="{e(a)}" loading="lazy"></a>' for p, a in items
    ) + "</div>"


def cta(text="Not sure which course is right for you?", sub="Come for a free demo class, at Kemps Corner, Bandra West or online, and talk to a trainer about your goals."):
    return f"""<section class="cta">
  <div class="wrap">
    <div><h2>{e(text)}</h2><p>{e(sub)}</p></div>
    <div class="btn-row">
      <a class="btn btn--ghost" href="#demo">Book a free demo class</a>
      <a class="btn btn--wa" href="{wa('Hi Compufield, please help me choose the right digital marketing course.')}">{WA_ICON}WhatsApp us</a>
    </div>
  </div>
</section>"""


def related(exclude):
    picks = [c for c in C.COURSES if c["file"] != exclude][:6]
    lis = "".join(f'<li><a href="{c["file"]}"><b>{e(c["menu"])}</b><span>{e(c["menu_desc"])}</span></a></li>' for c in picks)
    return f'<ul class="related">{lis}</ul>'


def tools_block(tools, light=True):
    cls = "tools tools--light" if light else "tools"
    return f'<ul class="{cls}">' + "".join(f"<li>{e(t)}</li>" for t in tools) + "</ul>"


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_hub():
    title = "Digital Marketing Course in Mumbai with AI 2026 | Advanced Diploma | Compufield"
    desc = "Advanced Diploma in Digital Marketing with AI in Mumbai: 21 modules, SEO, Google Ads, Meta Ads, GA4, ChatGPT & Canva AI, live projects, internship. ₹30,000. Kemps Corner, Bandra West & live online."
    sitelinks = [
        ("seo-courses-in-mumbai.html", "SEO & AI search", "Rank on Google and in AI answers"),
        ("social-media-marketing-courses-in-mumbai.html", "Social media marketing", "Instagram, Meta Ads, LinkedIn, YouTube"),
        ("adwords-training-analytics-training-mumbai.html", "Google Ads & Analytics", "Search, Performance Max, YouTube"),
        ("ai-tools-for-digital-marketing.html", "AI tools for marketing", "ChatGPT, Gemini, Canva AI, Firefly"),
        (FEES, "Course fees", "Diplomas from ₹30,000"),
        (CONTACT, "Our centres", "Kemps Corner, Bandra West, online"),
    ]
    sl = "".join(f'<li><a href="{h}"><b>{e(t)}</b><span>{e(d)}</span></a></li>' for h, t, d in sitelinks)
    audiences = [
        ("Working professionals", "becoming digital marketing experts"),
        ("Students", "building a career in digital marketing"),
        ("Marketing executives", "bringing relevant traffic and leads"),
        ("Entrepreneurs", "generating more enquiries and sales"),
        ("Freshers", "getting placed in the industry"),
    ]
    aud = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in audiences)
    ai_uses = [
        ("Keyword research and SEO", "AI topic clusters, content briefs, and optimising for AI Overviews"),
        ("Content and copy", "First drafts of blogs, captions and ad copy, edited by you"),
        ("Creatives", "Posts, carousels and infographics with Canva AI and Adobe Firefly"),
        ("Ads", "Performance Max, AI Max for Search, Meta Advantage+ and Smart Bidding"),
        ("Analytics", "Summarising GA4 and campaign data into clear reports"),
        ("Judgement", "Fact-checking, brand voice, and knowing when not to trust AI"),
    ]
    ai = "".join(f"<li><b>{a}</b>{b}</li>" for a, b in ai_uses)
    programmes_teaser = "".join(
        f'<li><a href="{FEES}"><b>{e(p["name"])}</b><span>{p["fee"]}, {e(p["length"])}</span></a></li>' for p in C.PROGRAMMES[:6]
    )

    body = f"""
<section class="serp-hero">
  <div class="wrap">
    <div>
      <div class="searchbox" role="presentation">{SEARCH_ICON}<span class="q" data-q="best digital marketing course in mumbai with ai">best digital marketing course in mumbai with ai</span></div>
      <div class="result">
        <div class="result-meta"><img src="{img('images/education/header-logo.png')}" alt=""><span><b>Compufield Computer Institute</b><i>compufield.com › digital</i></span></div>
        <h1>Advanced digital marketing course in Mumbai with AI, updated for 2026</h1>
        <p class="result-rating"><span class="stars" aria-hidden="true">★★★★★</span> Rated {C.RATING} from {C.REVIEWS} Google reviews. Training since 1985.</p>
        <p class="result-desc">21 practical modules, from SEO and Google Ads to Meta Ads, GA4 and WhatsApp marketing, with ChatGPT, Gemini and Canva AI used in every one. Job-ready in about 3 months with live projects, Google certifications and internship support. Classroom batches at Kemps Corner and Bandra West, or live online.</p>
        <ul class="sitelinks">{sl}</ul>
        <div class="btn-row">
          <a class="btn btn--demo" href="#demo">Book a free demo class</a>
          <a class="btn btn--wa" href="{wa('Hi Compufield, I would like details about the Advanced Diploma in Digital Marketing with AI.')}">{WA_ICON}WhatsApp {C.WHATSAPP_SHOW}</a>
        </div>
      </div>
    </div>
    {demo_form(C.COURSE_OPTIONS[0])}
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="numbers">
      <div><b>21</b><span>practical modules</span></div>
      <div><b>60+</b><span>hours of training</span></div>
      <div><b>15+</b><span>hours of live projects for real brands</span></div>
      <div><b>7+</b><span>certifications you can earn</span></div>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="section-head"><h2>Who joins this course</h2><p>No marketing or technical background needed. Batches mix students and working people, and timings are flexible.</p></div>
    <ul class="audience">{aud}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Learn in class or live online</h2><p>Weekday, weekend and fast-track batches at both centres. Online students get the same trainer, projects and certificate.</p></div>
    {modes_block("Advanced Diploma in Digital Marketing")}
  </div>
</section>

<section class="section section--white" id="syllabus">
  <div class="wrap">
    <div class="section-head"><h2>What you'll learn: 21 modules</h2><p>Updated for 2026. Tap a module to see its topics. Modules marked AI are new for this year; AI tools are used across all of them.</p></div>
    {syllabus(C.DIPLOMA_MODULES)}
    <p class="mt-l btn-row"><a class="btn btn--demo" href="#demo">Book a free demo class</a> <a class="btn btn--ghost" href="{FEES}">See fees and programmes</a></p>
  </div>
</section>

<section class="section band">
  <div class="wrap cols-2">
    <div>
      <h2>AI is built into every module</h2>
      <p class="lede">Employers now expect marketers to work with AI. You'll practise on real tasks, and learn where AI saves hours and where your judgement matters more.</p>
      {tools_block(["ChatGPT", "Google Gemini", "Microsoft Copilot", "Perplexity", "Canva AI", "Adobe Firefly", "Google Ads AI", "Meta Advantage+"], light=False)}
    </div>
    <ul class="ai-uses">{ai}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What our students say</h2><p>Rated {C.RATING} from {C.REVIEWS} reviews on Google.</p></div>
    {quotes_block()}
    <h3 class="mt-l">Video reviews</h3>
    {videos_block(C.VIDEOS[:3])}
    <p class="mt-l"><a href="{REVIEWS}">More reviews, certificates and classroom photos</a></p>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="section-head"><h2>Where our students work</h2><p>Internship support, interview preparation and placement assistance are part of the diploma.</p></div>
    {logos_block()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Google certificates earned by our students</h2><p>We prepare you for Google's free Skillshop certifications in Google Ads and Analytics.</p></div>
    {gallery_block(C.CERT_IMAGES[:6], certs=True)}
  </div>
</section>

<section class="section section--white">
  <div class="wrap cols-2">
    <div>
      <h2>Programmes and fees</h2>
      <p class="lede">Take the Advanced Diploma on its own, or combine it with web design, graphic design or MIS.</p>
      <p><a class="btn btn--ghost" href="{FEES}">Compare all programmes</a></p>
    </div>
    <ul class="related" style="grid-template-columns:1fr">{programmes_teaser}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap cols-2">
    <div><h2>Questions people ask before joining</h2><p class="muted">Something else? <a href="{wa('Hi Compufield, I have a question about the digital marketing course.')}">Ask us on WhatsApp</a>.</p></div>
    {faq(C.HUB_FAQS)}
  </div>
</section>

{cta()}
"""
    schema = [org_schema(), course_schema("Advanced Diploma in Digital Marketing with AI", desc, HUB, "₹30,000"), faq_schema(C.HUB_FAQS)]
    write(HUB, head(title, desc, HUB, schema) + header(HUB) + body + footer())


def page_course(c):
    modules = C.DIPLOMA_MODULES if c["modules"] == "DIPLOMA" else c["modules"]
    who = "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in c["who"])
    facts = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in c["facts"])
    fee = None
    for k, v in c["facts"]:
        if k == "Fee" and "₹" in v:
            fee = "₹" + v.split("₹")[1].split("<")[0]
    syl_title = "What you'll learn" if c["modules"] != "DIPLOMA" else "What you'll learn: all 21 diploma modules"
    body = f"""
{breadcrumb([("Digital marketing", HUB), (c["short"], None)])}
<section class="course-hero">
  <div class="wrap">
    <div>
      <h1>{e(c["h1"])}</h1>
      <p class="lede">{e(c["intro"])}</p>
      <dl class="facts">{facts}</dl>
      <div class="btn-row">
        <a class="btn btn--demo" href="#demo">Book a free demo class</a>
        <a class="btn btn--wa" href="{wa('Hi Compufield, I would like details about the ' + c['option'] + ' course.')}">{WA_ICON}WhatsApp us</a>
      </div>
    </div>
    {demo_form(c["option"])}
  </div>
</section>

<section class="section">
  <div class="wrap cols-2">
    <div><h2>Who this course is for</h2><p class="muted">No prior experience needed. Bring a laptop for online classes; classroom students get a computer each.</p></div>
    <ul class="ticks">{who}</ul>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="section-head"><h2>{syl_title}</h2><p>Updated for 2026. Tap a module to see its topics.</p></div>
    {syllabus(modules)}
    <h3 class="mt-l">Tools you'll use</h3>
    {tools_block(c["tools"])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Learn in class or live online</h2></div>
    {modes_block(c["option"])}
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="section-head"><h2>What our students say</h2><p>Rated {C.RATING} from {C.REVIEWS} Google reviews.</p></div>
    {quotes_block(3)}
  </div>
</section>

<section class="section">
  <div class="wrap cols-2">
    <div><h2>Frequently asked questions</h2><p class="muted">Want the full digital marketing skill set? See the <a href="{HUB}">Advanced Diploma in Digital Marketing with AI</a>.</p></div>
    {faq(c["faqs"])}
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <h2>Other courses</h2>
    {related(c["file"])}
  </div>
</section>

{cta()}
"""
    schema = [course_schema(c["option"], c["description"], c["file"], fee), faq_schema(c["faqs"])]
    write(c["file"], head(c["title"], c["description"], c["file"], schema) + header(c["file"]) + body + footer())


def page_fees():
    title = "Digital Marketing Course Fees in Mumbai 2026 | Compufield"
    desc = "Compufield digital marketing course fees 2026: Advanced Diploma with AI ₹30,000, combined web, graphic design and MIS diplomas, and short courses in SEO, social media, Google Ads and WordPress."
    progs = ""
    for p in C.PROGRAMMES:
        inc = "".join(f"<li>{e(i)}</li>" for i in p["includes"])
        intern = "Includes internship support" if p["internship"] else ""
        lead_cls = " programme--lead" if p.get("lead") else ""
        flag = '<span class="flag">Flagship programme</span>' if p.get("lead") else ""
        meta = e(p["length"]) + (f". {intern}" if intern else "")
        progs += f"""<div class="programme{lead_cls}">
  <div>{flag}<h3>{e(p['name'])}</h3><p class="meta">{meta}</p></div>
  <ul>{inc}</ul>
  <div class="cost"><b>{p['fee']}</b><span>Total fee</span><a class="btn btn--demo" href="#demo">Free demo class</a></div>
</div>"""
    shorts = [
        ("SEO with AI search optimisation", "seo-courses-in-mumbai.html", "2 to 3 weeks, about 20 hours", "₹12,000"),
        ("Social media marketing with AI content", "social-media-marketing-courses-in-mumbai.html", "About 20 sessions", "₹12,000"),
        ("Google Ads & Analytics", "adwords-training-analytics-training-mumbai.html", "About 20 sessions", "₹11,000"),
        ("WordPress website building", "wordpress-course-in-mumbai.html", "About 20 sessions", "₹8,500"),
        ("Google Analytics 4, AI tools, email marketing, ORM", "google-analytics-course.html", "Short courses", "Ask us"),
    ]
    rows = "".join(
        f'<tr><td><a href="{f}">{e(n)}</a></td><td>{e(d)}</td><td class="amt">{a}</td></tr>' for n, f, d, a in shorts
    )
    body = f"""
{breadcrumb([("Digital marketing", HUB), ("Fees", None)])}
<section class="course-hero">
  <div class="wrap">
    <div>
      <h1>Digital marketing with AI (2026): course fees & syllabus</h1>
      <p class="lede">One clear price for each programme. All programmes are available in the classroom at Kemps Corner or Bandra West, or as live online classes, at the same fee.</p>
      <dl class="facts">
        <dt>Diploma</dt><dd><span class="price">₹30,000</span> for the Advanced Diploma in Digital Marketing with AI</dd>
        <dt>Short courses</dt><dd>From ₹8,500</dd>
        <dt>Batches</dt><dd>Weekday, weekend or fast-track</dd>
        <dt>Payment</dt><dd>Ask us about payment options</dd>
      </dl>
    </div>
    {demo_form(C.COURSE_OPTIONS[0], sub="Try a class first. We'll also explain the fee and payment options on the call.")}
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="section-head"><h2>Diploma programmes</h2><p>Every diploma includes the full Advanced Diploma in Digital Marketing with AI.</p></div>
    <div class="programmes">{progs}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Short courses</h2><p>Learn one skill at a time. Each short course is also a part of the diploma.</p></div>
    <div class="table-scroll"><table class="fees"><thead><tr><th>Course</th><th>Duration</th><th>Fee</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p class="note mt-l">Fees are per student and include course material and the Compufield certificate. Google certification exams on Skillshop are free.</p>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="section-head"><h2>What's in the Advanced Diploma</h2></div>
    {syllabus(C.DIPLOMA_MODULES, open_first=False)}
  </div>
</section>

{cta("Want to talk through the fees?", "WhatsApp us or book a free demo class. We'll help you pick the programme that fits your goal and budget.")}
"""
    write(FEES, head(title, desc, FEES, [org_schema()]) + header(FEES) + body + footer())


def page_contact():
    title = "Digital Marketing Institute in Mumbai: Kemps Corner & Bandra West | Compufield"
    desc = "Visit Compufield's digital marketing institute at Kemps Corner (Warden Road) or Bandra West (near Mehboob Studio), or join live online. Addresses, phone numbers, maps and free demo booking."
    cards = ""
    for c in C.CENTRES:
        phones = "".join(f'<a href="tel:{p[1]}">{p[0]}</a>' for p in c["phones"])
        mapsrc = "https://maps.google.com/maps?q=" + quote(c["map_q"]) + "&output=embed"
        dirs = "https://www.google.com/maps/search/?api=1&query=" + quote(c["map_q"])
        cards += f"""<div class="centre">
  <div class="info">
    <h2>{c['name']}</h2>
    <address>{c['address']}</address>
    <p class="landmark">{c['landmark']}</p>
    <div class="phones">{phones}</div>
    <p class="btn-row" style="margin-top:14px">
      <a class="btn btn--wa" href="{wa('Hi Compufield, I would like to visit your ' + c['name'] + ' centre for a free demo class.')}">{WA_ICON}WhatsApp</a>
      <a class="btn btn--ghost" href="{dirs}" target="_blank" rel="noopener">Get directions</a>
    </p>
  </div>
  <iframe src="{mapsrc}" title="Map to Compufield {c['name']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</div>"""
    why = [
        ("Flexible timings", "choose weekday, weekend or fast-track batches"),
        ("Individual attention", "small batches and a computer for each student"),
        ("Free demo class", "try a real class before you join"),
        ("Google certification prep", "for Google Ads and Analytics"),
        ("Live projects", "for real brands, for your portfolio"),
        ("Experienced trainers", "teaching since 1985"),
    ]
    whyl = "".join(f"<li><b>{a}</b>: {b}</li>" for a, b in why)
    body = f"""
{breadcrumb([("Digital marketing", HUB), ("Centres", None)])}
<section class="course-hero">
  <div class="wrap">
    <div>
      <h1>Digital marketing institute at Bandra West and Kemps Corner, Mumbai, or learn online</h1>
      <p class="lede">Two classroom centres in Mumbai, and live online classes for students anywhere. The fastest way to reach us is WhatsApp.</p>
      <div class="btn-row">
        <a class="btn btn--wa" href="{wa('Hi Compufield, I would like to book a free demo class for digital marketing.')}">{WA_ICON}WhatsApp {C.WHATSAPP_SHOW}</a>
        <a class="btn btn--ghost" href="mailto:{C.EMAIL_SHOW}">Email {C.EMAIL_SHOW}</a>
      </div>
      <h2 class="mt-l" style="font-size:1.4rem">Why students choose Compufield</h2>
      <ul class="ticks">{whyl}</ul>
    </div>
    {demo_form(C.COURSE_OPTIONS[0])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="centres">{cards}</div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="section-head"><h2>Prefer to learn from home?</h2><p>Every course runs as live online classes, with the same trainer, syllabus, projects and certificate as the classroom. Students join from across India and abroad.</p></div>
    <a class="btn btn--wa" href="{wa('Hi Compufield, please share the online batch timings for digital marketing.')}">{WA_ICON}Ask for online batch timings</a>
  </div>
</section>
"""
    write(CONTACT, head(title, desc, CONTACT, [org_schema()]) + header(CONTACT) + body + footer())


def page_reviews():
    title = "Digital Marketing Student Reviews, Google Certificates & Classroom Photos | Compufield"
    desc = f"See what Compufield digital marketing students say: rated {C.RATING} from {C.REVIEWS} Google reviews. Video reviews, Google Ads certificates earned by students, and classroom photos from Mumbai."
    body = f"""
{breadcrumb([("Digital marketing", HUB), ("Reviews", None)])}
<section class="course-hero">
  <div class="wrap">
    <div>
      <h1>Digital marketing Google certification training: reviews, certificates and photos</h1>
      <p class="lede">Rated {C.RATING} from {C.REVIEWS} reviews on Google. Here is what our digital marketing students say, the Google certificates they've earned, and what our classes look like.</p>
    </div>
    {demo_form(C.COURSE_OPTIONS[0])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Student reviews</h2></div>
    {quotes_block()}
  </div>
</section>

<section class="section section--white" id="videos">
  <div class="wrap">
    <div class="section-head"><h2>Video reviews</h2><p>Hear it from our students.</p></div>
    {videos_block(C.VIDEOS)}
  </div>
</section>

<section class="section" id="certificates">
  <div class="wrap">
    <div class="section-head"><h2>Get Google Ads certification at Compufield Mumbai</h2><p>Certificates earned by our students. We prepare every student for Google's free Skillshop certifications.</p></div>
    {gallery_block(C.CERT_IMAGES, certs=True)}
  </div>
</section>

<section class="section section--white" id="batch-images">
  <div class="wrap">
    <div class="section-head"><h2>Digital marketing training images</h2></div>
    {gallery_block(C.CLASS_IMAGES)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Where our students work</h2></div>
    {logos_block()}
  </div>
</section>

{cta("See it for yourself", "Book a free demo class at Kemps Corner, Bandra West or online.")}
"""
    write(REVIEWS, head(title, desc, REVIEWS, [org_schema()]) + header(REVIEWS) + body + footer())


def page_thanks():
    title = "Thank you: your free demo class request is in | Compufield"
    desc = "Thank you for booking a free demo class with Compufield."
    body = f"""
<section class="section section--white">
  <div class="wrap thanks">
    <div class="tick" aria-hidden="true"></div>
    <h1>Thank you. Your demo class request is in.</h1>
    <p class="lede">Our team will call you to fix a time at Kemps Corner, Bandra West or online.</p>
    <p>Want an answer sooner? Message us on WhatsApp and we'll reply right away.</p>
    <p class="btn-row">
      <a class="btn btn--wa" href="{wa('Hi Compufield, I just booked a free demo class on your website.')}">{WA_ICON}WhatsApp {C.WHATSAPP_SHOW}</a>
      <a class="btn btn--ghost" href="{HUB}#syllabus">Browse the syllabus</a>
    </p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2>While you wait</h2>
    {related("")}
  </div>
</section>
"""
    # header without the demo jump-link target is fine: the nav button links to #demo on other pages
    hdr = header("").replace('href="#demo"', f'href="{HUB}#demo"')
    write(THANKS, head(title, desc, THANKS, noindex=True, lead=True) + hdr + body + footer())


def page_redirect(src, dst):
    target = dst.split("/")[-1] if not dst.startswith("..") else dst
    canonical = f"{C.SITE}/{dst.replace('../', '')}"
    html = f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<title>Moved: Compufield Digital Marketing</title>
<link rel="canonical" href="{canonical}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}" + location.hash);</script>
</head>
<body><p>This page has moved to <a href="{target}">{canonical}</a>.</p></body>
</html>
"""
    write(src, html)


def build():
    page_hub()
    for c in C.COURSES:
        page_course(c)
    page_fees()
    page_contact()
    page_reviews()
    page_thanks()
    for s, d in C.REDIRECTS.items():
        page_redirect(s, d)


if __name__ == "__main__":
    build()
