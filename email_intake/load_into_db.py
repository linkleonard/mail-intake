#!/usr/bin/env python
from mailbox import mbox
from email.message import EmailMessage
from email_intake.config import env
from email_intake.models import (
    Message,
    Mailbox,
    Address,
    MessageHeader,
    MessageHeaderValue,
    MessagePayload,
)
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


folder = "/Users/leonard/Documents/output/"


def configure_logger():
    log_level = logging.DEBUG
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setFormatter(formatter)


def main():
    configure_logger()
    engine = create_engine(env('DATABASE_URL'))
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    mailbox = Mailbox()
    session.add(mailbox)

    for fname in os.listdir(folder):
        logger.debug("Parsing {}".format(fname))
        file_path = folder + fname
        file_mbox = mbox(file_path)

        message_count = 0
        # There should be messages in each file
        for message_count, email_message in enumerate(file_mbox, 1):
            sender = Address(
                uri=email_message['To']
            )
            session.add(sender)

            message = Message(
                mailbox=mailbox,
                sender=sender,
            )

            session.add(message)

            for name, value in email_message.items():
                header = MessageHeader(name=name)
                session.add(header)

                header_value = MessageHeaderValue(header=header, value=value)
                session.add(header_value)


            message_payload = email_message.get_payload()
            for email_payload in message_payload:
                if isinstance(email_payload, str):
                    content = email_payload
                else:
                    content = email_payload.get_payload()

                message_payload = MessagePayload(
                    body=content,
                    message=message,
                )
                session.add(message_payload)
        logger.debug('Parsed {} messages'.format(message_count))

    logger.info("Finished parsing input files. Committing...")
    session.commit()
    transaction.commit()
    logger.info("Commit complete.")


if __name__ == '__main__':
    main()
