import snowflake_utils.snowflake_utils as su
import os 
import click
import logging,sys
import traceback

def get_logger(logger_name, logging_level):
    format = '%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)5s'
    logging.basicConfig(stream=sys.stdout, level=logging_level, format=format, datefmt='%m/%d/%Y %I:%M:%S')
    logger = logging.getLogger(logger_name)
    return logger

logger = get_logger('main', logging.INFO)


def get_params():
    user = os.getenv('SNOWFLAKE_USER')
    assert user is not None, "SNOWFLAKE_USER environment variable not set"
    password= os.getenv('SNOWFLAKE_PWD')
    assert password is not None, "SNOWFLAKE_PWD environment variable not set"
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    assert account is not None, "SNOWFLAKE_ACCOUNT environment variable not set"
    role = os.getenv('SNOWFLAKE_ROLE')
    assert role is not None, "SNOWFLAKE_ROLE environment variable not set"
    warehouse = os.getenv('SNOWFLAKE_WH')
    assert warehouse is not None, "SNOWFLAKE_WH environment variable not set"
    return user, password,account,role, warehouse


@click.command()
@click.option(
    '--name', 
    '-n',
    required=True,
    help = "database name"
)

def main(name):
    # Get snowflake execution parameters
    user, password, account, role, warehouse = get_params()

    # Get connections
    session = su.get_snowflake_session(user, password, account, role, warehouse)
    if session is None:
        logger.error('Execution finished with an Snowflake connection error -> unable to stablish the connection')
        sys.exit(1)

    logger.info(f'You have succesfully logged in')
    
    su.create_database(session, name)

if __name__ == "__main__":
    main()

