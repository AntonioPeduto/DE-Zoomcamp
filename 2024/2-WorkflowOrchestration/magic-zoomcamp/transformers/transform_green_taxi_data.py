if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    # Remove rows where the passenger count is equal to 0 and the trip distance is equal to zero
    data = data[(data['passenger_count']>0) & (data['trip_distance']>0)]
    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    # Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id
    data.columns = data.columns.str.replace('(?<=[a-z])(?=[A-Z])','_',regex=True).str.lower()
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # Add three assertions:
    # - vendor_id is one of the existing values in the column (currently)
    assert output['vendor_id'].notnull().all(), 'There are rows with no value for vendor_id'
    # - passenger_count is greater than 0
    assert (output['passenger_count'] > 0).all(), 'Not each value of passenger_count is greater than 0'
    # - trip_distance is greater than 0
    assert (output['trip_distance'] > 0).all(), 'Not each value of trip_distance is greater than 0'
    # Generic assert
    assert output is not None, 'The output is undefined'
