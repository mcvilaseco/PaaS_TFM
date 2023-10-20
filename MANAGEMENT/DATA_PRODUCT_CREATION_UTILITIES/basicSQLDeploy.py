import snowflake_utils.snowflake_utils as su
from snowflake_utils.snowflake_utils import get_snowflake_session
import os 
import click
import logging
import sys

def get_logger(logger_name, logging_level):
    format = '%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)5s'
    logging.basicConfig(stream=sys.stdout, level=logging_level, format=format, datefmt='%m/%d/%Y %I:%M:%S')
    logger = logging.getLogger(logger_name)
    return logger

logger = get_logger('main', logging.INFO)

def get_params():
    user = os.getenv(f'SNOWFLAKE_USER')
    assert user is not None, f"SNOWFLAKE_USER environment variable not set"
    password = os.getenv(f'SNOWFLAKE_PWD')
    assert password is not None, f"SNOWFLAKE_PWD environment variable not set"
    account = os.getenv(f'SNOWFLAKE_ACCOUNT')
    assert account is not None, f"SNOWFLAKE_ACCOUNT environment variable not set"
    role = os.getenv(f'SNOWFLAKE_ROLE')
    assert role is not None, f"SNOWFLAKE_ROLE environment variable not set"
    warehouse = os.getenv(f'SNOWFLAKE_WH')
    assert warehouse is not None, f"SNOWFLAKE_WH environment variable not set"
    return user, password, account, role, warehouse

@click.command()
@click.option(
    '--file', 
    '-f',
    required=True,
    type=click.Path(exists=True),
    help="File to run"
)

@click.option(
    '--res',
    is_flag=True,
    default=False,
    help="resultados despliegue"
)


def main(file, res):
    # Get snowflake execution parameters
    user, password, account, role, warehouse = get_params()

    # Get connections
    session = su.get_snowflake_session(user, password, account, role, warehouse)
    if session is None:
        logger.error('Execution finished with a Snowflake connection error -> unable to establish the connection')
        sys.exit(1)

    logger.info(f'You have succesfully logged in')

    # Execute SQL
    su.general(session, file, res)
    
if __name__ == "__main__":
    main()