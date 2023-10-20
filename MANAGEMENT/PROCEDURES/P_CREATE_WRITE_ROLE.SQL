CREATE OR REPLACE PROCEDURE ARQUITECTURA_DATOS.MANAGEMENT.P_MANAGE_WRITE_ROLE(
    DB_NAME VARCHAR(16777216), 
    DOMAIN_NAME VARCHAR(16777216), 
    CONTEXT_NAME VARCHAR(16777216)
)
RETURNS VARCHAR(16777216)
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS'

    var result = '''';

    try {
        var createRoleEnvironmentStmt = snowflake.createStatement({ sqlText: `create role if not exists R_${DOMAIN_NAME}_${CONTEXT_NAME}_W` });
        createRoleEnvironmentStmt.execute();

        var grantUsageDBStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON DATABASE ${DB_NAME} to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W` });
        grantUsageDBStmt.execute();

       //BRONZE RANK
        var grantUsageBronceStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_BRONZE to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W`});
        grantUsageBronceStmt.execute();

        var grantCRUDBronceStmt = snowflake.createStatement({ sqlText: `GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_BRONZE to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W` });
        grantCRUDBronceStmt.execute(); 

        var grantFutureCRUDFBronceStmt = snowflake.createStatement({ sqlText: `GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_BRONZE TO ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W`});
        grantFutureCRUDFBronceStmt.execute();

        //SILVER RANK
        var grantUsageSilverStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_SILVER to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W`});
        grantUsageSilverStmt.execute(); 

        var grantCRUDSilverStmt = snowflake.createStatement({ sqlText: `GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_SILVER to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W` });
        grantCRUDSilverStmt.execute(); 

        var grantFutureCRUDFSilverStmt = snowflake.createStatement({ sqlText: `GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_SILVER TO ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W`});
        grantFutureCRUDFSilverStmt.execute();

        //GOLD RANK
        var grantUsageGoldStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_GOLD to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W`});
        grantUsageGoldStmt.execute(); 

        var grantCRUDGoldStmt = snowflake.createStatement({ sqlText: `GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_GOLD to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W` });
        grantCRUDGoldStmt.execute(); 

        var grantFutureCRUDFGoldStmt = snowflake.createStatement({ sqlText: `GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_GOLD TO ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_W`});
        grantFutureCRUDFGoldStmt.execute();
        
        result = `Role R_${DOMAIN_NAME}_${CONTEXT_NAME}_W created and permissions granted successfully.`;

    } catch (err) {
        // Rollback transaction
        snowflake.execute({ sqlText: "ROLLBACK" });

        result =  "Failed: Code: " + err.code + "\\n  State: " + err.state;
        result += "\\n  Message: " + err.message;
        result += "\\nStack Trace:\\n" + err.stackTraceTxt;

        throw err; 
    }

    return result;

';
