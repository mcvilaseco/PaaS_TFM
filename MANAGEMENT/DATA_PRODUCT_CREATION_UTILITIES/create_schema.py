import snowflake_utils.snowflake_utils as suuu
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
    '-sch', '--schema_name', 'sch_name',
    required=True,
    help = "schema name"
)
@click.option(
    '-db', '--data_base_name', 'db_name',
    required=True,
    help = "data base name"
)
def main(sch_name, db_name):
    user, password, account, role, warehouse = get_params()
    session = suuu.get_snowflake_session(user, password, account, role, warehouse)
    if session is None:
        logger.error('Execution finished with an Snowflake connection error -> unable to stablish the connection')
        sys.exit(1)
    logger.info('You have logged in')
    
    try:
        collect = suuu.create_schema(session, sch_name, db_name)
    except Exception as e:
        logger.error(str(e))
    else:
        logger.info(collect)

if __name__ == "__main__":
    main()