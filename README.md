# Neon Contact Form

A simple Flask web app featuring a neon animated SVG background contact form.  
Submissions are saved to a CSV file, and users receive an automatic email reply via Gmail SMTP.

---

## Features

- Responsive neon animated background using SVG and CSS  
- Contact form with name, email, and message fields  
- Saves submissions to `contacts.csv`  
- Sends an automatic email confirmation to users  
- Simple, clean UI that works well on mobile devices

---

### Open the Python script and update these variables with your Gmail account details:

- SMTP_SERVER = 'smtp.gmail.com'
- SMTP_PORT = 587
- EMAIL_SENDER = 'your_email@gmail.com'
- EMAIL_PASSWORD = 'your_app_password'  # Use Google App Password if 2FA enabled
