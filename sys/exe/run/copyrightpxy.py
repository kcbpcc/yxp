from rich.console import Console
from rich.panel import Panel
import textwrap

# Copyright Notice
copyright_notice = (
    "The 'PXY®' trading tool and its content are protected by copyright laws and international treaties."
    " All rights reserved by 'PXY® .' Unauthorized use, reproduction, and distribution are strictly prohibited."
    " Infringement may lead to legal action and financial penalties. 'PXY® ' is committed to protecting its intellectual property."
)

# Set the desired width
width = 35

# Use textwrap to format the text with a fixed width
wrapped_notice = textwrap.fill(copyright_notice, width, break_long_words=False)

# Create a console for styling
console = Console()

# Create a styled panel with a title
panel = Panel(wrapped_notice, title="Copyright Notice", padding=(1, 2))

# Display the panel
console.print(panel)


