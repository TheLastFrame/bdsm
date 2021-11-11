import numpy as np
import pandas as pd
from ._helper import _load_file

class AbalonesSeries(pd.Series):
    @property
    def _constructor(self):
        return AbalonesSeries
    
    @property
    def _constructor_expanddim(self):
        return AbalonesDataFrame
    

class AbalonesDataFrame(pd.DataFrame):    
    @property
    def _constructor(self):
        return AbalonesDataFrame
    
    @property
    def _constructor_sliced(self):
        return AbalonesSeries
    
    def clean(self, unit = 'imperial'):
        df = self
        
        if not df.attrs['cleaned']:
            # column types
            df['Sex'] = df['Sex'].astype('category')
            
            # set clean state
            df.attrs['cleaned'] = True
        
        return df
    
    def for_regression(self, sex):
        df = self
        if sex=='A':
            df = df         
        elif sex=='M':
            df = df[df["Sex"]=="M"].copy()
        elif sex=="F":
            df = df[df["Sex"]=="F"].copy()
        elif sex=="I":
            df = df[df["Sex"]=="I"].copy()
        else:
            print("Unknown parameter. Please use A for all, M for male, F for Female or I for Infants")

        df.drop("Sex", axis=1, inplace=True)

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


def abalones():
    """
    Abalone data

    Predicting the age of abalone from physical measurements.  The age of
    abalone is determined by cutting the shell through the cone, staining it,
    and counting the number of rings through a microscope -- a boring and
    time-consuming task.

    Description
    -----------
    4177 rows, 8 columns

    Given is the attribute name, attribute type, the measurement unit and a
    brief description.  The number of rings is the value to predict: either
    as a continuous value or as a classification problem.

	Name		Data Type	Meas.	Description
	----		---------	-----	-----------
	Sex		    nominal			M, F, and I (infant)
	Length		continuous	mm	Longest shell measurement
	Diameter	continuous	mm	perpendicular to length
	Height		continuous	mm	with meat in shell
	Whole weight	continuous	grams	whole abalone
	Shucked weight	continuous	grams	weight of meat
	Viscera weight	continuous	grams	gut weight (after bleeding)
	Shell weight	continuous	grams	after being dried
	Rings		integer			+1.5 gives the age in years
    """
    data_file = _load_file('abalones.csv')
    
    df = AbalonesDataFrame(pd.read_csv(data_file))
    df.attrs['cleaned'] = False
    
    return df
