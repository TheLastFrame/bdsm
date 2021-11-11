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
    """
    Penguins data

    Predicting the species of penguines from physical measurements. Includes nesting
    observations from Palmer Station Antarctica LTER and K. Gorman., penguin size data,
    and isotope measurements from blood samples for adult Adélie, Chinstrap, and Gentoo penguins.

    Description
    -----------
    346 rows, 17 columns

    Given is the attribute name, attribute type, the measurement unit and a
    brief description. 
    The species is the value to predict (as a classification problem).
    (Descriptions are from the original dataset)

	Name			Data Type	Meas.	Description
	----			---------	-----	-----------
	studyName		string			Sampling expedition from which data were collected, generated, etc.
 	Sample Number		integer			continuous numbering sequence for each sample
	Species			string			penguin species
	Region			string			region of Palmer LTER sampling grid
	Island			string			island near Palmer Station where samples were collected
	Stage			string			reproductive stage at sampling
	Individual ID		string			unique ID for each individual in dataset
	Clutch Completion	string			denoting if the study nest observed with a full clutch, i.e., 2 eggs
	Date Egg		date			denoting the date study nest observed with 1 egg (sampled)
	Culmen Length		float		mm	length of the dorsal ridge of a bird's bill
	Culmen Depth		float		mm	depth of the dorsal ridge of a bird's bill
	Flipper Length		integer		mm	length penguin flipper
	Body Mass		integer		grams	penguin body mass
	Sex			string			sex of an animal
	Delta 15 N		float			the measure of the ratio of stable isotopes 15N:14N
	Delta 13 C		float			the measure of the ratio of stable isotopes 13C:12C
	Comments		string			text providing additional relevant information for data
    """
    data_file = _load_file('penguins.csv')
    
    df = PenguinsDataFrame(pd.read_csv(data_file))
    df.attrs['cleaned'] = False
    
    return df
