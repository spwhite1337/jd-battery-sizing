import pandas as pd
import numpy as np
from tqdm import tqdm

from config import logger


def energy_by_demand(df: pd.DataFrame, interval_min: int = 15, calc_col: str = 'ApparentPowerMean_KVA_'):
    """
    Subset demand by various cutoffs, integrate energy above and below cutoff
    """
    total_time_days = (df['Timestamp'].max() - df['Timestamp'].min()).days

    # outline cutoffs in 10 kW intervals from min to max of mean apparent power
    min_calc, max_calc = df[calc_col].min(), df[calc_col].max()
    cutoffs = np.linspace(min_calc, max_calc, int((max_calc - min_calc) / 10))

    # For each cutoff sum the total energy and number of time intervals for kW-h
    logger.info('Calculating Energy Demands by Cutoff')
    records = []
    for cutoff in tqdm(cutoffs):
        record = {calc_col + '_cutoff': cutoff}
        # Energy above
        df_above = df[df[calc_col] >= cutoff]
        if df_above.shape[0] == 0:
            total_time_min, total_energy_kwh = 0., 0
        else:
            # Number of 15 min intervals above cutoff
            total_time_min = df_above.shape[0] * interval_min
            # Mean power above, times total time above, divided by the total time in this data set
            # Units: kW * hr / day
            total_energy_kwh = df_above[calc_col].mean() * (total_time_min / 60) / total_time_days
        record.update({
            'daily_energy_above_kwh': total_energy_kwh,
            'daily_min_above': total_time_min / total_time_days,
        })

        # Energy below
        df_below = df[df[calc_col] < cutoff]
        if df_below.shape[0] == 0:
            total_time_min, total_energy_kwh = 0., 0
        else:
            total_time_min = df_below.shape[0] * interval_min
            total_energy_kwh = df_below[calc_col].mean() * (total_time_min / 60) / total_time_days
        record.update({
            'daily_energy_below_kwh': total_energy_kwh,
            'daily_min_below': total_time_min / total_time_days,
        })

        # Gather
        records.append(record)
    df_output = pd.DataFrame.from_records(records)

    # Other calcs
    df_output['total'] = df_output['daily_energy_above_kwh'] + df_output['daily_energy_below_kwh']
    df_output['FractionEnergyAbove'] = df_output['daily_energy_above_kwh'] / df_output['total']
    df_output['total'] = df_output['daily_min_above'] + df_output['daily_min_below']
    df_output['FractionTimeAbove'] = df_output['daily_min_above'] / df_output['total']
    df_output = df_output.drop('total', axis=1)

    return df_output
