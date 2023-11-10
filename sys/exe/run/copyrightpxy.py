from rich.console import Console
from rich.panel import Panel

# Copyright Notice
copyright_notice = (
    "Copyright Notice: The 'PXY®' trading tool, along with all its associated content, including but not\n"
    "limited to software, documentation, graphics, and text, is safeguarded by copyright\n"
    "laws and international treaties. All rights pertaining to these intellectual properties\n"
    "are reserved by 'PXY® PreciseXceleratedYield.'\n\n"
    "Protection Under Copyright Laws: The copyright protection encompasses the entirety of\n"
    "the 'PXY®' trading tool, including its software, documentation, graphics, and textual\n"
    "components. This protection extends to prevent unauthorized reproduction, distribution,\n"
    "and modification.\n\n"
    "Express Prohibition: Users and third parties are explicitly prohibited from engaging in\n"
    "any activities that would infringe upon these copyrights. Specifically, this prohibition\n"
    "includes but is not limited to the following actions:\n\n"
    "Copying: No one is allowed to reproduce, duplicate, or make copies of the 'PXY®' trading\n"
    "tool or its associated content without obtaining explicit written consent from 'PXY®\n"
    "PreciseXceleratedYield.' This restriction ensures that the original creators maintain\n"
    "control over the dissemination and use of their intellectual property.\n\n"
    "Distribution: Unauthorized distribution, whether in physical or digital form, of the 'PXY®'\n"
    "trading tool and its associated content is strictly forbidden. This measure prevents the\n"
    "unauthorized spread of the software and its components.\n\n"
    "Modification: Any attempt to modify, alter, or create derivative works based on the 'PXY®'\n"
    "trading tool or its associated content without the explicit written consent of 'PXY®\n"
    "PreciseXceleratedYield' is in violation of copyright laws. This preserves the integrity\n"
    "and authenticity of the original work.\n\n"
    "Consequences of Infringement: The violation of these copyright conditions may result in\n"
    "serious legal consequences and financial penalties. 'PXY® PreciseXceleratedYield' is\n"
    "committed to safeguarding its intellectual property rights and will take legal action\n"
    "against any party found in breach of these conditions.\n\n"
    "In conclusion, the copyright protection of the 'PXY®' trading tool and its associated\n"
    "content is a fundamental measure taken by 'PXY® PreciseXceleratedYield' to protect their\n"
    "intellectual property rights. Users and third parties are urged to respect these copyright\n"
    "conditions, as any violation may lead to legal action and financial liabilities."
)

# Create a console for styling
console = Console()

# Create a styled panel with a title
panel = Panel(copyright_notice, title="Copyright Notice", padding=(1, 2))

# Display the panel
console.print(panel)
