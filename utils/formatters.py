from rich.console import Console
from rich.table import Table

# from rich.layout import Layout
# from rich.panel import Panel

console = Console()


class Formatter:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def load_viewer(data=None, kind=None):
        # print(f"[DEBUG] {type(data)}")
        if data and kind:
            if isinstance(data, str):
                match kind:
                    case "path_to_view":
                        console.print(f"[dim]{data}[/dim]")
                    case "app_description":
                        console.print(f"[bold][#FF8C00]{data}[/#FF8C00][/bold]")
                    case "balance_good":
                        table = Table(show_header=False, header_style="bold magenta")
                        table.add_column("Balance")
                        table.add_row(f"[green]{data}[/green]")
                        console.print(table)
                    case "balance_bad":
                        table = Table(show_header=False, header_style="bold magenta")
                        table.add_column("Balance")
                        table.add_row(f"[red]{data}[/red]")
                        console.print(table)
                    case "success":
                        console.print(f"[yellow]{data.capitalize()}[/yellow]")
                    case "warning":
                        console.print(f"[magenta]{data.capitalize()}[/magenta]")
                    case "menu_question_main":
                        console.print(f"[bold][#FF8C00]{data.capitalize()}[/#FF8C00][/bold]")
                    case "menu_question":
                        console.print(f"[cyan]{data.capitalize()}[/cyan]")
                    case "menu_option":
                        console.print(f"{data}")
                    case "transaction":
                        table = Table(show_header=False, header_style="bold magenta")
                        table.add_column("Timestamp")
                        table.add_column("Value")
                        table.add_column("Type")
                        table.add_column("Category")
                        table.add_column("Description")

            if isinstance(data, list):
                # print(f"[DEBUG] DATA IS LIST")
                # print(f"[DEBUG] KIND IS {kind}")
                table = Table(show_header=True, header_style="bold")
                table.add_column("Index", justify="right")
                table.add_column("Timestamp", justify="right")
                table.add_column("Value", justify="right")
                table.add_column("Type", justify="right")
                table.add_column("Category", justify="right")
                table.add_column("Description", justify="right")
                transaction_balance = 0
                i = 1
                if kind == "transactions_list":
                    for item in data:
                        if item.kind == "income":
                            color = "green"
                            transaction_balance += item.amount
                        else:
                            color = "red"
                            transaction_balance -= item.amount
                        item.timestamp = item.timestamp[:19].replace("T", " ")
                        # print(f"[DEBUG] i: {i}")
                        # print(f"[DEBUG] len(data): {len(data)}")
                        table.add_row(f"[bold cyan]{item.index}[/bold cyan].", item.timestamp,
                                      f"[{color}]${str(item.amount)}[/{color}]", item.kind,
                                      item.category,
                                      item.description if item.description else f"[dim]n/a[/dim]",
                                      end_section=True if i == len(data) else False)
                        i += 1
                    color = "green" if transaction_balance > -0.0001 else "red"
                    table.add_row("[bold]TOTAL[/bold]", "", f"[{color}]${transaction_balance:.2f}[/{color}]",
                                  "", "", "",
                                  end_section=True)
                    console.print(table)
                elif kind == "incomes_list":
                    # print(f"[DEBUG] Incomes List Data: {data}")
                    for item in data:
                        # print(f"[DEBUG] {item}")
                        if item.kind != "income":
                            continue
                        transaction_balance += item.amount
                        item.timestamp = item.timestamp[:19].replace("T", " ")
                        # print(f"[DEBUG] i: {i}")
                        # print(f"[DEBUG] len(data): {len(data)}")
                        table.add_row(f"[bold cyan]{item.index}[/bold cyan].", item.timestamp,
                                      f"[green]${str(item.amount)}[/green]", item.kind,
                                      item.category,
                                      item.description if item.description else f"[dim]n/a[/dim]",
                                      end_section=True if i == len(data) else False)
                        i += 1
                    color = "green" if transaction_balance > -0.0001 else "red"
                    table.add_row("[bold]TOTAL[/bold]", "", f"[{color}]${transaction_balance:.2f}[/{color}]",
                                  "", "", "",
                                  end_section=True)
                    console.print(table)
                elif kind == "expenses_list":
                    # print(f"[DEBUG] Expenses List Data: {data}")
                    for item in data:
                        # print(f"[DEBUG] {item}, {item.kind}")
                        if item.kind != "expense":
                            continue
                        transaction_balance -= item.amount
                        item.timestamp = item.timestamp[:19].replace("T", " ")
                        # print(f"[DEBUG] i: {i}")
                        # print(f"[DEBUG] len(data): {len(data)}")
                        table.add_row(f"[bold cyan]{item.index}[/bold cyan].", item.timestamp,
                                      f"[red]${str(item.amount)}[/red]",
                                      item.kind,
                                      item.category,
                                      item.description if item.description else f"[dim]n/a[/dim]",
                                      end_section=True if i == len(data) else False)
                        i += 1
                    color = "green" if transaction_balance > -0.0001 else "red"
                    table.add_row("[bold]TOTAL[/bold]", "", f"[{color}]${transaction_balance:.2f}[/{color}]",
                                  "", "", "",
                                  end_section=True)
                    console.print(table)
                elif kind == "transaction_details":
                    table = Table(show_header=True, header_style="bold")
                    table.add_column("Timestamp", justify="right")
                    table.add_column("Value", justify="right")
                    table.add_column("Type", justify="right")
                    table.add_column("Category", justify="right")
                    table.add_column("Description", justify="right")
                    table.add_row(str(data[0].timestamp), str(data[0].amount), str(data[0].kind), str(data[0].category),
                                  str(data[0].description) if data[0].description else "[dim]n/a[/dim]",
                                  end_section=True)
                    console.print(table)

    @staticmethod
    def transform_month_to_int(month_name):
        match month_name:
            case 'january':
                return 1
            case 'february':
                return 2
            case 'march':
                return 3
            case 'april':
                return 4
            case 'may':
                return 5
            case 'june':
                return 6
            case 'july':
                return 7
            case 'august':
                return 8
            case 'september':
                return 9
            case 'october':
                return 10
            case 'november':
                return 11
            case 'december':
                return 12
