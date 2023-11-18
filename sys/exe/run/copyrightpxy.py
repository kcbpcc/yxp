from rich.console import Console
from rich.table import Table
import textwrap

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

# Create a console for styling
console = Console()

# Create a table
table = Table(show_header=False, box=None)

# Add a single cell to the table with the wrapped notice
table.add_row(wrapped_notice)

# Display the table
console.print(table)







