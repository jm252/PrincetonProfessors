import os
import sys
import sqlalchemy
import sqlalchemy.orm
import dotenv
import database

# ----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

# ----------------------------------------------------------------------


def main():
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
