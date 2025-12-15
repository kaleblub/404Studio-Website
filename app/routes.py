from flask import Blueprint, render_template, request, redirect, flash, url_for, make_response
from .utils import get_country_from_ip, get_user_lang
from urllib.parse import urlparse, urlunparse
from .forms import ContactForm
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

main = Blueprint('main', __name__)

load_dotenv()

ZOHO_EMAIL = os.getenv('ZOHO_EMAIL')
ZOHO_PASSWORD = os.getenv('ZOHO_PASSWORD')

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = ZOHO_EMAIL
    msg['To'] = ZOHO_EMAIL  # You can change this to another recipient if needed

    try:
        with smtplib.SMTP('smtp.zoho.com', 587) as server:
            server.starttls()
            server.login(ZOHO_EMAIL, ZOHO_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print("SMTP error:", e)
        return False

reviews = [
    {
        "review_content": "\"Excellent work. Hope to work with him again asap\"",
        "reviewer": "Client review",
        "reviewer_titlle": "(Upwork)"
    },
    {
        "review_content": "\"I have used Tina on Several Different occasions, and in each instance was very pleased. Her accounting skills are second to none, and she is well informed, If she is stumped with a question, she continues her research until she finds the right answer. She has helped me to find the right software, and has help me with implementing it. She is very trust worthy, and I would recommend her to anyone.\"",
        "reviewer": "Devi",
        "reviewer_title": "Manager at Chambers Construction",
    },
    {
        "review_content": "\"Tina keeps me organized and helps me not to stress about details of my business.\"",
        "reviewer": "Chad",
        "reviewer_title": "CEO at Carlson Audio",
    },
    {
        "review_content": "\"She is a remarkable person her personality, flexibility, her knowledge with accounting software and technology was very valuable to me.\"",
        "reviewer": "Alba",
        "reviewer_title": "Owner at Alba’s Trucking",
    },
    {
        "review_content": "\"Tina is a dedicated, organized, attentive, and creative accountant who is excellent at helping small businesses optimize their financial systems in order to maximize profits and organizational stability. She helped our business catch up on years of poorly managed records and was wonderfully accessible when we had questions. Tina is highly professional and fantastic to work with. She has our highest recommendation.\"",
        "reviewer": "Debby",
        "reviewer_title": "CEO at Curious Student Foundation",
    },
    {
        "review_content": "\"Tina was the best Bookkeeper my company has ever had. If she still lived nearby, she would still be my Bookkeeper. She is excellent at Training in the use of QuickBooks and she is very reliable. I can't recommend her enough for your Accounting needs for your business.\"",
        "reviewer": "Tim",
        "reviewer_title": "CEO of Ecomech",
    },
    {
        "review_content": "\"I highly recommend Tina! She is reliable, thorough, and someone who can be trusted implicitly. As the senior pastor at the Madison Campus Seventh-day Adventist Church, I greatly appreciated that she volunteered her bookkeeping skills to our non-profit community service center. This was a significant gift of her time as the center ran a thrift store and provided financial assistance to the community.\"",
        "reviewer": "Ken",
        "reviewer_title": "Pastor",
    }    
]

@main.route('/set-lang/<lang_code>')
def set_language(lang_code):
    if lang_code not in ['en', 'es']:
        lang_code = 'en'
    
    referrer = request.referrer or url_for('main.home', lang=lang_code)
    parsed_url = urlparse(referrer)

    # Split path and change the lang code
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) > 0 and path_parts[0] in ['en', 'es']:
        path_parts[0] = lang_code
    else:
        # If no lang in path, default to home in target lang
        path_parts.insert(0, lang_code)

    new_path = '/' + '/'.join(path_parts)

    # Reconstruct the URL with the new path
    new_url = urlunparse(parsed_url._replace(path=new_path))

    resp = make_response(redirect(new_url))
    resp.set_cookie('lang', lang_code, max_age=60*60*24*30, path='/')
    return resp


@main.route('/')
def root_redirect():
    lang = request.cookies.get('lang')
    if lang not in ['en', 'es']:
        lang = get_user_lang()
        response = make_response(redirect(url_for('main.home', lang=lang)))
        response.set_cookie('lang', lang, max_age=60*60*24*30, path='/')
        return response
    else:
        # If cookie valid, just redirect
        return redirect(url_for('main.home', lang=lang))


@main.route('/<lang>/', methods=['GET', 'POST'])
def home(lang):
    if lang not in ['en', 'es']:
        return redirect(url_for('main.home', lang='en'))

    cookie_lang = request.cookies.get('lang')
    if cookie_lang != lang:
        # Set cookie but render page immediately — no redirect!
        response = make_response(render_template('home.html', reviews=reviews, form=ContactForm()))
        response.set_cookie('lang', lang, max_age=60*60*24*30, path='/')
        return response

    # Now the cookie and URL lang are in sync — proceed with form etc.
    form = ContactForm()
    if form.validate_on_submit():
        subject = f"New message from {form.first_name.data} {form.last_name.data}"
        body = f"""
        Name: {form.first_name.data} {form.last_name.data}
        Email: {form.email.data}
        Company: {form.company.data}
        Business Type: {form.business_type.data}
        Service Interested In: {form.service.data}
        Subject: {form.subject.data}
        Message: {form.message.data}
        """

        if send_email(subject, body):
            flash('Message sent successfully!', 'success')
        else:
            flash('Error sending message. Please try again later.', 'danger')

        return redirect(url_for('main.home', lang=lang))

    return render_template('home.html', reviews=reviews, form=form)


@main.route('/<lang>/links')
def links_page(lang):
    if lang not in ['en', 'es']:
        return redirect(url_for('main.links_page', lang='en'))
    return render_template('links-page.html')


@main.route('/links', strict_slashes=False)
def links_redirect():
    lang = request.cookies.get('lang')
    if lang not in ['en', 'es']:
        lang = get_user_lang()
    print(f"Redirecting to: /{lang}/links")
    return redirect(url_for('main.links_page', lang=lang))



@main.route('/<lang>/about')
def about(lang):
    if lang not in ['en', 'es']:
        return redirect(url_for('main.about', lang='en'))
    return render_template('about.html', reviews=reviews)

@main.route('/<lang>/services')
def services(lang):
    if lang not in ['en', 'es']:
        return redirect(url_for('main.services', lang='en'))
    return render_template('services.html')

@main.route('/<lang>/contact', methods=['GET', 'POST'])
def contact(lang):
    if lang not in ['en', 'es']:
        return redirect(url_for('main.contact', lang='en'))
    
    form = ContactForm()
    if form.validate_on_submit():
        subject = f"New message from {form.first_name.data} {form.last_name.data}"
        body = f"""
        Name: {form.first_name.data} {form.last_name.data}
        Email: {form.email.data}
        Company: {form.company.data}
        Business Type: {form.business_type.data}
        Service Interested In: {form.service.data}
        Subject: {form.subject.data}
        Message: {form.message.data}
        """

        if send_email(subject, body):
            flash('Message sent successfully!', 'success')
        else:
            flash('Error sending message. Please try again later.', 'danger')

        return redirect(url_for('main.contact', lang=lang))

    return render_template('contact.html', form=form)

@main.route('/<lang>/pricing')
def pricing(lang):
    if lang not in ['en', 'es']:
        return redirect(url_for('main.pricing', lang='en'))
    return render_template('pricing.html')


projects = [
    {
        "id": "nationwide-legal",
        "title": "Nationwide Legal Directory",
        "description": "SEO-first, CMS-driven court information system built to scale across hundreds of U.S. jurisdictions.",
        "role": "Front-end architecture, SEO strategy, template system",
        "client_type": "Legal services company",
        "industry": "Legal / Information Directory",
        "features": [
            "CMS-driven court templates",
            "Structured data (JSON-LD)",
            "Mobile-first accessibility",
            "FAQ & breadcrumb schema",
            "Lighthouse 90+ scores"
        ],
        "seo_focus": True,
        "tech": [
            ("Next.js", "nextjs-icon-svgrepo-com.svg"),
            ("TailwindCSS", "tailwind-css.png"),
        ],
        "link": "https://state.1court.ai/",
        "desktop_mockup": "state-1court-ai-desktop-mockup.png",
        "mobile_mockup": "state-1court-ai-mobile-mockup.png",
        "testimonial": "Excellent work. Hope to work with him again asap."
    },
    {
        "id": "balanced-accountant",
        "title": "Balanced Accountant",
        "description": "Migrated from Squarespace to a modern custom design and built from scratch with Flask, HTML5, Tailwindcss, and JavaScript.",
        "role": "Front-end architecture, SEO strategy, Custom CMS",
        "client_type": "Accounting company",
        "industry": "Accounting",
        "features": [
            "CMS-driven information",
            "Structured data (JSON-LD)",
            "Mobile-first accessibility",
            "FAQ & breadcrumb schema",
            "Lighthouse 90+ scores"
        ],
        "seo_focus": True,
        "tech": [
            ("Flask", "flask.webp"),
            ("HTML5", "html-5-2.png"),
            ("TailwindCSS", "tailwind-css.png"),
        ],
        "link": "https://balancedaccountant.com/",
        "desktop_mockup": "balanced-accountant-home-page-mockup.png",
        "mobile_mockup": "balanced-accountant-home-page-mobile-mockup.png",
    },
    {
        "id": "woven-dignity",
        "title": "Woven Dignity",
        "description": "Woven Dignity is a non-profit organization specializing in handmade cards, with the main focus being to provide refugee women with hope and empowerment through sustainable work.",
        "tech": [
            ("Square Online", "Square_Jewel_White.svg"),
        ],
        "link": "https://wovendignity.com/",
        "desktop_mockup": "woven-dignity-home-page-mockup.png",
        "mobile_mockup": "woven-dignity-home-page-mobile-mockup.png",
    },
    {
        "id": "ilca-bejaia",
        "title": "ILCA Bejaia",
        "description": "ILCA Bejaia is an International Learning Center in Algeria offering language courses and learning resources.",
        "tech": [
            ("HTML5", "html-5-2.png"),
        ],
        "link": "https://ilca-website.vercel.app/",
        "desktop_mockup": "ilca-bejaia-home-page-mockup.png",
        "mobile_mockup": "woven-dignity-home-page-mobile-mockup.png",
    }
]

@main.route('/<lang>/portfolio')
def portfolio(lang):
    if lang not in ['en', 'es']:
        return redirect(url_for('main.portfolio', lang='en'))
    return render_template('portfolio.html', projects=projects)

@main.errorhandler(404)
def not_found(e):
    return redirect(url_for('main.index'))
