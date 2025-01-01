import argparse
import pandas as pd
from bioservices import KEGG


def ko_to_kegg_mapping(input_file):

    """
    Maps KEGG Orthology (KO) numbers to KEGG pathways using the KEGG API and saves the result in a CSV file.

    Args:
        input_file (str): Path to the input file (`KO_pred_metagenome_unstrat.tsv.gz`). This file
                          is expected to be a gzip-compressed TSV file containing a column
                          named 'function' with KO terms.

    Output:
        - `ko_to_kegg_mapping.csv`: A CSV file containing the KEGG pathways mapped to their corresponding KO terms.
    """

    df = pd.read_csv(input_file, sep='\t', compression='gzip')

    # Initialize KEGG service
    kegg = KEGG()

    pathways_dict = {}
    cnt = 0
    # Fetch pathways for each KO
    for ko in df['function'].values:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt)
        pathways = kegg.link("pathway", ko)
        try:
            consider_pathways = pathways.split('\n')
            selected_pathways = [v.split('path:')[1] for v in consider_pathways if v.count('map') == 0 and v != '']

            for path in selected_pathways:
                if path in pathways_dict.keys():
                    pathways_dict[path].append(ko)
                else:
                    pathways_dict[path] = [ko]
        except:
            print(ko + ' not found')

    df = pd.DataFrame.from_dict(pathways_dict, orient='index')
    df.to_csv(f'ko_to_kegg_mapping.csv', index=False)


if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Map KO numbers to KEGG pathways.")
    parser.add_argument('--input', help="Path to the `KO_pred_metagenome_unstrat.tsv.gz` file.")
    args = parser.parse_args()

    ko_to_kegg_mapping(args.input)

