import unittest
import pandas as pd
from utils import fetch_table, plot_column

class TestWikipediaTablePlotter(unittest.TestCase):
    
    def setUp(self):
        # Example Wikipedia URL for testing
        self.valid_url = "https://en.wikipedia.org/wiki/Women%27s_high_jump_world_record_progression"
        self.invalid_url = "https://en.wikipedia.org/wiki/Non_existent_page"

    def test_fetch_table_valid_url(self):
        """Test fetch_table with a valid Wikipedia URL containing a numeric column."""
        df, column = fetch_table(self.valid_url)
        # Check if the DataFrame is not None
        self.assertIsNotNone(df, "Failed to fetch table from the valid URL")
        # Check if a numeric column was identified
        self.assertIsNotNone(column, "Failed to identify a numeric column in the table")
        # Verify the column contains numeric values
        self.assertTrue(pd.to_numeric(df[column], errors='coerce').notna().sum() > 0)

    def test_fetch_table_invalid_url(self):
        """Test fetch_table with an invalid Wikipedia URL."""
        df, column = fetch_table(self.invalid_url)
        # Expecting None for both since URL is invalid
        self.assertIsNone(df, "DataFrame should be None for an invalid URL")
        self.assertIsNone(column, "Column name should be None for an invalid URL")

    def test_plot_column(self):
        """Test plot_column with a small DataFrame containing numeric data."""
        # Create a sample DataFrame with numeric values
        df = pd.DataFrame({
            'Year': [1950, 1960, 1970, 1980],
            'Height': [1.5, 1.6, 1.7, 1.8]
        })
        output_file = "test_output_plot.png"
        
        # Plot the column and check if the file is created
        plot_column(df, 'Height', output_file)
        
        # Check if the plot was saved as an image file
        try:
            with open(output_file, 'r') as f:
                pass
        except FileNotFoundError:
            self.fail(f"Plot image {output_file} was not created")

if __name__ == "__main__":
    unittest.main()
