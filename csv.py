from typing import overload
import colorama
import os

class csv():
	def __init__(self, FilePath=''):
		# Initlaise feature to color text in STDOUT
		colorama.init()

		# Sets basic information strings
		self.CSVtrad = "\x1B[1mCSV\x1B[0m"
		self.CSVWarn = "\x1B[38;2;255;192;0m[WARNING]\x1B[0m"
		self.CSVErrs = "\x1B[38;2;255;0;0m[ERROR]\x1B[0m"
		self.CSVnote = "\x1B[38;2;128;0;255m[NOTE]\x1B[0m"
		self.CSVmsgs = "\x1B[38;2;0;255;0m[MSG]\x1B[0m"
		self.CSVinfo = "\x1B[38;2;0;96;255m[INFO]\x1B[0m"
		#self.CSVcodestart = "\x1B[30m\x1B[47m "
		#self.CSVcodeends  = " \x1B[0m"
		self.CSVcodestart = "\x1B[30m\x1B[47m«"
		self.CSVcodeends  = "»\x1B[0m"

		# Variables
		self.FPath = FilePath
		self.FileOpen = False
		self.TableName = ''

		self.Separator			= ','
		self.HintTag			= '%'
		self.Directive			= '#'
		self.EvalMode			= 1
		self.IgnoreWhiteSpaces		= True
		self.IgnoreSpaces		= True
		self.IgnoreTabs			= True
		self.EndOfRowIsSemiColomn	= False
		self.AllQuoted			= False
		self.QuoteTextOnly		= True

		self.RowCurrent= 0
		self.ColCurrent= 0

		if len(FilePath) < 1:
			print(f"{self.CSVtrad} {self.CSVWarn}: no file was given.")
			print(f"{self.CSVtrad} {self.CSVnote}: you can use {self.CSVcodestart}csv.SetFile(<file_path>){self.CSVcodeends} to open a/another file")
			return
		# Lookup file
		if os.path.isfile(FilePath) == False:
			print(f"{self.CSVtrad} {self.CSVErrs}: file '{FilePath}' does not exist.")
			return
		if FilePath.endswith(".csv") == False:
			print(f"{self.CSVtrad} {self.CSVWarn}: file '{FilePath}' may not be a CSV file.")
		self.File = open(FilePath, "r+")
		self.FileOpen = True

		return

	def __del__(self):
		# Closing file (if open)
		if self.FileOpen == True: self.File.close()
		print(f"{self.CSVtrad} {self.CSVmsgs}: Ending operations with file {self.CSVcodestart}{self.FPath}{self.CSVcodeends}.")
		return

	def SetFile(self, FilePath: str):
		if len(FilePath) < 1: return
		# Lookup file
		if os.path.isfile(FilePath) == False:
			print(f"{self.CSVtrad} {self.CSVErrs}: file '{FilePath}' does not exist.")
			return
		if FilePath.endswith(".csv") == False:
			print(f"{self.CSVtrad} {self.CSVWarn}: file '{FilePath}' may not be a CSV file.")

		if self.FileOpen:
			self.File.close()

		self.File = open(FilePath, "r+")
		self.FPath = FilePath

	def Init(self):
		if not self.FileOpen:
			print(f"{self.CSVtrad} {self.CSVErrs}: No file were given, nothing to do!")
			print(f"{self.CSVtrad} {self.CSVinfo}: You can precise a file to open using {self.CSVcodestart}csv.SetFile(<file_path>{self.CSVcodeends})")
			return
		Line = self.File.readline()
		L = 0
		while len(Line) >= 1:
			Line = self.File.readline()
			if self.EndOfRowIsSemiColomn and Line.find(';') == -1:
				print(f"{self.CSVtrad} {self.CSVErrs}: Line {L} does not end with a semi-column, but {self.CSVcodestart}EndOfRowIsSemiColomn{self.CSVcodeends} parameter is set to {self.CSVcodestart}True{self.CSVcodeends}!")
				print(f"{self.CSVtrad} {self.CSVnote}: If you wish to disable this parameter use {self.CSVcodestart}csv.SetMode(EndOfRowIsSemiColomn=False){self.CSVcodeends}.")
				return
			if Line.startswith(self.Directive):
				Line.lstrip(self.Directive)
				if Line.startswith("set-hint-tag "):
					Line.lstrip("set-hint-tag ")
					self.SetMode(HintTag=Line[0])
				if Line.startswith("name "):
					Line.lstrip("name ")
					NEnd = (Line.find(' ') if Line.find(' ') != -1 else
						Line.find(';') if self.EndOfRowIsSemiColomn and Line.find(';') != -1 else
						len(Line))
					for i in range(NEnd):
						self.Name += Line[i]
				continue

			if Line.startswith(self.HintTag):
				Line.lstrip(self.HintTag)
				continue
			L += 1
		return

	def SetMode(
		self,
		Separator=',',
		HintTag='%',
		Directive='#',
		EvalMod=1,
		IgnoreWhiteSpaces=True,
		IgnoreSpaces=True,
		IgnoreTabs=True,
		EndOfRowIsSemiColomn=False,
		AllQuoted=False,
		QuoteTextOnly=True
	):
		"""
		Allows the user to set the evaluation mod of the CSV file:

		- `Separator`: change separator (default: `,`) ; Cannot be set to `;` if `EndOfRowIsSemiColomn` is set to `True`,
		- `HintTag`: specifies the hint tag (default: `%`),
		- `Directive`: directive that can be used inside a CSV (default: `#`),
		- `EvalMod`: Specify operation mod, if 1: Standard, if 2: Line-per-line (French),
		- `IgnoreWhiteSpaces`: sets the evaluation mode for white spaces (spaces and tabs) (default: `True`),
		- `IgnoreSpaces`: sets the evaluation mode for spaces (default: `True`),
		- `IgnoreTabs`: sets the evaluation mode for tabulations (default: `True`),
		- `EndOfRowIsSemiColomn`: sets the EOL rule, true: must end with a semi-colomn ; false: EOL only (default: `False`);
		if true this option can't be used with the separator set to ';',
		- `AllQuoted`: sets the value rule, true: all value must be surrounded by double quotes (default: `False`);
		if false: then all the values are processed as strings
		- `QuoteTextOnly`: set the valeu rule, true: strings must be surrounded by string(default: `True`);
		conflict with `AllQuoted` if it is set to `True`.
		"""
		# Problem variables
		PbSep = False
		PbQut = False
		PbEOL = False
		PbIng = False
		PbHnt = False
		PbDrc = False

		if Separator == None: self.Separator = ','
		elif len(Separator) > 1:
			print(f"{self.CSVtrad} {self.CSVErrs}: Separator must \x1B[1mONE\x1B[0m character!")
			PbSep = True
		else:
			if Separator == ';' and EndOfRowIsSemiColomn == True:
				print(f"{self.CSVtrad} {self.CSVWarn}: Separator set as {self.CSVcodestart};{self.CSVcodeends} (semi-colomn) is incompatible with required semi-colomn at EOL!")
				PbSep = True
				PbEOL = True

			if Separator == '\n':
				print(f"{self.CSVtrad} {self.CSVWarn}: Separator can't be EOL!")
				PbSep = True
			if Separator == '"' or Separator == '\'':
				print(f"{self.CSVtrad} {self.CSVWarn}: Separator cannot be {self.CSVcodestart}'{self.CSVcodeends} or {self.CSVcodestart}\"{self.CSVcodeends} because is an operator!")
				PbSep = True
			if Separator == '\t' and IgnoreTabs == False:
				print(f"{self.CSVtrad} {self.CSVWarn}: Separator cannot be {self.CSVcodestart}\\t{self.CSVcodeends} if tabs are not ignored!")
				PbSep = True
			if Separator == ' ' and IgnoreSpaces == False:
				print(f"{self.CSVtrad} {self.CSVWarn}: Separator cannot be {self.CSVcodestart}` `{self.CSVcodeends} if spaces are not ignored!")
				PbSep = True
			if (
				HintTag == ' ' or HintTag == '\n' or HintTag == '\t' or
				(HintTag == ';' and (self.EndOfRowIsSemiColomn == True or EndOfRowIsSemiColomn == True)) or
				(HintTag == Separator or HintTag == self.Separator) or
				(HintTag == Directive or HintTag == self.Directive) or
				HintTag == '"' or HintTag == '\''
			):
				print(f"{self.CSVtrad} {self.CSVWarn}: Conflict between given {self.CSVcodestart}HintTag{self.CSVcodeends} and other parameter(s)!")
				PbHnt = True
			if (
				Directive == ' ' or Directive == '\n' or Directive == '\t' or
				(Directive == ';' and (self.EndOfRowIsSemiColomn == True or EndOfRowIsSemiColomn == Ture)) or
				(Directive == Separator or Directive == self.Separator) or
				(Directive == Separator or Directive == self.Separator) or
				Directive == '"' or Directive == '\''
			):
				print(f"{self.CSVtrad} {self.CSVWarn}: Conflict between given {self.CSVcodestart}Directive{self.CSVcodeends} and other parameter(s)!")
				PbDrc = True
		if IgnoreSpaces == True or IgnoreTabs == True: self.IgnoreWhiteSpaces = True

		if AllQuoted == True and QuoteTextOnly == True:
			print(f"{self.CSVtrad} {self.CSVWarn}: Conflict between parameter {self.CSVcodestart}AllQuoted{self.CSVcodeends} and {self.CSVcodestart}QuoteTextOnly{self.CSVcodeends}!")
			PbQut = True


		if Separator == ';' and self.EndOfRowIsSemiColomn == True:
			print(f"{self.CSVtrad} {self.CSVWarn}: Separator set as {self.CSVcodestart};{self.CSVcodeends} (semi-colomn) is incompatible with required semi-colomn at EOL!")
			PbSep = True
		if self.Separator == ';' and EndOfRowIsSemiColomn == True:
			print(f"{self.CSVtrad} {self.CSVWarn}: Separator set as {self.CSVcodestart};{self.CSVcodeends} (semi-colomn) is incompatible with required semi-colomn at EOL!")
			PbEOL = True


		if Separator == '\t' and self.IgnoreTabs == False:
			print(f"{self.CSVtrad} {self.CSVWarn}: Separator cannot be {self.CSVcodestart}\\t{self.CSVcodeends} if tabs are not ignored!")
			PbSep = True
		if Separator == ' ' and self.IgnoreSpaces == False:
			print(f"{self.CSVtrad} {self.CSVWarn}: Separator cannot be {self.CSVcodestart}` `{self.CSVcodeends} if spaces are not ignored!")
			PbSep = True

		if self.Separator == '\t' and IgnoreTabs == False:
			print(f"{self.CSVtrad} {self.CSVWarn}: Separator cannot be {self.CSVcodestart}\\t{self.CSVcodeends} if tabs are not ignored!")
			PbIng = True
		if self.Separator == ' ' and IgnoreSpaces == False:
			print(f"{self.CSVtrad} {self.CSVWarn}: Separator cannot be {self.CSVcodestart}` `{self.CSVcodeends} if spaces are not ignored!")
			PbIng = True


		if AllQuoted == True and QuoteTextOnly == True:
			print(f"{self.CSVtrad} {self.CSVWarn}: Conflict between parameter {self.CSVcodestart}AllQuoted{self.CSVcodeends} and {self.CSVcodestart}QuoteTextOnly{self.CSVcodeends}!")
			PbQut = True

		if PbSep == False: self.Separator		= Separator
		if PbEOL == False: self.EndOfRowIsSemiColomn	= EndOfRowIsSemiColomn

		if PbQut == False: self.AllQuoted		= AllQuoted
		if PbQut == False: self.QuoteTextOnly		= QuoteTextOnly

		if PbIng == False: self.IgnoreWhiteSpaces	= IgnoreWhiteSpaces
		if PbIng == False: self.IgnoreSpaces		= IgnoreSpaces
		if PbIng == False: self.IgnoreTabs		= IgnoreTabs

		if PbHnt == False: self.HintTag			= HintTag
		if PbDrc == False: self.Directive		= Directive

		if EvalMod == 1 or EvalMod == 2:
			self.EvalMode = EvalMod

	def GetMode(self):
		print(f"{self.CSVtrad} {self.CSVinfo}: Separator is {self.CSVcodestart}{self.Separator}{self.CSVcodeends}.")
		print(f"{self.CSVtrad} {self.CSVinfo}: White spaces evaluation is set to {self.CSVcodestart}{not self.IgnoreWhiteSpaces}{self.CSVcodeends}.")
		print(f"{self.CSVtrad} {self.CSVinfo}: Space character evaluation is set to {self.CSVcodestart}{not self.IgnoreSpaces}{self.CSVcodeends}.")
		print(f"{self.CSVtrad} {self.CSVinfo}: Tab character evaluation is set to {self.CSVcodestart}{not self.IgnoreTabs}{self.CSVcodeends}.")
		print(f"{self.CSVtrad} {self.CSVinfo}: {self.CSVcodestart}EOL == ';'{self.CSVcodeends} is set to {self.CSVcodestart}{self.EndOfRowIsSemiColomn}{self.CSVcodeends}.")
		if self.AllQuoted == True and self.QuoteTextOnly == True:
			print(f"{self.CSVtrad} {self.CSVinfo}: Quotes are evaluated for no objects.")
		elif self.AllQuoted == True:
			print(f"{self.CSVtrad} {self.CSVinfo}: Quotes are evaluated for text only (strings).")
		else:
			print(f"{self.CSVtrad} {self.CSVinfo}: Quotes are evaluated for all objects.")

	def GetRow(self):
		return
	def GetRow2(self, Row: int):
		return

	def GetCol(self):
		return
	def GetCol2(self, Col: int):
		return


	def GetArray(self):
		return
	def GetArrayAt(self, RowStart: int, ColStart: int, RowEnd: int, ColEnd: int):
		return

	def GetRowHint(self):
		if os.path.getsize(self.FPath) < 1:
			print(f"{self.CSVtrad} {self.CSVErrs}: File {self.FPath} is empty!")
			return

		self.File.seek(0)
		Str: str = ''
		L = 0
		Ls = []

		while len(Str) < 1:
			L += 1
			Str = self.File.readline()

		if self.EndOfRowIsSemiColomn == True and Str.endswith(';') != True:
			print(f"{self.CSVtrad} {self.CSVErrs}: Line {L} does not ends with a semi-coloms (';')!")
			print(f"{self.CSVtrad} {self.CSVnote}: if you wish to not use this feature, use {self.CSVcodestart}CSV.SetMode(EndOfRowIsSemiColomn=False){self.CSVcodeends}.")
			return None

		TS = Str[0]
		for i in range(1, len(Str)):
			if (Str[i] == ' ' or Str[i] == '\t') and self.IgnoreWhiteSpaces == False:
				print(f"{self.CSVtrad} {self.CSVErrs}: Invalid character at line {L} in file {self.FPath}, position {i}!")
				print(f"{self.CSVtrad} {self.CSVnote}: If you wish to ignore white spaces use {self.CSVcodestart}CSV.SetMode(IgnoreWhiteSpaces=Ture){self.CSVcodeends}.")
			elif Str[i] == ' ' or Str[i] == '\t':
				continue
			else:
				if Str[i] == ';' and self.EndOfRowIsSemiColomn == True:
					break
				if (Str[i] != self.Separator):
					TS += Str[i]
				else:
					Ls.append(TS)
					TS = ''
					continue
				if i == len(Str):
					break
		Ls.append(TS)
		return Ls

	def GetColHint(self):
		return


	def GetAmountOfRows(self):
		return
	def GetAmountOfCols(self):
		return


	def Help(Func=''):
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

		if len(Func) < 1:
			print(f"{CSVtrad} {CSVErrs}: No function name were inputed.")
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
		if Func.startswith("__init__"):		HelpPage = "help/csv.__init__.csv-help"
		if Func.startswith("__del__"):		HelpPage = "help/csv.__del__.csv-help"
		if Func.startswith("SetMode"):		HelpPage = "help/csv.SetMode.csv-help"
		if Func.startswith("GetMode"):		HelpPage = "help/csv.GetMode.csv-help"
		if Func.startswith("GetRow"):		HelpPage = "help/csv.GetRow.csv-help"
		if Func.startswith("GetRow2"):		HelpPage = "help/csv.GetRow2.csv-help"
		if Func.startswith("GetCol"):		HelpPage = "help/csv.GetCol.csv-help"
		if Func.startswith("GetCol2"):		HelpPage = "help/csv.GetCol2.csv-help"
		if Func.startswith("GetArray"):		HelpPage = "help/csv.GetArray.csv-help"
		if Func.startswith("GetArrayAt"):	HelpPage = "help/csv.GetArrayAt.csv-help"
		if Func.startswith("GetRowHint"):	HelpPage = "help/csv.GetRowHint.csv-help"
		if Func.startswith("GetColHint"):	HelpPage = "help/csv.GetColHint.csv-help"
		if Func.startswith("GetAmountOfRows"):	HelpPage = "help/csv.GetAmountOfRows.csv-help"
		if Func.startswith("GetAmountOfCols"):	HelpPage = "help/csv.GetAmountOfCols.csv-help"
		if Func.startswith("Help"):		HelpPage = "help/csv.Help.csv-help"
		if Func.startswith("SetFile"):		HelpPage = "help/csv.SetFile.csv-help"
		if Func.startswith("Init"):		HelpPage = "help/csv.Init.csv-help"

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

