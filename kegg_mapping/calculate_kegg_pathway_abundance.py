import pandas as pd
import os
import argparse


def calculate_kegg_pathway_abundance(ko_abundance_file, mapping_file):

    """
    Aggregates KO abundances to KEGG pathway-level abundances.

    Args:
        ko_abundance_file (str): Path to the KO abundance file (gzip-compressed TSV).
        mapping_file (str): Path to the KO-to-KEGG mapping file (CSV).

    Output:
        Saves the aggregated KEGG pathway-level abundances to `KEGG_path_abun_unstrat.csv`.
    """

    ko_df = pd.read_csv(ko_abundance_file, sep='\t', compression='gzip')

    mapping_ko_kegg_df = pd.read_csv(mapping_file)

    selected_col = [v for v in ko_df.columns if v != 'function']
    final_col = selected_col.copy()
    final_col.insert(0, 'Pathway')
    pathways_df = pd.DataFrame(columns=final_col)

    check_ko = []

    for kegg_pathway in mapping_ko_kegg_df['Pathway'].values:
        ko_numbers = mapping_ko_kegg_df.loc[mapping_ko_kegg_df['Pathway'] == kegg_pathway].values.tolist()[0]
        ko_numbers = [v for v in ko_numbers if str(v) != 'nan']
        check_ko.extend(ko_numbers)
        selected_co = ko_df.loc[ko_df['function'].isin(ko_numbers)]
        values_list = [kegg_pathway]
        values_list.extend(selected_co[selected_col].sum(axis=0).values.tolist())
        pathways_df.loc[pathways_df.shape[0] + 1, final_col] = values_list

    check_ko = set(check_ko)
    total_ko_functions = ko_df['function'].values.tolist()
    missed_ko_numbers = [v for v in total_ko_functions if v not in check_ko]
    if missed_ko_numbers:
        print(f"\nMissed KO numbers:")
        print(f"Count: {len(missed_ko_numbers)}")
        print(f"List: {missed_ko_numbers[:10]}{'...' if len(missed_ko_numbers) > 10 else ''}")

    output_path = os.path.dirname(ko_abundance_file)
    pathways_df.to_csv(output_path + '/KEGG_path_abun_unstrat.csv', index=False)


if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Aggregate KO abundances to KEGG pathway-level abundances.")
    parser.add_argument('--ko_abundance',
                        help="Path to the KO abundance file (file name: 'KO_pred_metagenome_unstrat.tsv.gz'.")
    parser.add_argument('--mapping_file', help="Path to the KO-to-KEGG mapping file.")
    args = parser.parse_args()

    # Run the function with the parsed arguments
    calculate_kegg_pathway_abundance(args.ko_abundance, args.mapping_file)

