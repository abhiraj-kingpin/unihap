"""
UniHAP CLI Application using Typer and Rich.
Commands:
- `unihap run <input_file>` — Executes the 12-layer enrichment pipeline
- `unihap ui` — Launches the Streamlit HITL Review Dashboard
- `unihap evaluate` — Scores predictions against 200-row ground truth
- `unihap info` — Displays active architecture and configuration
"""

import sys
import subprocess
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from unihap.pipeline import UniHAPPipeline
from unihap.config import settings

app = typer.Typer(
    name="unihap",
    help="UniHAP — Enterprise Product Intelligence & Attribute Enrichment Pipeline",
    add_completion=False
)
console = Console()


@app.command()
def run(
    input_file: Path = typer.Argument(..., help="Path to input XLSX or CSV catalog sheet"),
    output_file: Path = typer.Option(None, "--output", "-o", help="Optional output JSON/CSV path"),
):
    """Run the 12-layer UniHAP enrichment pipeline on a product catalog."""
    console.print(Panel.fit("[bold cyan]UniHAP 12-Layer Product Intelligence Pipeline[/bold cyan]\n[dim]Evidence-Grounded Catalog Enrichment[/dim]"))

    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found.[/red]")
        raise typer.Exit(code=1)

    pipeline = UniHAPPipeline()
    with console.status("[bold green]Executing 12-layer pipeline...[/bold green]"):
        result = pipeline.run(input_file, output_delivery_csv=output_file)

    table = Table(title="Pipeline Execution Summary", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim")
    table.add_column("Value", style="bold")

    table.add_row("Total Processed", str(result.total_processed))
    table.add_row("Auto-Approved (>=90%)", f"[green]{result.auto_approved_count}[/green]")
    table.add_row("Needs Review (70-89%)", f"[yellow]{result.needs_review_count}[/yellow]")
    table.add_row("Rejected (<70%)", f"[red]{result.rejected_count}[/red]")
    table.add_row("Execution Time", f"{result.execution_time_seconds}s")

    console.print(table)


@app.command()
def ui():
    """Launch the Streamlit Human-in-the-Loop Review Dashboard."""
    ui_path = Path(__file__).parent / "ui" / "app.py"
    console.print(f"[bold cyan]Launching UniHAP Streamlit Dashboard from: {ui_path}[/bold cyan]")
    subprocess.run(["streamlit", "run", str(ui_path)])


@app.command()
def info():
    """Display active pipeline architecture, LLM cascade, and configurations."""
    console.print(Panel(
        f"[bold]UniHAP Pipeline Configuration[/bold]\n\n"
        f"• [cyan]Environment:[/cyan] {settings.unihap_env}\n"
        f"• [cyan]Python Runtime:[/cyan] uv (Python 3.11+)\n"
        f"• [cyan]Groq LLM Tier:[/cyan] {settings.groq_model}\n"
        f"• [cyan]Local LLM Tier:[/cyan] {settings.ollama_model} ({settings.ollama_base_url})\n"
        f"• [cyan]Embeddings:[/cyan] {settings.embedding_model_name}\n"
        f"• [cyan]Auto-Approve Threshold:[/cyan] {settings.confidence_auto_approve * 100}%\n"
        f"• [cyan]Review Threshold:[/cyan] {settings.confidence_needs_review * 100}%",
        title="UniHAP System Info",
        border_style="blue"
    ))


if __name__ == "__main__":
    app()
