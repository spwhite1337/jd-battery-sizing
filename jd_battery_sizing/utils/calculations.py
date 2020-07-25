import pandas as pd
import numpy as np


from jd_battery_sizing.utils.wrangle import daily_aggregation
from config import logger


def energy_by_demand(df: pd.DataFrame, interval_min: int = 15):
    """
    Subset demand by various cutoffs, integrate energy above and below cutoff
    """
    total_time_days = (df['Timestamp'].max() - df['Timestamp'].min()).days

    calc_col = 'ApparentPowerMean_KVA_'
    # outline cutoffs in 100 kW intervals from min to max of mean apparent power
    min_calc, max_calc = df[calc_col].min(), df[calc_col].max()
    cutoffs = np.linspace(min_calc, max_calc, int((max_calc - min_calc) / 100))

    # For each cutoff sum the total energy and number of time intervals for kW-h
    logger.info('Calculating Energy Demands by Cutoff')
    records = []
    for cutoff in cutoffs:
        record = {}

        # Energy above
        df_above = df[df[calc_col] >= cutoff]
        if df_above.shape[0] == 0:
            total_time_min, total_energy_kwh, max_daily_energy_above = 0., 0, 0.
        else:
            total_time_min = df_above.shape[0] * interval_min
            total_energy_kwh = df_above[calc_col].sum() * total_time_min / 60

            df_daily = daily_aggregation(df_above, only_weekdays=False)
            max_daily_energy_above = df_daily[calc_col].max() * 24

        record.update({
            'daily_energy_above_kwh': total_energy_kwh / total_time_days,
            'daily_min_above': total_time_min / total_time_days,
            'max_daily_energy_above_kWh': max_daily_energy_above
        })

        # Energy below
        df_below = df[df[calc_col] < cutoff]
        if df_below.shape[0] == 0:
            total_time_min, total_energy_kwh = 0., 0
        else:
            total_time_min = df_below.shape[0] * interval_min
            total_energy_kwh = df_below[calc_col].sum() * total_time_min / 60
        record.update({
            'daily_energy_below_kwh': total_energy_kwh / total_time_days,
            'daily_min_below': total_time_min / total_time_days,
        })

        record['ApparentPowerCutoff_KVA'] = cutoff

        # Gather
        records.append(record)
    df_output = pd.DataFrame.from_records(records)

    # Other calcs
    df_output['total'] = df_output['daily_energy_above_kwh'] + df_output['daily_energy_below_kwh']
    df_output['FractionEnergyAbove'] = df_output['daily_energy_above_kwh'] / df_output['total']
    df_output['total'] = df_output['daily_min_above'] + df_output['daily_min_below']
    df_output['FractionTimeAbove_min_'] = df_output['daily_min_above'] / df_output['total']
    df_output = df_output.drop('total', axis=1)

    return df_output
