from rich import print
from rich.table import Table
import textwrap

# ANSI color codes
BRIGHT_YELLOW = '\033[93m'
BRIGHT_RED = '\033[91m'
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

# Add the column header "${BRIGHT_YELLOW}PXY® ${BRIGHT_YELLOW}PreciseXceleratedYield ${BRIGHT_YELLOW}Pvt Ltd™:${NC}"
table.add_column(f"[{BRIGHT_YELLOW}]PXY® PreciseXceleratedYield Pvt Ltd™:{NC}")

# Add the row with the wrapped notice in bright red
table.add_row(f"[{BRIGHT_RED}]{wrapped_notice}{NC}")

# Display the table without extra space
print(table)











