"""
This file parsers the metadata file (.sfx) file to filter tags.
 - It filters only single tags and gives the timestamp with the scores for that tag.
 - Currently, it only filters a single tag within a timeframe.
 - In the future, we need to implement an advanced filtering mechanism using logical operations (&, | etc).
"""

import collections
import sys
import os
from collections import OrderedDict
import numpy as np
import pandas as pd


def process_tag_result(result_dictionary, scores_dict):
    for tag in result_dictionary:
        result_dictionary[tag] = sorted(set([elem for sublist in result_dictionary[tag] for elem in sublist]))
    df = pd.DataFrame(columns=['Tags', 'Time', 'Score'])
    for tag, times in result_dictionary.items():
        for time in times:
            df.loc[len(df.index)] = [tag, time, [score for score in scores_dict[time].split(",") if tag in score][0]]
    return df


def get_time_interval_tags(scores_dict, tag, time_windows_indices):
    result = collections.defaultdict(list)
    for index, window in enumerate(time_windows_indices):
        matching_idx = [idx for idx, s in enumerate(list(scores_dict.values())[window[0]:window[1]]) if
                        tag in s]
        if len(matching_idx) != 0:
            result[tag].append(np.array(list(scores_dict.keys())).take(np.array(matching_idx) + window[0]))
    df = process_tag_result(result, scores_dict)
    return df


def get_sfx_files(folder_path, date, sfx_files_with_path):
    sfx_format = "sfx"
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for file_name in [f for f in file_names if f.endswith("." + sfx_format) and f.startswith(str(date).split()[0])]:
            sfx_files_with_path.append(os.path.join(dir_path, file_name))
    return sfx_files_with_path


# ToDo:// create tags
def get_tag_combinations(audio_effects):
    return audio_effects


def is_starting_line(line):
    if line.startswith("FFS"):
        return True


def filter_sfx_file(sfx_file, audio_effects, time_duration, filename_text):
    dict_times_score = OrderedDict()
    with open(sfx_file) as f:
        lines = f.readlines()
        start_read = False
        for line in lines:
            if not start_read and is_starting_line(line):
                start_read = True
                continue
            if start_read:
                split_line = line.split(line_split_separator)
                dict_times_score[split_line[0].rstrip("|").split("|")[1].replace(file_name_text, '')] = split_line[
                    1].lstrip("|")

    # Creating time windows
    time_windows_indices = [(i, time_duration + i)
                            for i in range(0, int(float(list(dict_times_score.keys())[-1].replace(filename_text, ''))))]
    tag_combinations = get_tag_combinations(audio_effects)

    # For each window find the tags
    df = get_time_interval_tags(dict_times_score, tag_combinations, time_windows_indices)
    return df


# ssfx -r —files /tv/2022/2022-03/20220305 —effects{{drum|percussion}&{laughter}} —within 5

if __name__ == '__main__':
    FILE_LOCATION = sys.argv[1]
    START_DATE = sys.argv[2]
    END_DATE = sys.argv[3]
    EFFECTS = sys.argv[4]
    TIME_DURATION = int(sys.argv[5])
    LOGS = int(sys.argv[6])

    # FILE_LOCATION = "/Users/saby/Documents/RedHen/Baselining/TaggedAudioFiles/"
    #START_DATE = "2010-01-01"
    #END_DATE = "2020-01-01"
    # EFFECTS = "Clicking"
    # TIME_DURATION = 5
    # LOGS = 1

    # Code Starts from here ....
    line_split_separator = "SFX_01"

    date_range = pd.date_range(start=START_DATE, end=END_DATE)
    sfx_files_with_path = []
    for date in date_range:
        sfx_files_with_path = get_sfx_files(FILE_LOCATION, date, sfx_files_with_path)  # Get SFX files

    for index, sfx_file in enumerate(sfx_files_with_path):
        csv_file_name = os.path.split(sfx_files_with_path[index])[1].replace(".sfx", ".csv")
        file_name = os.path.split(sfx_files_with_path[index])[1].replace(".sfx", "")
        file_name_text = "-".join(file_name.split("_", 2)[:2]).replace("-", "")
        if LOGS: print("Starting the filtering script for filename ", sfx_file)
        df = filter_sfx_file(sfx_file, EFFECTS, TIME_DURATION, file_name_text)
        # Dump Dataframe to CSV
        df.to_csv(csv_file_name)
        if LOGS: print("Operation completed for sfx file ", sfx_file)
    if LOGS: print("All Done ...")
