from utils import fetch_table, plot_column

def main():
    url = input("Enter Wikipedia URL: ")
    output_file = "output_plot.png"
    
    # Fetch the table and numeric column
    df, column = fetch_table(url)
    
    # Plot if a numeric column is found
    if df is not None and column is not None:
        plot_column(df, column, output_file)
    else:
        print("Could not find a suitable numeric column to plot.")

if __name__ == "__main__":
    main()
