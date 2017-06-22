# daycal

daycal is a small script to generate a calendar with one page for each quarter. Instead of using day of month, it uses day of year (from 1 to 365 or 366) in the calendar display.

## Requirements
- Python 3
- pdflatex: used to generate the pdf.

## Usage

    usage: daycal.py [-h] [-y YEAR] [-c COLOUR] [--no-pdf] [--keep-tex]
  
    optional arguments:
      -h, --help            show this help message and exit
      -y YEAR, --year YEAR  which year to generate calendar for (default: current)
      -c COLOUR, --colour COLOUR
                            colour to use for weekends
      --no-pdf              do not generate a pdf
      --keep-tex            keep intermediate tex file
