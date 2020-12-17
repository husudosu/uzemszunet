import ssl
import smtplib
import enum
import logging
import os
from collections import namedtuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEBase
from email import encoders

from uzemszunet.jinjaext import jinja_env

logger = logging.getLogger('uzemszunet')


class EmailTipus(enum.IntEnum):
    EGYSZERU_LISTA = 1
    RENDEZETT_LISTA = 2
    HEARTBEAT = 3


def create_email(uzemszunetek, email_tipus, have_error):
    """
    Létrehozza az E-mail-nek a HTML-jét
    :param uzemszunetek: Üzemszünetek listája
    :param email_tipus: Email típusa, amely alapján generálva lesz a HTML
    :param have_error: Ha történt hiba.
    """
    template = None
    if email_tipus == EmailTipus.EGYSZERU_LISTA:
        template = jinja_env.get_template('egyszeru_lista.jinja')
    elif email_tipus == EmailTipus.RENDEZETT_LISTA:
        template = jinja_env.get_template('rendezett_lista.jinja')
    elif email_tipus == EmailTipus.HEARTBEAT:
        template = jinja_env.get_template('heartbeat.jinja')
        return template.render(have_error=have_error)
    else:
        raise Exception("Nem megfelelő E-mail típust kaptam!")

    return template.render(
        uzemszunetek=uzemszunetek,
        have_error=have_error
    )


def send_email(
    text,
    subject,
    email_config,
    attachments=[]
):
    """
    Email elküldése.
    :param text: E-mail üzenet tartalma (HTML)
    :param subject: Üzenet tárgya.
    :param email_config: Dict ami tartalmazza a kongigurációt
    email_config = {
        'to_mail': 'cimzett@gmail.com',
        'smtp_host': 'smtp.gmail.com',
        'smtp_port': 465,
        'user': 'felhasznalo@gmail.com',
        'password': 'jelszo'
    }
    :param attachments: Csatolt fájlok listája.
    """
    try:
        message = MIMEMultipart("alternative")

        smtp_host = email_config["smtp_host"]
        smtp_port = email_config.get("smtp_port", 465)
        to_mail = email_config["to_mail"]
        user = email_config["user"]
        password = email_config["password"]

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(text, "html")

        message.attach(part1)
        message.attach(part2)

        message["Subject"] = subject
        message["From"] = user
        message["TO"] = to_mail

        # Fájl csatolmányok
        # TODO: Lekezelni ha fájl nem létezik/None
        for attachment in attachments:
            path, filename = os.path.split(attachment)

            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment, "rb").read())
            encoders.encode_base64(part)

            part.add_header(
                'Content-Disposition',
                'attachment; filename="{0}"'.format(filename)
            )
            message.attach(part)

        # Kapcsolat létrehozása.
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(user, password)
            server.sendmail(
                user, to_mail, message.as_string()
            )
    except Exception as e:
        logger.exception("Hiba történt az E-mail küldése közben:")


def handle_email(
    results,
    email_tipus,
    have_error,
    email_config,
    logfile
):
    html = create_email(results, email_tipus, have_error)

    if have_error:
        send_email(
            html,
            'Üzemszünetek Hiba',
            email_config,
            [logfile]
        )
    else:
        send_email(
            html,
            'Üzemszünetek',
            email_config
        )
