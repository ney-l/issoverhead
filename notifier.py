import smtplib


def send_email(email, password, recipient):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(
            from_addr=email,
            to_addrs=recipient,
            msg="Subject:Look up! It's ISS!\n\nInternational Space Station is flying over you right now! Look up!"
        )
