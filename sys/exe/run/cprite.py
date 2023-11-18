import csv
from rich import print
from rich.table import Table
import textwrap
from io import StringIO

# Copyright Notice
copyright_notice = (
    "The PXY® trading tool and its content are protected by copyright laws and international treaties."
    " All rights reserved by PXY® and Unauthorized use, reproduction, and distribution are strictly prohibited."
    " Infringement may lead to legal action and financial penalties. PXY® is committed to protecting its intellectual property."
)

# Set the desired width
width = 30

# Use textwrap to format the text with a fixed width and center-align
wrapped_notice = textwrap.fill(copyright_notice, width, break_long_words=False).center(width)

# Create a CSV file-like object using StringIO
csv_data = StringIO()
csv_writer = csv.writer(csv_data)
csv_writer.writerow([wrapped_notice])
csv_data.seek(0)

# Create a table
table = Table()

# Read the CSV data into the table
table.add_row(*csv_reader := csv.reader(csv_data), end="")

# Display the table
print(table)








