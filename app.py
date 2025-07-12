from flask import Flask, request, redirect, render_template_string
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email config
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_SENDER = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'

def send_auto_reply(to_email, name):
    subject = "Thanks for contacting us!"
    body = f"""Hi {name},

Thanks for reaching out! We've received your message and will get back to you shortly.

Best regards,
Your Team"""

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Neon Contact Form</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: #0f0c29;
      height: 100vh;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      color: white;
      position: relative;
    }

    svg {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
    }

    .glow-path {
      stroke: url(#grad);
      stroke-width: 8;
      fill: none;
      filter: blur(1.5px);
      animation: pathMove 10s linear infinite;
    }

    @keyframes pathMove {
      0%   { stroke-dashoffset: 0; }
      100% { stroke-dashoffset: -1000; }
    }

    .form-container {
      position: relative;
      z-index: 1;
      background: rgba(255, 255, 255, 0.06);
      backdrop-filter: blur(20px);
      padding: 40px 30px;
      border-radius: 20px;
      box-shadow: 0 0 20px rgba(0,255,255,0.25);
      width: 90%;
      max-width: 400px;
    }

    .form-container h2 {
      margin-bottom: 25px;
      text-align: center;
    }

    input, textarea {
      width: 100%;
      margin-bottom: 15px;
      padding: 12px 15px;
      border-radius: 10px;
      border: none;
      background: rgba(255, 255, 255, 0.1);
      color: white;
      font-size: 16px;
    }

    input::placeholder, textarea::placeholder {
      color: #ccc;
    }

    button {
      width: 100%;
      padding: 12px;
      background: #00ffe1;
      border: none;
      border-radius: 10px;
      font-weight: bold;
      color: #000;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    button:hover {
      background: #00c4aa;
    }

    @media (max-width: 480px) {
      .form-container {
        padding: 30px 20px;
      }

      h2 {
        font-size: 22px;
      }
    }
  </style>
</head>
<body>

<svg>
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00ffe1"/>
      <stop offset="100%" stop-color="#ff00ff"/>
    </linearGradient>
  </defs>
  <path class="glow-path"
    d="M0 400 C 300 200, 600 600, 900 400 S 1500 200, 1800 400"
    stroke-dasharray="1000"
    stroke-dashoffset="0"
  />
</svg>

<div class="form-container">
  <h2>Contact Us</h2>
  <form method="POST">
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="email" name="email" placeholder="Your Email" required>
    <textarea name="message" rows="5" placeholder="Your Message" required></textarea>
    <button type="submit">Submit</button>
  </form>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        with open("contacts.csv", mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([name, email, message])

        try:
            send_auto_reply(email, name)
        except Exception as e:
            print("Email failed:", e)

        return redirect("/")
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
