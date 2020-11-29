import smtplib
import ssl
import sys
import os
from pathlib import Path
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_config_path():
    platform = sys.platform
    if platform == 'win32':
        return os.path.join(
            os.getenv('APPDATA'), 'uzemszunet', 'uzemszunet.cfg'
        )
    else:
        # Unix alapú rendszereken talán ezt meg fogja enni (Linuxon tuti megy)
        # TODO ^ Kivizsgálni
        return os.path.join(
            Path.home(), '.config', 'uzemszunet', 'uzemszunet.cfg'
        )


def format_email(uzemszunetek):
    """
    Megformázza az E-mail-t küldés előtt.
    """
    email_html = "Várható üzemszünetek:<br />"

    for datum in uzemszunetek.items():
        email_html += "<h3>{}</h3>".format(datum[0][0:10])
        for telepules in datum[1].items():
            email_html += "<h4>{}</h4>".format(telepules[0])

            email_html += "<ul>"
            for helyszin in telepules[1]:
                email_html += "<li><b>{0};</b> {1}-{2}; {3}-{4}; {5}</li>".format(
                    helyszin.get("utca"),
                    helyszin.get("hazszam_tol"),
                    helyszin.get("hazszam_ig"),
                    helyszin.get("idopont_tol"),
                    helyszin.get("idopont_ig"),
                    helyszin.get("megjegyzes")
                )
            email_html += "</ul> <br />"
        return email_html


def send_email(
    text,
    smtp_host,
    user, password,
    to_mail,
    subject,
    smtp_port=465
):
    """
    Email elküldése.
    """
    try:
        message = MIMEMultipart("alternative")

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(text, "html")

        message.attach(part1)
        message.attach(part2)

        message["Subject"] = subject
        message["From"] = user
        message["TO"] = to_mail

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(user, password)
            server.sendmail(
                user, to_mail, message.as_string()
            )
    except Exception as e:
        print(e)
