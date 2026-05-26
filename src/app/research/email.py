import smtplib
from email.message import EmailMessage
from app.config.settings import Settings

def send_email_with_attachment(query: str, file_path: str, settings: Settings):
    msg = EmailMessage()
    msg["Subject"] = f"AI Research Report – {query}"
    msg["From"] = settings.from_email
    msg["To"] = settings.to_email

    body = f"""Hello,

    Please find attached the research report titled
    “{query}.”

    The report provides an evidence-based analysis of the topic, highlighting
    key findings, relevant context, and practical implications.

    If you have any questions or would like a deeper analysis on a specific area,
    feel free to reach out.

    Best regards,
    Ankit
    """
    msg.set_content(body)

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="report.pdf"
        )

    with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as s:
        s.starttls()
        s.login(settings.from_email, settings.email_pwd)
        s.send_message(msg)