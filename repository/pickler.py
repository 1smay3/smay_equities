import os
import pickle


def pickle_dict_of_dataframes_to_file(dataframes_dict, save_directory, file_name):
    """
    Pickle a dictionary of Pandas DataFrames and save it to a file.

    :param dataframes_dict: Dictionary where keys are strings and values are Pandas DataFrames.
    :param save_directory: Directory where the pickled file will be saved.
    :param file_name: Name to use for the pickled file.
    """
    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Construct the full path for the pickled file
    file_path = os.path.join(save_directory, f"{file_name}.pkl")

    # Pickle the dictionary of DataFrames to the specified file
    with open(file_path, "wb") as file:
        pickle.dump(dataframes_dict, file)
