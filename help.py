#!/usr/bin/python3

import sys
import os

def Help():
	CSVtrad = "\x1B[1mCSV\x1B[0m"
	CSVWarn = "\x1B[38;2;255;192;0m[WARNING]\x1B[0m"
	CSVErrs = "\x1B[38;2;255;0;0m[ERROR]\x1B[0m"
	CSVnote = "\x1B[38;2;128;0;255m[NOTE]\x1B[0m"
	CSVmsgs = "\x1B[38;2;0;255;0m[MSG]\x1B[0m"
	CSVinfo = "\x1B[38;2;0;96;255m[INFO]\x1B[0m"
	#CSVcodestart = "\x1B[30m\x1B[47m "
	#CSVcodeends  = " \x1B[0m"
	CSVcodestart = "\x1B[30m\x1B[47m«"
	CSVcodeends  = "»\x1B[0m"
	CSVcodestart2 = "\x1B[30m\x1B[47m"
	CSVcodeends2  = "\x1B[0m"

	if len(sys.argv) < 2:
		print(f"{CSVtrad} {CSVErrs}: No function name was inputed!")
		return

	Argv = sys.argv
	if Argv[1].startswith('-'):
		if Argv[1] == "-h" or Argv[1] == "-help":
			print(f"{CSVtrad} {CSVinfo}: {CSVcodestart2}help.py{CSVcodeends2} does not requiere more than 1 argument.")
			print(f"{CSVtrad} {CSVnote}: All arguments after the first one will be ignored.")
			print(f"{CSVtrad} -- Available functions:")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.__init__(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.__del__(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.SetMode(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetMode(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetRow(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetRow2(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetCol(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetCol2(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetArray(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetArrayAt(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetRowHint(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetColHint(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetAmountOfRows(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.GetAmountOfCols(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.Help(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.SetFile(){CSVcodeends2}")
			print(f"\t{CSVinfo}: {CSVcodestart2}csv.Init(){CSVcodeends2}")
			return
		else:
			print(f"{CSVtrad} {CSVErrs}: unknown argument {CSVcodestart}{Argv[1]}{CSVcodeends}")
			return

	else:
		CSVtradf = "\x1B[1m"
		CSVWarnf = "\x1B[38;2;255;192;0m"
		CSVErrsf = "\x1B[38;2;255;0;0m"
		CSVnotef = "\x1B[38;2;128;0;255m"
		CSVmsgsf = "\x1B[38;2;0;255;0m"
		CSVinfof = "\x1B[38;2;0;96;255m"
		CSVf0    = "\x1B[0m"

		# file format:
		# `$t`: logo hint
		# `$e`: error hint
		# `$w`: warning hint
		# `$n`: note hint
		# `$m`: message hint
		# `$i`: info hint
		# `$B`: bold format
		# `$U`: underline format
		# `$I`: italic format
		# `$E`: error format
		# `$W`: warning format
		# `$N`: note format
		# `$M`: message format
		# `$0`: end format
		# `${`: code starts
		# `$}`: code ends
		# `$[`: code starts (2nd version)
		# `$]`: code ends (2nd version)

		HelpPage: str
		if Argv[1].startswith("__init__"):		HelpPage = "help/csv.__init__.csv-help"
		if Argv[1].startswith("__del__"):		HelpPage = "help/csv.__del__.csv-help"
		if Argv[1].startswith("SetMode"):		HelpPage = "help/csv.SetMode.csv-help"
		if Argv[1].startswith("GetMode"):		HelpPage = "help/csv.GetMode.csv-help"
		if Argv[1].startswith("GetRow"):		HelpPage = "help/csv.GetRow.csv-help"
		if Argv[1].startswith("GetRow2"):		HelpPage = "help/csv.GetRow2.csv-help"
		if Argv[1].startswith("GetCol"):		HelpPage = "help/csv.GetCol.csv-help"
		if Argv[1].startswith("GetCol2"):		HelpPage = "help/csv.GetCol2.csv-help"
		if Argv[1].startswith("GetArray"):		HelpPage = "help/csv.GetArray.csv-help"
		if Argv[1].startswith("GetArrayAt"):	HelpPage = "help/csv.GetArrayAt.csv-help"
		if Argv[1].startswith("GetRowHint"):	HelpPage = "help/csv.GetRowHint.csv-help"
		if Argv[1].startswith("GetColHint"):	HelpPage = "help/csv.GetColHint.csv-help"
		if Argv[1].startswith("GetAmountOfRows"):	HelpPage = "help/csv.GetAmountOfRows.csv-help"
		if Argv[1].startswith("GetAmountOfCols"):	HelpPage = "help/csv.GetAmountOfCols.csv-help"
		if Argv[1].startswith("Help"):		HelpPage = "help/csv.Help.csv-help"
		if Argv[1].startswith("SetFile"):		HelpPage = "help/csv.SetFile.csv-help"
		if Argv[1].startswith("Init"):		HelpPage = "help/csv.Init.csv-help"

		Page = open(HelpPage, 'r')
		Str = ''

		PageSize = os.path.getsize(HelpPage)
		Cn = 0
		while  Cn <= PageSize:
			C = Page.read(1)
			if C == '$':
				B = Page.read(1)
				if B == 't': Str += CSVtrad
				elif B == 'e': Str += CSVErrs
				elif B == 'w': Str += CSVWarn
				elif B == 'n': Str += CSVnote
				elif B == 'm': Str += CSVmsgs
				elif B == 'i': Str += CSVinfo
				elif B == 'B': Str += CSVtradf
				elif B == 'U': Str += "\x1B[4m"
				elif B == 'I': Str += CSVinfof
				elif B == 'E': Str += CSVErrsf
				elif B == 'W': Str += CSVWarnf
				elif B == 'N': Str += CSVnotef
				elif B == 'M': Str += CSVmsgsf
				elif B == '0': Str += CSVf0
				elif B == '{': Str += CSVcodestart
				elif B == '}': Str += CSVcodeends
				elif B == '[': Str += CSVcodestart2
				elif B == ']': Str += CSVcodeends2
				else:
					Str += C
					Str += B
			else: Str += C
			Cn += 1

		print(f"{CSVtrad} {CSVmsgs}: Opening manual {CSVcodestart2}{HelpPage}{CSVcodeends2}")
		print(Str)

if __name__ == "__main__":
	Help()