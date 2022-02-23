# -*- coding: utf-8 -*-
# Copyright (c) 2022 by Phuc Phan

import os
import torch
import pickle
import argparse
from tqdm import tqdm


def make_standard(data_path, dataset_type):
    with open(f"{data_path}/{dataset_type}_pair.pkl", 'rb') as f:
        triple_data = pickle.load(f)

    standard_list = []

    header_fmt = 'Make standard {:>4s}'
    for triplet in tqdm(triple_data, desc=f"{header_fmt.format(dataset_type.upper())}"):
        aspect_temp = []
        asp_pol_temp = []
        for temp_t in triplet:
            ap = [temp_t[0][0], temp_t[0][-1], temp_t[2]]
            if ap not in asp_pol_temp:
                asp_pol_temp.append(ap)

            a = [temp_t[0][0], temp_t[0][-1]]
            if a not in aspect_temp:
                aspect_temp.append(a)

        standard_list.append({
            'asp_target': aspect_temp,
            'asp_pol_target': asp_pol_temp
        })

    return standard_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_path", type=str, default='./data/v2/14rest/pair',
                        help="Path to the dataset.")
    parser.add_argument('--output_path', type=str, default='./data/v2/14rest/preprocess',
                        help='Path to the saved standard data.')

    args = parser.parse_args()

    dev_standard = make_standard(args.data_path, 'dev')
    test_standard = make_standard(args.data_path, 'test')

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    output_path = f"{args.output_path}/data_standard.pt"

    print(f"Saved data : `{output_path}`.")
    torch.save({
        'dev': dev_standard,
        'test': test_standard
    }, output_path)
