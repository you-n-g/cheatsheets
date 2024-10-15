import typer
app = typer.Typer()

@app.command()
def run() -> None:
    """Run command."""
    a = 3
    b = "a value that normal backtrace may not provide"
    x  # Here is the error!!

if __name__ == "__main__":
    app()
