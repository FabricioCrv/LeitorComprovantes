from findElements import lerpdf, findDate, findPrice, findName
import csv
import xlsxwriter
import openpyxl

def print_comprovantes():
    for file_name in range(1, 100):
        try:
            text_list = lerpdf(str(file_name) + ".pdf")
            date = findDate(text_list, "2023")
            print(date)
            price = findPrice(text_list)
            print(price)
            name = findName(text_list)
            print(name)
            print("Documento " + str(file_name))
            print('_' * 10)
        except:
            if False:
                print()
    return comprovante

def read_comprovante():
    comprovante = [['DATA DO PAGAMENTO', 'VALOR', 'RAZÃO DA CONTA']]
    print(comprovante[0])
    for file_name in range(1, 100):
        try:
            text_list = lerpdf(str(file_name) + ".pdf")
            date = findDate(text_list, "2023")
            price = findPrice(text_list)
            name = findName(text_list)
            line = [date, price, name]
            print(line)
            comprovante.append(line)
        except:
            if False:
                print()

    return comprovante

def create_csv(file_name, sheet):
    with open(file_name + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sheet)


def create_xlsx(sheet, file_name, max_column, max_row):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(file_name + '.xlsx')
    worksheet = workbook.add_worksheet()

    # Iterate over the data and write it out row by row.
    for col in range(0, max_column):
        for row in range(0, max_row):
            worksheet.write(row, col, sheet[row][col])

    workbook.close()

def read_template(comprovante, template_doc, max_col, max_line):
    wb_obj = openpyxl.load_workbook(template_doc + ".xlsx")
    sheet = wb_obj.active
    this_line = []
    template = []
    for line in range(1, max_line + 1):
        for col in range(1, max_col + 1):
            cell = sheet.cell(row=line, column=col)
            if cell.value == None:
                cell.value = ""
            this_line.append(cell.value)
        print(this_line)
        template.append(this_line)
        this_line = []
    return template

if __name__ == '__main__':
    comprovante = print_comprovantes()
    #comprovante = read_comprovante()
    #template = read_template('', 'template', 10, 43)
    #create_csv("comprovante", comprovante)
    #create_xlsx(comprovante, "comprovante", 3, 60 + 1)
    #create_xlsx(template, 'template2', 10, 43)
