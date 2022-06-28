"""
    Description:

    Envio de E-mails

    Author:           @Palin
    Created:          2021-04-26
    Copyright:        (c) Ampere Consultoria Ltda
"""
import os
import sys

try:
    import smtplib
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    from dynaconf import Dynaconf

    settings = Dynaconf(
        envvar_prefix="AMPERE",
        settings_files=["settings.toml", ".secrets.toml"],
        environments=True,
        load_dotenv=True,
    )
except ImportError as error:
    print(error)
    print(f"error.name: {error.name}")
    print(f"error.path: {error.path}")


def send_email(
    MSG_TO: str, MSG_TITULO: str, HTML_BODY_MSG: str, PATH_FILE_ANEXO: str = None
):
    """Dispara e-mail utilizando SMTPLIB

    Args:
        MSG_TO (str): e-mail do destinatário
        MSG_TITULO (str): Título da Mensagem
        HTML_BODY_MSG (str): Corpo da Mensagem em Html
        PATH_FILE_ANEXO (str): string com o caminho completo
        e nome do arquivo anexo.
    """

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_MSG_FROM
    msg["To"] = MSG_TO
    msg["Subject"] = MSG_TITULO

    # ANEXA HTML DO CORPO DO EMAIL
    part1 = MIMEText(HTML_BODY_MSG, "html")
    msg.attach(part1)
    if PATH_FILE_ANEXO:
        part2 = MIMEBase("application", "octet-stream")
        try:
            with open(PATH_FILE_ANEXO, "rb") as fp:
                part2.set_payload(fp.read())
            encoders.encode_base64(part2)
            part2.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(PATH_FILE_ANEXO),
            )
            msg.attach(part2)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    mailServer = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    mailServer.sendmail(settings.SMTP_MSG_FROM, MSG_TO, msg.as_string())
    mailServer.close()


def send_email_plain_text(MSG_TO: str, MSG_TITULO: str, STR_MSG_CONTEUDO: str):
    """Dispara e-mail utilizando SMTPLIB

    Args:
        MSG_TO (str): e-mail do destinatário
        MSG_TITULO (str): Título da Mensagem
        STR_MSG_CONTEUDO (str): Corpo da Mensagem em TXT
    """

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_MSG_FROM
    msg["To"] = MSG_TO
    msg["Subject"] = MSG_TITULO

    # ANEXA HTML DO CORPO DO EMAIL
    part1 = MIMEText(STR_MSG_CONTEUDO, "plain")
    msg.attach(part1)
    mailServer = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    mailServer.sendmail(settings.SMTP_MSG_FROM, MSG_TO, msg.as_string())
    mailServer.close()
