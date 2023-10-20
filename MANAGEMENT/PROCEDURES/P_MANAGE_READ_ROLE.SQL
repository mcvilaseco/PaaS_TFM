CREATE OR REPLACE PROCEDURE ARQUITECTURA_DATOS.MANAGEMENT.P_MANAGE_READ_ROLE(DB_NAME VARCHAR(16777216), DOMAIN_NAME VARCHAR(16777216) , CONTEXT_NAME VARCHAR(16777216) )
RETURNS VARCHAR(16777216)
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS '

        var result = '''';
        
        try {
            var createRoleEnvironmentStmt = snowflake.createStatement({ sqlText: `create role if not exists R_${DOMAIN_NAME}_${CONTEXT_NAME}_R` });
            var crRs = createRoleEnvironmentStmt.execute();

            var  createRoleEnvironmentStmt = snowflake.createStatement({ sqlText: `create role if not exists R_${DOMAIN_NAME}_${CONTEXT_NAME}_W` });
            var crRs = createRoleEnvironmentStmt.execute();

            var grantUsageDBStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON DATABASE ${DB_NAME} to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_R` });
            var crRs = grantUsageDBStmt.execute();

            var grantUsageSCHEMASStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_BRONZE to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_R` });
            var crRs = grantUsageSCHEMASStmt.execute();
            grantUsageSCHEMASStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_SILVER to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_R` });
            crRs = grantUsageSCHEMASStmt.execute();
            grantUsageSCHEMASStmt = snowflake.createStatement({ sqlText: `GRANT USAGE ON SCHEMA ${DB_NAME}.${DOMAIN_NAME}_DATA_GOLD to ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_R` });                    
            crRs = grantUsageSCHEMASStmt.execute();
            var gSystStmt = snowflake.createStatement({ sqlText: `GRANT ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_R to ROLE SYSADMIN` });
            var crRs = gSystStmt.execute();
            
            var selectEnvironmentStmt = snowflake.createStatement({ sqlText: `show grants to role R_${DOMAIN_NAME}_${CONTEXT_NAME}_W` });
            var selectEnvironmentRs = selectEnvironmentStmt.execute();
            
            while (selectEnvironmentRs.next()) {
                var privilege = selectEnvironmentRs.getColumnValue(2);
                var object_type = selectEnvironmentRs.getColumnValue(3);
                var name = selectEnvironmentRs.getColumnValue(4);
                if ((object_type == "TABLE" || object_type == "VIEW" ||  object_type == "PROCEDURE"  ||  object_type == "TASK") && (privilege=="OWNERSHIP")){
                     var grant =  `GRANT SELECT ON ${object_type} ${name} TO ROLE R_${DOMAIN_NAME}_${CONTEXT_NAME}_R`;
                     var grantObjectStmt = snowflake.createStatement({ sqlText: grant });
                     grantObjectStmt.execute();
                     result += `R_${DOMAIN_NAME}_${CONTEXT_NAME}_R +R \(${object_type}\) ${name} \n`;
                }
            }

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
    