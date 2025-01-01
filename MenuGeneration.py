from playwright.sync_api import sync_playwright
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def send_email(content):
    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]
    receivers = os.environ["RECEIVER_EMAIL"].split(',')
    
    msg = MIMEText(content)
    msg['Subject'] = f'Weekly Menu - {datetime.now().strftime("%Y-%m-%d")}'
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        for receiver in receivers:
            server.send_message(msg)

def get_weekly_menu():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto('https://claude.ai/login')
        page.fill('input[type="email"]', os.environ["CLAUDE_EMAIL"])
        page.fill('input[type="password"]', os.environ["CLAUDE_PASSWORD"])
        page.click('button[type="submit"]')
        
        page.goto(f'https://claude.ai/chat/{os.environ["CHAT_ID"]}')
        page.fill('textarea[placeholder="Message Claude..."]', 
                 "Please create a new weekly menu using the same criteria as before but with different meals.")
        page.keyboard.press('Enter')
        
        page.wait_for_selector('.claude-response')
        menu = page.locator('.claude-response').last.inner_text()
        
        browser.close()
        return menu

if __name__ == "__main__":
    menu = get_weekly_menu()
    send_email(menu)
