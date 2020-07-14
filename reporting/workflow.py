import pandas as pd


def vvads_site_perf(df):
    req_cols = ['postbackTimestamp', 'clickId', 'campaignId', 'campaignName', 'offerId', 'offerName',
                'trafficSourceId', 'trafficSourceName', 'deviceName', 'revenue', 'customVariable1', 'customVariable2',
                'customVariable3', 'customVariable4']

    col_rename = {'postbackTimestamp': 'day', 'customVariable1': 'campaign_id', 'customVariable2': 'adgroup_id',
                  'deviceName': 'device_type', 'customVariable3': 'adid', 'customVariable4': 'external_site_name'}

    reporting_cols = ['day', 'clickId', 'campaignId', 'campaignName', 'offerId', 'offerName',
                      'trafficSourceId', 'trafficSourceName', 'revenue', 'conversions',
                      'campaign_id', 'adgroup_id', 'adid', 'external_site_name', 'device_type']

    df = df.loc[:, req_cols]
    df.loc[:, 'conversions'] = 1
    df.rename(inplace=True, columns=col_rename)
    df = df.loc[:, reporting_cols]
    return df


def vvads_grpby_transform(df):
    repl_dict = {'Desktop': 'Desktop', 'Mobile phone': 'SmartPhone', 'Tablet': 'SmartPhone'}
    df['device_type'] = df['device_type'].map(repl_dict)
    df.loc[:, 'external_site_name'] = df['external_site_name'].apply(lambda x: x if x.isupper() else "NON ATTRIBUTED")
    cols_to_grpby = ['day', 'campaign_id', 'adgroup_id', 'external_site_name', 'device_type']
    df = df.groupby(cols_to_grpby)['conversions', 'revenue'].sum().reset_index()
    return df


def vads_site_perf_transform(df):
    column_rename = {
        'date': 'day', 'Advertiser ID': 'advertiser_id', 'Advertiser Name': 'advertiser_name',
        'Campaign ID': 'campaign_id', 'Campaign Name': 'campaign_name', 'Ad Group ID': 'adgroup_id',
        'Ad Group Name': 'adgroup_name', 'External Site Name': 'external_site_name',
        'Device Type': 'device_type', 'SUM(Impressions)': 'impression', 'SUM(Clicks)': 'clicks',
        'SUM(Spend)': 'spend'
    }

    df.rename(inplace=True, columns=column_rename)
    df['day'] = pd.to_datetime(df['day']).dt.date

    # change dtype from int to object in pandas
    # df['campaign_id'] = df['campaign_id].apply(str)
    # df['adgroup_id'] = df['adgroup_id'].apply(str)

    df = df[['day', 'advertiser_id', 'advertiser_name', 'campaign_id', 'campaign_name', 'adgroup_id', 'adgroup_name',
             'external_site_name', 'device_type', 'impression', 'clicks', 'spend']]
    return df


def verizon_ads_site_report(yads_df, vol_df):
    left_keys = ['day', 'campaign_id', 'adgroup_id', 'external_site_name', 'device_type']
    right_keys = ['day', 'campaign_id', 'adgroup_id', 'external_site_name', 'device_type']
    result = pd.merge(yads_df, vol_df, how='outer', left_on=left_keys, right_on=right_keys)
    return result
