import argparse
from pathlib import Path

import numpy as np
import pandas as pd


colspecs = [(0, 7),
            (8, 13),
            (14, 21),
            (22, 29),
            (30, 37),
            (38, 45),
            (46, 53),
            (54, 61),
            (62, 69),
            (70, 84),
            (85, 92),
            (93, 108),
            (109, 121),
            (122, 132),
            (133, 142),
            (143, 152),
            (153, 165),
            (166, 179),
            (180, 193),
            ]


def main(filename):
    nums = []
    with open(filename, encoding='latin') as myFile:
        lookup = "Robuste Analyse"
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                nums.append(num)
        skiprows = nums[0] + 1
        nrows = nums[1] - nums[0] - 1

    df = pd.read_fwf(filename, encoding='latin', skiprows=skiprows,
                    nrows=nrows, colspecs=colspecs)

    columns = ['Freq. /Hz', 'Rhoa/Ohm*m', 'Phase /°',
            'dR /%', 'dP /°', 'Current /mA',
            'Date Time']

    date = df['Date /ddmmyy'].str.replace(".", "-", regex=False)
    time = df['Time /hhmmss'].str.replace(" ", "", regex=False)
    df['Date Time'] = pd.to_datetime(
        date + ' ' + time)


    df['dR /%'] = df['Rhoa/Ohm*m'] * df['dR /%'] / 100

    df['Phase /°'] = np.radians(df['Phase /°'])
    df['dP /°'] = np.radians(df['dP /°'])

    df = df[columns].dropna()

    new_cols = ['Frequency (Hz)', 'Amplitude (Ohm)', 'Phase (rad)',
                'dAmplitude (Ohm)', 'dPhase (rad)', 'Current (mA)',
                'Date Time']

    df.columns = new_cols

    new_filename = filename.with_suffix('.csv')
    df.to_csv(new_filename, index=None)
    print(f"Wrote file {new_filename.resolve()}")


parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()
filename = Path(args.path)

if __name__ == "__main__":
    main(filename)
