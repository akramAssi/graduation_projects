    """script to append csv file
    """
import pandas as pd
all_filenames=["Data(R1).csv","Data(R2).csv","Data(R3).csv"]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "Data(final).csv", index=False, encoding='utf-8')
