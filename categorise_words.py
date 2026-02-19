import pandas as pd

# Load your Excel file
file_path = "english_banjara_words.xlsx"   # put your file name here
df = pd.read_excel(file_path)

# Add a helper column with word count
df["Word Count"] = df["English"].astype(str).apply(lambda x: len(x.split()))

# Sort rows based on word count
df_sorted = df.sort_values(by="Word Count")

# Save to a new Excel file
output_path = "sorted_by_wordcount.xlsx"
df_sorted.to_excel(output_path, index=False)

print(f"✅ Excel saved as {output_path}, sorted by word count")
