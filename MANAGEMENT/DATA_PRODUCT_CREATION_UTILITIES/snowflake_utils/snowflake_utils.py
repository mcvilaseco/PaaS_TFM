from snowflake.snowpark import Session
import snowflake.connector
import traceback
import os

def get_snowflake_session(user, password, account, role, warehouse):
    connection_parameters = {
        "user": user,
        "password": password,
        "account": account,
        "role": role,
        "warehouse": warehouse
    }

    session = Session.builder.configs(connection_parameters).create()
    return session

def general(session, file, res, dbname):
    session.use_database(dbname)

    try:
        # Read the SQL file and execute its content
        with open(file, 'r') as sql_file:
            sql_content = sql_file.read()
            
        print(sql_content)

        # Execute SQL file content
        df = session.sql(sql_content)

        # Return result if desired
        result = df.collect()

        if res:
            print("Resultado del Despliegue:")
            print(result)

    except Exception as e:
        print("Excepcion")
        print(str(e))
        traceback.print_exc()

def create_schema(session, sch_name, db_name):
    try:
        session.use_database(db_name)
        sqlQuery = "CREATE SCHEMA IF NOT EXISTS {name}".format(name=sch_name)
        
        return session.sql(sqlQuery).collect()

    except Exception as err:
        print("Failed to create the schema:")
        print("\nError Message:" + str(err))

# Shows column lineage
def showColumnLineage(session, database):
    try:
        # Execute column lineage query
        text_query = """
        select qh.query_text,
            trim(ifnull(src.value:objectName::string, '') || '.' || ifnull(src.value:columnName::string, ''), '.') as source,
            trim(ifnull(om.value:objectName::string, '') || '.' || ifnull(col.value:columnName::string, ''), '.') as target,
            ah.objects_modified
        from snowflake.account_usage.access_history ah
        left join snowflake.account_usage.query_history qh
        on ah.query_id = qh.query_id,
        lateral flatten(input => objects_modified) om,
        lateral flatten(input => om.value: "columns", outer => true) col,
        lateral flatten(input => col.value:directSources, outer => true) src
        where (ifnull(src.value:objectName::string, '') like '%{database}%'
            or ifnull(om.value:objectName::string, '') like '%{database}%')
        order by ah.query_start_time;
        """.format(database=database)

        result = session.sql(text_query).collect()
        print("\n=========== COLUMN LINEAGE - CONTAINING:" + database + "===========")
        for row in result:
            print(row)

    except Exception as err:
        print("Failed to retrieve the column lineage:")
        print("\nError Message:" + str(err))

# Creates a new database whit a default schema given a name TODO ROLLBACK
def create_database(session, name):
    try:
        # Execute the create database query
        session.sql("create database if not exists " + name).collect()

        # Create default schemas
        create_schema(session, "MANAGEMENT", name)
        create_schema(session, "LANDING_DATA_BRONZE", name)
        create_schema(session, "LANDING_DATA_SILVER", name)
        create_schema(session, "LANDING_DATA_GOLD", name)

        #Create roles procedures
        script_directory = os.path.dirname(os.path.abspath(__file__))
        sql_file1 = os.path.join(script_directory, "../../PROCEDURES/P_MANAGE_READ_ROLE.SQL")
        sql_file2 = os.path.join(script_directory, "../../PROCEDURES/P_CREATE_WRITE_ROLE.SQL")
        general(session, sql_file1, False, name)
        general(session, sql_file2, False, name)

        #Call roles procedures
        session.call("ARQUITECTURA_DATOS.MANAGEMENT.P_MANAGE_READ_ROLE", name, "LANDING", "LANDING")
        session.call("ARQUITECTURA_DATOS.MANAGEMENT.P_MANAGE_WRITE_ROLE", name, "LANDING", "LANDING")

    except Exception as err:
        print("Failed to create database:")
        print("\nError Message:" + str(err))
