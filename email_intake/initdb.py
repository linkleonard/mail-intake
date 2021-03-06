#!/usr/bin/env python
from email_intake import config, models
from sqlalchemy import create_engine


def main():
    engine = create_engine(config.env('DATABASE_URL'))
    models.Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()
