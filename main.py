from reporting.voluum_data import fetch_columns, extract_conversions_data
from reporting.config import credentials
from reporting import FORMAT
import logging
from reporting.mysql_data import vads_site_perf_report_table
from reporting.send_email import sending_report_email
import pandas as pd
import datetime as dt
from reporting.workflow import vvads_site_perf, vvads_grpby_transform, vads_site_perf_transform, \
    verizon_ads_site_report

logging.basicConfig(level=logging.INFO, filename='yahoo_site_report.log', format=FORMAT,
                    datefmt='%d-%b-%y %H:%M:%S')


if __name__ == "__main__":

    # Extracting data from Voluum Tracking Platform
    vc_df = extract_conversions_data(28, fetch_columns, credentials, filter_by_col='trafficSourceId',
                                       predicate='89b073a0-a3e1-4519-89a3-89fe7863a22f')
    print(vc_df.revenue.sum())

    # Transforming the Voluum API Data
    vvads_perf = vvads_site_perf(vc_df)
    vvads_gpt = vvads_grpby_transform(vvads_perf)

    # Extracting Verizon Ads - Performance Data from MySQL Database
    query_df = vads_site_perf_report_table(28)
    t_query_df = vads_site_perf_transform(query_df)
    print(t_query_df.spend.sum())

    # Combining Conversion & Performance data
    result = verizon_ads_site_report(t_query_df, vvads_gpt)
    print(result.revenue.sum())
    print(result.spend.sum())

    # Exporting the result to a CSV file
    result.to_csv(r'./verizon_ads_site_performance_report.csv', index=False)

    # Sending CSV Report in an Email
    email_subject = 'Verizon Native Ads - Site Performance Report: {0}'.format(dt.datetime.today().strftime('%Y-%m-%d'))
    email_body = """
                    <p>Hi,&nbsp;</p>
                    <p>Please find the attached<strong> "<span style="color: #ff0000;">
                    Verizon Native Ads - Site Performance Report
                    /span>"</strong></p>
                    <p>&nbsp;</p>
                    <p><strong>Regards,</strong></p>
                    <p><strong>Ronnie Joshua</strong></p>
                """
    plain_or_html = "html"
    email_sender = 'sender@domain.com'
    email_receiver = 'receiver@domain.com'
    email_attachment = 'verizon_ads_site_performance_report.csv'
    sending_report_email(email_subject, email_body, plain_or_html, email_sender, email_receiver, email_attachment)

