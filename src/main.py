from services.sheets.googlesheets_reader import GoogleSheet


gs = GoogleSheet()
df = gs.convert_sheet_to_pandas('Test', 'B2:C10')
df.to_excel('a.xlsx')
