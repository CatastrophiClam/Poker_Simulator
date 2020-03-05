## Data Stores
The goal of the data stores is handle selected accumulative and non accumulative data from each round record.
Each data extractor must be able to log information from round records and provide methods for 
obtaining that information for the data console.
- Each data store must implement the base_data_store methods
- Note we prepend accumulative data stores with the acc_ prefix so we can clearly see what accumulative
data stores we have
