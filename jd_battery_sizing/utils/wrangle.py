import pandas as pd


def daily_aggregation(df: pd.DataFrame, only_weekdays: bool = False) -> pd.DataFrame:
    if only_weekdays:
        df = df[df['Timestamp'].dt.dayofweek < 5]
    return df. \
        assign(Timestamp=df['Timestamp'].dt.round('D')). \
        groupby('Timestamp'). \
        agg(
            ActivePower_KW_=('ActivePowerMean_KW_', 'mean'),
            ReactivePowerMean_KVAR_=('ReactivePowerMean_KVAR_', 'mean'),
            ApparentPowerMean_KVA_=('ApparentPowerMean_KVA_', 'mean'),
            ActivePowerHigh=('ActivePowerHigh', 'max'),
            ReactivePowerHigh=('ReactivePowerHigh', 'max'),
            ApparentPowerHigh=('ApparentPowerHigh', 'max'),
            ActivePowerLow=('ActivePowerLow', 'min'),
            ReactivePowerLow=('ReactivePowerLow', 'min'),
            ApparentPowerLow=('ApparentPowerLow', 'min')
        ).reset_index()
