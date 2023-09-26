from smtplib import SMTP
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import pandas as pd
from decouple import AutoConfig
import os

config = AutoConfig()



send_to = "data.csv"
template_path = os.path.join(os.getcwd(), "templates", "Template.html")
subject = "You're Invited to TEDxDWIT!"


def send_email():
    host = "smtp.gmail.com"
    port = 587

    from_mail = config("APP_EMAIL")

    email_content = ""

    with open(f"{template_path}", "r") as file:
        print(f"opening {template_path}")

        email_content = file.read()

        # print("email content is ",email_content)
        with SMTP(host, port, timeout=10) as smtp:
            smtp.starttls()
            print(
                f"trying to log in with {from_mail , config('APP_PASSWORD')} "
            )
            smtp.login(from_mail, config("APP_PASSWORD"))
            print("Successfully logged in !")

            df = pd.read_csv(f"{send_to}")
            print("reading csv")

            total = len(df.index)

            for index, row in df.iterrows():
                # replace text
                content = email_content.replace("{{name}}", row["name"].title())

                msg = MIMEMultipart()

                msgText = MIMEText(content, "html")
                msg.attach(msgText)
                image_path = os.path.join(os.getcwd(), "qr", f"{row['uuid']}.png")

                # attach image
                # with open(image_path, "rb") as image:
                #     img = MIMEImage(image.read())
                #     img.add_header(
                #         "Content-Disposition",
                #         "attachment",
                #         filename=f"{row['uuid']}.png",
                #     )
                #     msg.attach(img)

                # with open("event_schedule.pdf", "rb") as pdf:
                #     p = MIMEApplication(pdf.read())
                #     p.add_header(
                #         "Content-Disposition",
                #         "attachment",
                #         filename="event_schedule.pdf",
                #     )
                #     msg.attach(p)

                # with open("judging_criteria.pdf", "rb") as pdf:
                #     p = MIMEApplication(pdf.read())
                #     p.add_header('Content-Disposition', 'attachment', filename="judging_criteria.pdf")
                #     msg.attach(p)

                msg["Subject"] = subject

                msg["From"] = formataddr(("Software Club", from_mail))
                msg["To"] = formataddr((row["name"], row["email"]))

                try:
                    smtp.sendmail(from_mail, row["email"], msg.as_string())
                except smtplib.SMTPRecipientsRefused as email_problem_error:
                    print(f"[x] Email to {row['email']} not send ")
                    continue

                print(f"Mail sent to {row['email']}. ({index+1}/{total})")


def read_file():
    df = pd.read_csv("test.csv")
    for index, row in df.iterrows():
        print(row["Name"])


if __name__ == "__main__":
    # send_email()
    print("Hello World!")
    send_email()
    # print(config('EMAIL_ADDRESS'),config('EMAIL_PASSWORD'))
