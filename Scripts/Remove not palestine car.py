from os import stat
import pandas as pd 
import time

from googletrans import Translator
translator = Translator()

df = pd.read_csv("DataR2Hamza.csv")

df.drop(columns=[
    'اسم المُعلن',
    'رقم الهاتف',
    'موبايل',
    'Email',
    'Website',
    'المدينة',
    'العنوان',
    'تاريخ إنتهاء الإعلان',
    'حالة الإعلان',
    "معروضة"], inplace=True)

df=df[~df["رخصة السيارة"].str.contains("نمرة صفراء")]
print(df["رخصة السيارة"].value_counts())

df.drop(columns=["رخصة السيارة"] ,inplace=True)


