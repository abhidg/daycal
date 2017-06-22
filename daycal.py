#!/usr/bin/python3
# License: MIT (see LICENSE.txt)
# Copyright: (c) 2017 Abhishek Dasgupta
# daycal: generate a calendar with day numbers

import os
import calendar
import operator
import datetime
import argparse
from typing import Sequence, Tuple, List, Iterator
from subprocess import call

Year = int
Weekday = int
Day = int
File = str
MONTHS = list(range(1, 13))
MONTH_NAMES = list(calendar.month_abbr)
snd = operator.itemgetter(1)

with open('latex_header.tex') as fp:
    latex_template = fp.read()
end_latex_document = """\n\end{document}"""

def texday_portrait(dw: Tuple[Day, Weekday], colour: str) -> str:
    day, weekday = dw
    if weekday >= 5:
        return "\\textcolor{%s}{%d}\\\\\n" % (colour, day)
    else:
        return "%d\\\\\n" % day

def accumulate(xs: Iterator[int]) -> Sequence[int]:
    acc = 0
    ys = []
    for i in xs:
        ys.append(acc)
        acc += i
    return ys

def yeardays_month(acc: int, ys: Sequence[Tuple[Day, Weekday]]) -> Sequence[Tuple[Day, Weekday]]:
    return [(acc + x, y) for x, y in ys]

def accumulate_days(monthdays_acc: Sequence[int],
                    days_weekdays: Sequence[Sequence[Tuple[Day, Weekday]]]) -> Sequence[Sequence[Tuple[Day, Weekday]]]:
    return [yeardays_month(acc, xs) for acc, xs in zip(monthdays_acc, days_weekdays)]

def drop_trailing_zeros(xs: Sequence[Tuple[Day, Weekday]]) -> List[Tuple[Day, Weekday]]:
    return [(x, y) for x, y in xs if x > 0]

def get_monthdays(year: Year = None) -> Sequence[Sequence[Tuple[Day, Weekday]]]:
    c = calendar.Calendar()
    if year is None:
        year = datetime.datetime.utcnow().year
    monthdays = accumulate(y for x, y in
                           (calendar.monthrange(year, month) for month in MONTHS))
    month_weekdays = accumulate_days(monthdays,
                                     [drop_trailing_zeros(list(c.itermonthdays2(year, month))) for month in MONTHS])
    return month_weekdays

def tex_portrait(year: Year, colour: str, makepdf: bool = True, keeptex: bool = False) -> None:
    if not os.path.exists("tex"):
        os.mkdir("tex")
    fn = os.path.join("tex", "%d.tex" % year)
    fp = open(fn, 'w')
    fp.write(latex_template.replace("$year", str(year)))
    md = get_monthdays(year)
    groups = [md[:3], md[3:6], md[6:9], md[9:]]  # Q1, Q2, Q3, Q4 of year
    fp.write("\\begin{multicols}{5}\n")
    month_number = 0
    for quarter in groups:
        for m in quarter:
            month_number += 1
            fp.write("\n\\textbf{\\Large %s}\\\\\n" % MONTH_NAMES[month_number])
            fp.write(''.join(texday_portrait(i, colour) for i in m))
        fp.write("\\pagebreak\n")
    fp.write("\\end{multicols}\n")
    fp.write(end_latex_document)
    fp.close()
    if makepdf:
        call(["pdflatex", "tex/%d.tex" % year])
    if not keeptex:
        os.remove(fn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="which year to generate calendar for (default: current)",
                        type=int, default=datetime.datetime.utcnow().year)
    parser.add_argument("-c", "--colour", help="colour to use for weekends", default="red")
    parser.add_argument("--no-pdf", help="do not generate a pdf", action="store_false")
    parser.add_argument("--keep-tex", help="keep intermediate tex file", action="store_true")
    args = parser.parse_args()
    tex_portrait(year=args.year, colour=args.colour, makepdf=args.no_pdf, keeptex=args.keep_tex)
