import pandas as pd
import numpy as np

from config import logger


def energy_by_demand(df: pd.DataFrame, interval_min: int = 15):
    """
    Subset demand by various cutoffs, integrate energy above and below cutoff
    """
    total_time_years = (df['Timestamp'].max() - df['Timestamp'].min()).year

    calc_col = 'ApparentPowerMean_KW_'
    # outline cutoffs in 100 kW intervals from min to max of mean apparent power
    min_calc, max_calc = df[calc_col].min(), df[calc_col].max()
    cutoffs = np.linspace(min_calc, max_calc, (max_calc - min_calc) / 100)

    # For each cutoff sum the total energy and number of time intervals for kW-h
    logger.info('Calculating Energy Demands by Cutoff')
    records = []
    for cutoff in cutoffs:
        record = {}

        # Energy above
        df_above = df[df[calc_col] < cutoff]
        if df_above.shape[0] == 0:
            record.update({'annual_energy_above_kwh': 0., 'annual_min_above': 0})
        else:
            total_time_min = df_above.shape[0] * interval_min
            total_energy_kwh = df_above[calc_col].sum() * total_time_min / 60
            record.update({
                'annual_energy_above_kwh': total_energy_kwh / total_time_years,
                'annual_min_above': total_time_min / total_time_years
            })

        # Energy below
        df_below = df[df[calc_col] >= cutoff]
        if df_below.shape[0] == 0:
            record.update({'annual_energy_below_kwh': 0., 'annual_min_below': 0})
        else:
            total_time_min = df_below.shape[0] * interval_min
            total_energy_kwh = df_below[calc_col].sum() * total_time_min / 60
            record.update({
                'annual_energy_below_kwh': total_energy_kwh / total_time_years,
                'annual_min_below': total_time_min / total_time_years
            })

        record['cutoff'] = cutoff

        # Gather
        records.append(record)
    df_output = pd.DataFrame.from_records(records)

    # Other calcs
    df['TotalAnnualEnergy_kWh_'] = df['annual_energy_above_kwh'] + df['annual_energy_below_kwh']
    df['FractionEnergyAbove_kWh_'] = df['annual_energy_above_kwh'] / df['TotalAnnualEnergy']
    df['TotalTime_min_'] = df['annual_min_above'] + df['annual_min_below']
    df['FractionTimeAbove_min_'] = df['annual_min_above'] / df['TotalTime_min_']

    return df_output
