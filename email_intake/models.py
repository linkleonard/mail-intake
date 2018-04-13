from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    uri = Column(String)

    mailboxes = relationship('Mailbox', back_populates='owner')
    sent_messages = relationship('Message', back_populates='sender')
    received_messages = relationship('Message', back_populates='recipients')


class Mailbox(Base):
    __tablename__ = 'mailbox'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('address.id'))

    owner = relationship('Address', back_populates='mailboxes')
    messages = relationship('Message', back_populates='mailbox')


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    mailbox_id = Column(Integer, ForeignKey('mailbox.id'))
    sender_id = Column(Integer, ForeignKey('address.id'))

    mailbox = relationship('Mailbox', back_populates='messages')
    sender = relationship('Address', back_populates='sent_messages')
    recipients = relationship(
        'Address',
        back_populates='received_messages',
        secondary="message_recipient",
    )
    header_values = relationship('MessageHeaderValue', back_populates='message')
    payloads = relationship('MessagePayload', back_populates='message')


class MessagePayload(Base):
    __tablename__ = 'message_payload'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('message.id'))
    body = Column(Text)

    message = relationship('Message', back_populates='payloads')


class MessageHeader(Base):
    __tablename__ = 'message_header'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    values = relationship('MessageHeaderValue', back_populates='header')


class MessageHeaderValue(Base):
    __tablename__ = 'message_header_value'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('message.id'))
    name_id = Column(Integer, ForeignKey('message_header.id'))
    value = Column(Text)

    header = relationship('MessageHeader', back_populates='values')
    message = relationship('Message', back_populates='header_values')


message_recipients = Table(
    'message_recipient', Base.metadata,
    Column('message_id', Integer, ForeignKey('message.id'), primary_key=True),
    Column('recipient_id', Integer, ForeignKey('address.id'), primary_key=True),
)
