from rich.console import Console
from rich.table import Table
from models.budget import Budget

# from rich.layout import Layout
# from rich.panel import Panel

console = Console()


class Formatter:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def load_viewer(data=None, kind=None, modifier=None):
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
                        console.print(f"[yellow]{data}[/yellow]")
                    case "warning":
                        console.print(f"[magenta]{data}[/magenta]")
                    case "failure":
                        console.print(f"[red]{data}[/red]")
                    case "menu_question_main":
                        console.print(f"[bold][#FF8C00]{data}[/#FF8C00][/bold]")
                    case "menu_question":
                        console.print(f"[cyan]{data}[/cyan]")
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
                elif kind == "transaction_details":
                    color = "green" if data[0].kind == "income" else "red"
                    table = Table(show_header=True, header_style="bold")
                    table.add_column("Timestamp", justify="right")
                    table.add_column("Value", justify="right")
                    table.add_column("Type", justify="right")
                    table.add_column("Category", justify="right")
                    table.add_column("Description", justify="right")
                    table.add_row(str(data[0].timestamp), f"[{color}]{str(data[0].amount)}[/{color}]",
                                  str(data[0].kind), str(data[0].category),
                                  str(data[0].description) if data[0].description else "[dim]n/a[/dim]",
                                  end_section=True)
                    console.print(table)

    @staticmethod
    def display_budgets(data=None, transactions=None):
        if isinstance(data, Budget):
            table = Table(show_header=True, header_style="bold")
            table.add_column("Timestamp", justify="right")
            table.add_column("Name", justify="right")
            table.add_column("Limit", justify="right")
            table.add_column("Applies to", justify="right")
            table.add_column("Status", justify="right")
            spent = calculate_spent(transactions, data)
            bar, status = create_budget_display(spent, data.limit)
            filled = bar.count("█")
            if filled < 5:
                color = "green"
            elif filled < 9:
                color = "yellow"
            else:
                color = "red"
            displayed_categories = []
            for cat in data.categories:
                displayed_categories.append(cat)
            printed_categories = ", ".join(displayed_categories)
            table.add_row(str(data.timestamp), str(data.name), str(data.limit), printed_categories,
                          f"[{color}]{bar}\n{status}[/{color}]",
                          end_section=True)
            console.print(table)
        if isinstance(data, list):
            table = Table(show_header=True, header_style="bold")
            table.add_column("Index", justify="right")
            table.add_column("Created on", justify="right")
            table.add_column("Name", justify="right")
            table.add_column("Limit", justify="right")
            table.add_column("Applies to", justify="right")
            table.add_column("Status", justify="right")
            i = 1
            for budget in data:
                spent = calculate_spent(transactions, budget)
                bar, status = create_budget_display(spent, budget.limit)
                filled = bar.count("█")
                if filled < 5:
                    color = "green"
                elif filled < 9:
                    color = "yellow"
                else:
                    color = "red"
                displayed_categories = []
                budget.timestamp = budget.timestamp[:10]
                for cat in budget.categories:
                    displayed_categories.append(cat)
                printed_categories = ", ".join(displayed_categories)
                table.add_row(f"[bold cyan]{str(budget.index)}[/bold cyan].", budget.timestamp, budget.name,
                              str(budget.limit),
                              printed_categories, f"[{color}]{bar}\n{status}[/{color}]", end_section=True)
                i += 1
            console.print(table)


def create_budget_display(spent, limit):
    percentage = spent / limit
    width = 10
    filled = int(percentage * width)
    if filled > width:
        filled = width
    empty = width - filled

    bar = "█" * filled + "░" * empty
    if percentage <= 1.0:
        status = f"{percentage * 100:.0f}% Used"
    else:
        percent_over = (percentage - 1.0) * 100
        status = f"{percent_over:.0f}% OVER"

    return bar, status


def calculate_spent(transactions, budget):
    spent = 0
    for cat in budget.categories:
        for transaction in transactions:
            if transaction.category == cat:
                spent += transaction.amount
    return spent
