#!/usr/bin/env python
from email_intake import mbox
from email_intake.config import env
from email_intake.models import (
    Message,
    Mailbox,
    Address,
    MessageHeader,
    MessageHeaderValue,
)
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


folder = "/Users/leonard/Documents/output/"


def configure_logger():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

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
        with open(folder + fname) as fp:
            # Consume the From_ line
            # See: http://www.qmail.org/man/man5/mbox.html
            from_line = next(fp)
            logger.info(from_line)

            sender = Address()
            session.add(sender)

            message = Message(
                mailbox=mailbox,
                sender=sender,
            )

            session.add(message)

            header_lines = mbox.collect_headers(fp)
            grouped_header_lines = mbox.group_lines_as_headers(header_lines)
            for header_lines in grouped_header_lines:
                (name, value_iterator) = mbox.header_as_tuple(iter(header_lines))
                header = MessageHeader(name=name)
                session.add(header)

                value = '\n'.join(value_iterator)
                header_value = MessageHeaderValue(header=header, value=value)
                session.add(header_value)

    logger.info("Finished parsing input files. Committing...")
    session.commit()
    transaction.commit()
    logger.info("Commit complete.")


if __name__ == '__main__':
    main()
