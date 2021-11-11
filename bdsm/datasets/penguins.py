import numpy as np
import pandas as pd
from ._helper import _load_file

class PenguinsSeries(pd.Series):
    @property
    def _constructor(self):
        return PenguinsSeries
    
    @property
    def _constructor_expanddim(self):
        return PenguinsDataFrame
    

class PenguinsDataFrame(pd.DataFrame):    
    @property
    def _constructor(self):
        return PenguinsDataFrame
    
    @property
    def _constructor_sliced(self):
        return PenguinsSeries
    
    def clean(self, unit = 'imperial'):
        df = self
        
        if not df.attrs['cleaned']:
            # drop headers in data
            df = df[df['Comments'] != 'Comments']
            
            # NA: mean by species as float
            for col in ['CulmenLength', 'CulmenDepth', 'FlipperLength', 'BodyMass']:
                df[col] = df[col].astype('float')
                df[col] = df[col].fillna(df.groupby('Species')[col].transform('mean'))
            
            # Rename NA and . to Unknown
            df['Sex'] = np.where(df['Sex'].isna(), 'Unknown', df['Sex'].str.title())
            df['Sex'] = np.where(df['Sex'] == ".", 'Unknown', df['Sex'].str.title())
            
            # unneeded columns
            df = df.drop(df.columns[[0, 1, 3, 5, 6, 7, 8, 14, 15, 16]], axis = 1)
            
            # column types
            df['Species'] = df['Species'].astype('category')
            df['Island'] = df['Island'].astype('category')
            df['Sex'] = df['Sex'].astype('category')
            
            # set clean state
            df.attrs['cleaned'] = True
        
        return df
    
    def to_numeric(self):
        # clean df if not cleaned
        if not self.attrs['cleaned']:
            df = self.clean()
        else:
            df = self
        
        cat = df.select_dtypes(['category']).columns
        cat_codes = [x + '_cat' for x in cat]
        
        df[cat_codes] = df[cat].apply(lambda x: x.cat.codes)
        
        df = df.select_dtypes(include = ['number'])
        
        return df


def penguins():
    data_file = _load_file('penguins.csv')
    
    df = PenguinsDataFrame(pd.read_csv(data_file))
    df.attrs['cleaned'] = False
    
    return df
