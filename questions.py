import pandas as pd
import random

def pick_and_combine_row(df, columns_to_combine):
    """
    Randomly picks a row from a DataFrame and combines specified columns into a single text, separated by newlines.

    Args:
        df (pd.DataFrame): The DataFrame to pick a row from.
        columns_to_combine (list): List of column names to combine.

    Returns:
        str: Combined text from the specified columns of the randomly selected row, separated by newlines.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    
    # Pick a random row
    random_index = random.randint(0, len(df) - 1)
    random_row = df.iloc[random_index]
    
    # Combine the values from the specified columns, separated by newlines
    combined_text = "\n\n".join(str(random_row[col]) for col in columns_to_combine if col in df.columns)
    
    return combined_text

def rand_choose():
    
    logic = pd.read_csv("C:\\Users\\tee_m\\Desktop\\cv\\Technical Questions\\Combined_Logic.csv", encoding='ISO-8859-1')
    stats = pd.read_csv("C:\\Users\\tee_m\\Desktop\\cv\\Technical Questions\\Combined_Stats.csv", encoding='ISO-8859-1')
    
    logic_text = pick_and_combine_row(logic, ["Question Number", "Question", "Answer Number", "Answer"])
    stats_text = pick_and_combine_row(stats, ["Question Number", "Question", "Answer Number", "Answer"])
    combined_text = f"Logic Question\n\n{logic_text}\n\nStatistics Question\n\n{stats_text}"
    print(combined_text)

    output_file = "C:\\Users\\tee_m\\Desktop\\gpt\\data.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(combined_text)

    print(f"\nCombined text has been exported to {output_file}")

if __name__ == "__main__":
    rand_choose()