import openpyxl

wb = openpyxl.load_workbook('ADM_TOTAL.xlsx')
ws = wb['744']

print(f'Dimensoes da aba 744: {ws.dimensions}')

total = 0
linhas = 0
for i, row in enumerate(ws.iter_rows(values_only=True), 1):
    if i == 1:
        print(f'Header: {row}')
        continue
    n = row[0]
    if n and isinstance(n, (int, float)):
        total += int(n) if isinstance(n, int) else int(n)
        linhas += 1
        if linhas <= 5:
            desc = row[1][:50] if len(row) > 1 and row[1] else ""
            print(f'{i}: {n} - {desc}')

print(f'\nTotal de linhas: {linhas}')
print(f'Total de aparelhos: {total:,}')
