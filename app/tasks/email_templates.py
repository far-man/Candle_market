from email.message import EmailMessage
from pydantic import EmailStr

from app.config import settings


def create_basket_confirmation_template(
        basket: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение покупки"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Подтвердите покупку</h1>
        Вы приобретаете продукцию на сумму {basket["total_cost"]}
""",
        subtype="html"
    )
    return email
