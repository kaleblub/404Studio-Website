from flask import Blueprint, render_template, request, redirect, flash, url_for
import smtplib
from email.message import EmailMessage
import time
from dotenv import load_dotenv
import os


load_dotenv()

ZOHO_EMAIL = os.getenv('ZOHO_EMAIL')
ZOHO_PASSWORD = os.getenv('ZOHO_PASSWORD')



main = Blueprint('main', __name__)

reviews = [
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

@main.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Honeypot field (bot filter)
            if request.form.get('company_code'):
                # Silently redirect bots
                return redirect(url_for('main.home'))

            # Time-based spam protection
            try:
                form_loaded_at = int(request.form.get('form_loaded_at', 0))
                time_elapsed = time.time() - form_loaded_at
                if time_elapsed < 3:
                    return redirect(url_for('main.home'))  # too fast = suspicious
            except (ValueError, TypeError):
                return redirect(url_for('main.home'))  # invalid or missing timestamp

            # Extract form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            company = request.form.get('company', '')
            business_type = request.form.get('business_type', '')
            subject = request.form.get('subject')
            service = request.form.get('service', 'Other')
            message = request.form.get('message')

            # Compose email
            email_message = EmailMessage()
            email_message['Subject'] = f"Contact Form Submission: {subject}"
            email_message['From'] = ZOHO_EMAIL
            email_message['To'] = ZOHO_EMAIL

            email_message.set_content(f"""
            New Contact Submission:

            Name: {first_name} {last_name}
            Email: {email}
            Company: {company}
            Business Type: {business_type}
            Service Interested: {service}
            Subject: {subject}

            Message:
            {message}
            """)

            # Send email via Zoho SMTP
            with smtplib.SMTP_SSL('smtp.zoho.com', 465) as smtp:
                smtp.login(ZOHO_EMAIL, ZOHO_PASSWORD)
                smtp.send_message(email_message)

            flash('Message sent successfully!', 'success')

        except Exception as e:
            print("Email sending failed:", e)
            flash('Failed to send message. Please try again later.', 'danger')

        return redirect(url_for('main.home'))

    return render_template('home.html', reviews=reviews, form_loaded_at=int(time.time()))


@main.route('/links')
def links_page():
    return render_template('links-page.html')

@main.route('/about')
def about():
    return render_template('about.html', reviews=reviews)

all_services = {
    'accounting': {
        'image': 'static/images/services-accounting-image.jpg',  # Replace with actual image paths
        'title': 'Accounting & Financial Statements',
        'content': [
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>', 'We help you create financial statements and reports tailored to your business. Tracking financial trends monthly helps you make informed decisions for the future.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>', 'We guide you in analyzing assets and liabilities to improve financial health and optimize business operations.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.293a1 1 0 01.707.293l.707.707a1 1 0 001.414 0l.707-.707A1 1 0 0111.707 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path></svg>','We help develop and monitor budgets to keep expenses low and maximize profitability.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>','From data collection to tax reporting, we streamline the process, making tax season stress-free and efficient.')
            ],
    },
    'payroll': {
        'image': 'static/images/services-payroll-image.jpg',  # Replace with actual image paths
        'title': 'Payroll Management',
        'content': [
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>', 'We help you set up payroll systems and manage employee work hours efficiently.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>', 'We assist in choosing and configuring the best payroll software for your business needs.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.293a1 1 0 01.707.293l.707.707a1 1 0 001.414 0l.707-.707A1 1 0 0111.707 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path></svg>','We create paychecks, set up direct deposits, and ensure employees are paid on time.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>','We file payroll tax forms and handle tax payments to keep your business compliant.')
            ],
    },
    'software': {
        'image': 'static/images/services-software-training-image.jpg',  # Replace with actual image
        'title': 'Software Training & Setup',
        'content': [
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>', 'We provide hands-on training so you can confidently manage your financial records. Want to manage your own books?'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.128m-1.457 1.281a2.25 2.25 0 02.25-2.25A2.25 2.25 0 0110.743 16.05c.463-.885.723-1.976.723-3.128zm-11.48 2.1c.36-.566.781-1.033 1.258-1.39l4.808-3.202a1.25 1.25 0 011.562 2.08l-4.807 3.202c-.477.318-.898.776-1.258 1.39z"></path></svg>', 'Learn Accounting Terminology. Understand financial concepts in simple terms.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.128m-1.457 1.281a2.25 2.25 0 02.25-2.25A2.25 2.25 0 0110.743 16.05c.463-.885.723-1.976.723-3.128zm-11.48 2.1c.36-.566.781-1.033 1.258-1.39l4.808-3.202a1.25 1.25 0 011.562 2.08l-4.807 3.202c-.477.318-.898.776-1.258 1.39z"></path></svg>', 'Compare Software Options. We help you choose the best accounting software for your needs.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.128m-1.457 1.281a2.25 2.25 0 02.25-2.25A2.25 2.25 0 0110.743 16.05c.463-.885.723-1.976.723-3.128zm-11.48 2.1c.36-.566.781-1.033 1.258-1.39l4.808-3.202a1.25 1.25 0 011.562 2.08l-4.807 3.202c-.477.318-.898.776-1.258 1.39z"></path></svg>', 'Certified Quickbooks & Xero Experts. As ProAdvisors, we provide in-depth training tailored to your business.')
        ],
    },
    'bookkeeping': {
        'image': 'static/images/services-bookkeeping-image.jpg',  # Replace with actual image
        'title': 'Bookkeeping & Record Keeping',
        'content': [
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>', 'One-Time Assistance. Software Training - We train you on Quickbooks, Xero, and other software so you can manage finances confidently. Record Review - Need help correcting transactions? We review your records and ensure accuracy. General Ledger Cleanup - Get your books in order for better financial tracking. Software Setup - We configure your accounting software for easy and efficient use.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.128m-1.457 1.281a2.25 2.25 0 02.25-2.25A2.25 2.25 0 0110.743 16.05c.463-.885.723-1.976.723-3.128zm-11.48 2.1c.36-.566.781-1.033 1.258-1.39l4.808-3.202a1.25 1.25 0 011.562 2.08l-4.807 3.202c-.477.318-.898.776-1.258 1.39z"></path></svg>', 'Daily Assistance. Transaction Data Entry - We record all checks, deposits, and credit card transactions. Accounts Receivable - We manage invoicing, payments, and deposits. Accounts Payable - We track and process your business expenses.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.128m-1.457 1.281a2.25 2.25 0 02.25-2.25A2.25 0 0110.743 16.05c.463-.885.723-1.976.723-3.128zm-11.48 2.1c.36-.566.781-1.033 1.258-1.39l4.808-3.202a1.25 1.25 0 011.562 2.08l-4.807 3.202c-.477.318-.898.776-1.258 1.39z"></path></svg>', 'Monthly Assistance. Record Review & Reconciliation - We review your general ledger, reconcile accounts, and generate management reports.'),
            ('<svg class="w-8 h-8 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.128m-1.457 1.281a2.25 2.25 0 02.25-2.25A2.25 0 0110.743 16.05c.463-.885.723-1.976.723-3.128zm-11.48 2.1c.36-.566.781-1.033 1.258-1.39l4.808-3.202a1.25 1.25 0 011.562 2.08l-4.807 3.202c-.477.318-.898.776-1.258 1.39z"></path></svg>', 'Yearly Assistance. Catch-Up Bookkeeping - Need help preparing records for tax filing? We\'ll get everything in order. Financial Review - Before handing records to your CPA, we ensure everything is in check.')
        ],
    },
}

@main.route('/services')
def services():
    selected_tab = request.args.get('tab', 'accounting')
    return render_template('services.html', all_services=all_services, selected_tab=selected_tab)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Honeypot field (bot filter)
            if request.form.get('company_code'):
                # Silently redirect bots
                return redirect(url_for('main.home'))

            # Time-based spam protection
            try:
                form_loaded_at = int(request.form.get('form_loaded_at', 0))
                time_elapsed = time.time() - form_loaded_at
                if time_elapsed < 3:
                    return redirect(url_for('main.home'))  # too fast = suspicious
            except (ValueError, TypeError):
                return redirect(url_for('main.home'))  # invalid or missing timestamp

            # Extract form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            company = request.form.get('company', '')
            business_type = request.form.get('business_type', '')
            subject = request.form.get('subject')
            service = request.form.get('service', 'Other')
            message = request.form.get('message')

            # Compose email
            email_message = EmailMessage()
            email_message['Subject'] = f"Contact Form Submission: {subject}"
            email_message['From'] = ZOHO_EMAIL
            email_message['To'] = ZOHO_EMAIL

            email_message.set_content(f"""
            New Contact Submission:

            Name: {first_name} {last_name}
            Email: {email}
            Company: {company}
            Business Type: {business_type}
            Service Interested: {service}
            Subject: {subject}

            Message:
            {message}
            """)

            # Send email via Zoho SMTP
            with smtplib.SMTP_SSL('smtp.zoho.com', 465) as smtp:
                smtp.login(ZOHO_EMAIL, ZOHO_PASSWORD)
                smtp.send_message(email_message)

            flash('Message sent successfully!', 'success')
        
        except Exception as e:
            print("Email sending failed:", e)
            flash('Failed to send message. Please try again later.', 'danger')

        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form_loaded_at=int(time.time()))

@main.route('/pricing')
def pricing():
    return render_template('pricing.html')

@main.route('/blog')
def blog():
    return render_template('blog.html')

@main.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')




# Pricing Calculation Logic
# def calculate_price(data):
#     return {"package": "Custom Quote", "price": round(estimated_savings, 2)}

# @main.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.json
#     result = calculate_price(data)
#     return jsonify(result)