import mysql.connector as mysql
import logging
import pandas as pd
from reporting.config import credentials


def mysql_connector(func):
    def with_connection(*args, **kwargs):
        conn = mysql.connect(**credentials.get('reporting_db'))
        try:
            return_value = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            logging.error("Database connection error")
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        return return_value

    return with_connection


@mysql_connector
def vads_site_perf_report_table(conn, reporting_period):
    query = """
    SELECT 
        date,
        `Advertiser ID`,
        `Advertiser Name`,
        `Campaign ID`,
        `Campaign Name`,
        `Ad Group ID`,
        `Ad Group Name`,
        `External Site Name`,
        `Device Type`,
        SUM(Impressions),
        SUM(Clicks),
        SUM(Spend)
    FROM
        db_reporting.ad_yahoo_site_data_daily
    WHERE
        DATE(date) >= DATE(NOW()) - INTERVAL %s DAY
    GROUP BY 1 , 2 , 3 , 4 , 5 , 6, 7, 8, 9
    ORDER BY date ASC;
    """ % reporting_period
    return pd.read_sql(query, con=conn)
