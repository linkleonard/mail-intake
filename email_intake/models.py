from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    uri = Column(String)


class Mailbox(Base):
    __tablename__ = 'mailbox'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('address.id'))

    owner = relationship('Address', back_populates='mailboxes')


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    mailbox_id = Column(Integer, ForeignKey('mailbox.id'))
    sender_id = Column(Integer, ForeignKey('address.id'))

    mailbox = relationship('Mailbox', back_populates='messages')
    sender = relationship('Address', back_populates='sent_messages')
    recipients = relationship('Address', back_populates='received_messages', secondary="message_recipients")


class MessageHeader(Base):
    __tablename__ = 'message_header'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('message.id'))

    message = relationship('Message', back_populates='headers')


message_recipients = Table(
    'message_recipient', Base.metadata,
    Column('message_id', Integer, ForeignKey('message.id'), primary_key=True),
    Column('recipient_id', Integer, ForeignKey('address.id'), primary_key=True),
)
