import bioread
import pandas as pd
import os

def convert_acq_to_csv(input_file, output_file=None):
    """
    Convert .acq file to CSV format
    
    Args:
        input_file (str): Path to input .acq file
        output_file (str): Path to output CSV file (optional)
    """
    # Read the .acq file
    data = bioread.read_file(input_file)
    
    # Create a dictionary to store channel data
    data_dict = {}
    
    # Get time vector
    data_dict['Time'] = data.time_index
    
    # Get data from each channel
    for channel in data.channels:
        data_dict[channel.name] = channel.data
        
    # Create DataFrame
    df = pd.DataFrame(data_dict)
    
    # If no output file specified, use input filename with .csv extension
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.csv'
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"File converted successfully: {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "5min.acq"  # Using the .acq file in the current directory
    convert_acq_to_csv(input_file)