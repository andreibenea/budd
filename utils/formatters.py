from rich.console import Console
from rich.table import Table

console = Console()


class Formatter:
    def __init__(self, **kwargs):
        pass

    @staticmethod
    def load_viewer(data=None):
        # print(f"[DEBUG] {type(data)}")
        if data:
            if isinstance(data, str):
                console.print(data)
            if isinstance(data, list):
                table = Table(show_header=True, header_style="bold")
                table.add_column("Timestamp")
                table.add_column("Value", justify="right")
                table.add_column("Type", justify="right")
                table.add_column("Category", justify="right", style="dim")
                table.add_column("Description", justify="right")
                for item in data:
                    item.timestamp = item.timestamp[:19].replace("T", " ")
                    color = "green" if item.kind == "deposit" else "red"
                    table.add_row(item.timestamp, f"[{color}]${str(item.amount)}[/{color}]", item.kind, item.category,
                                  item.description if item.description else "n/a")
                console.print(table)
