from rich import print
from rich.table import Table
from rich.console import Console
import textwrap

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

# Copyright Notice
copyright_notice = (
    "The PXY® trading tool and its content are protected by copyright laws and international treaties."
    " All rights reserved by PXY® and Unauthorized use, reproduction, and distribution are strictly prohibited."
    " Infringement may lead to legal action and financial penalties. PXY® is committed to protecting its intellectual property."
)

# Set the desired width
width = 41

# Use textwrap to format the text with a fixed width
wrapped_notice = textwrap.fill(copyright_notice, width, break_long_words=False)

# Create a table
table = Table()

# Add the column header "${YELLOW}PXY® ${YELLOW}PreciseXceleratedYield ${YELLOW}Pvt Ltd™:${NC}"
table.add_column("[yellow]${YELLOW}PXY® ${YELLOW}PreciseXceleratedYield ${YELLOW}Pvt Ltd™:${NC}[/yellow]")

# Add the row with the wrapped notice in red
table.add_row(f"[red]{wrapped_notice}[/red]")

# Display the table without extra space
print(table)











