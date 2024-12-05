import sys
import pandas as pd


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python transform.py <input_path> <output_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    pre_df = pd.read_csv(input_file)
    df_cleaned = pre_df.drop("numVotes", axis=1)
    df_cleaned.to_csv(output_file, index=False)
