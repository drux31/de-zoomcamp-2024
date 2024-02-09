if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Preprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Preprocessing: column befor rename - {data.columns[0]}")
    print(f"Preprocessing: rows with a null vendor ID column : {data['VendorID'].isna().sum()}")
    print(f"Preprocessing: rows with a zero trip distance: {data['trip_distance'].isin([0]).sum()}")
    
    print('\n')

    data = data[data['passenger_count'] > 0]
    print('-- removing rows with zero passenger_count')

    data = data[data['trip_distance'] > 0]
    print('-- removing rows with zero trip_distance')

    data = data.dropna(subset=['VendorID'])
    print('-- removing rows with NA vendor id')

    data = data.rename(columns={"VendorID": "vendor_id"})
    print('-- renaming column')

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    print('-- adding a new column')

    print('\n')
    
    print(f"Postprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Postrocessing: column befor rename - {data.columns[0]}")
    print(f"Postrocessing: adding a new column - {data.columns[20]}")
    print(f"Postprocessing: rows with a null vendor ID column : {data['vendor_id'].isna().sum()}")
    print(f"Postprocessing: rows with zero passengers: {data['trip_distance'].isin([0]).sum()}")
    print('\n')

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with no trip distance'
    assert output['vendor_id'].isna().sum() == 0, 'The vendor ID Has no value'

