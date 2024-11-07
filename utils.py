import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import re

def clean_numeric_column(column_data):
    """Clean a column to extract numeric values, removing commas, units, etc."""
    cleaned_data = []
    for value in column_data:
        cleaned_value = re.sub(r'[^\d\.]', '', value)  # Keep only digits and periods
        try:
            cleaned_data.append(float(cleaned_value))
        except ValueError:
            cleaned_data.append(None)  # Append None if conversion fails
    return cleaned_data

def fetch_table(url):
    # Request the Wikipedia page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the first table on the page
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        print("No table found on the page.")
        return None

    # Parse table rows, handling rowspan and colspan
    rows = table.find_all('tr')
    data = []
    col_names = [col.text.strip() for col in rows[0].find_all(['td', 'th'])]
    row_span_tracker = [0] * len(col_names)  # To keep track of rowspans

    for row in rows[1:]:
        row_data = []
        cols = row.find_all(['td', 'th'])
        
        col_idx = 0  # Column index in the row_data list
        while col_idx < len(row_span_tracker):
            if row_span_tracker[col_idx] > 0:
                # If rowspan is active, fill in the cell from the previous row
                row_data.append(data[-1][col_idx])
                row_span_tracker[col_idx] -= 1
                col_idx += 1
            else:
                # Process next column in current row
                if cols:
                    col = cols.pop(0)
                    cell_value = col.text.strip()
                    rowspan = int(col.get('rowspan', 1))
                    colspan = int(col.get('colspan', 1))

                    # Fill in the cell value, respecting colspan
                    for _ in range(colspan):
                        row_data.append(cell_value)
                        if col_idx < len(row_span_tracker):
                            # Set rowspan if applicable
                            row_span_tracker[col_idx] = rowspan - 1 if rowspan > 1 else 0
                        else:
                            # Expand row_span_tracker if new columns are encountered
                            row_span_tracker.append(rowspan - 1 if rowspan > 1 else 0)
                        col_idx += 1
                else:
                    # If no more columns are left, fill with None
                    row_data.append(None)
                    col_idx += 1

        data.append(row_data)

    # Convert the processed data to a DataFrame
    df = pd.DataFrame(data, columns=col_names)

    # Try cleaning and finding a numeric column
    for column in df.columns:
        cleaned_column = clean_numeric_column(df[column])
        df[column] = pd.Series(cleaned_column)  # Replace with cleaned data
        
        # Check if at least half of the column values are numeric
        if df[column].notna().sum() > len(df) / 2:
            return df, column  # Return the DataFrame and the numeric column name

    print("No numeric column found in the table.")
    return None, None

def plot_column(df, column, output_file):
    # Drop rows with NaN in the numeric column
    df = df.dropna(subset=[column])
    
    # Plot the numeric column
    plt.figure(figsize=(10, 6))
    plt.plot(df[column].astype(float), marker='o')
    plt.title(f'Plot of {column}')
    plt.xlabel('Index of records')
    plt.ylabel(f'{column} (meters)')
    plt.grid(True)
    
    # Save the plot as an image file
    plt.savefig(output_file)
    print(f"Plot saved as {output_file}")