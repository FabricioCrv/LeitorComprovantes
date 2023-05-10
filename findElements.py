from PyPDF2 import PdfReader

def insertString(string, position, character):
    array = string[:position] + character + string[position:]
    return array


def lerpdf(file_name):
    reader = PdfReader(file_name)
    page = reader.pages[0]
    text = page.extract_text()
    # print(text)
    # print("_" * 10)
    text_list = text.split("\n")
    return text_list


def findDate(text_file, year):
    date = ""
    for contador in range(0, len(text_file)):
        if ("/" + year) in text_file[contador]:
            date_line = text_file[contador]
            date_list = date_line.split(" ")
            for count in range(0, len(date_list)):
                if ("/" + year) in date_list[count]:
                    date = date_list[count]
    if "em" in date:
        date = date.replace("em", "")

    return date


def findPrice(text_file):
    price = ""
    price_full = False
    for contador in range(0, len(text_file)):
        if ("R$") in text_file[contador]:
            price_line = text_file[contador]
            cifrao = price_line.index("$")
            count = int(cifrao)
            while (count < len(price_line)):
                # caso venham dois boletos no mesmo documento
                if price_full != False:
                    count = len(price_line)
                elif price_line[count].isnumeric():
                    price = price + price_line[count]
                elif price_line[count].isalpha():
                    count = len(price_line)
                count += 1
                if count == len(price_line):
                    price_full = True
        if ("valor: " in text_file[contador]):
            if ("R$") in text_file[contador]:
                break
            else:
                price_line = text_file[contador]
                valor = price_line.index("valor: ") + 7
                count = int(valor)
                while (count < len(price_line)):
                    # caso venham dois boletos no mesmo documento
                    if price_full != False:
                        count = len(price_line)
                    elif price_line[count].isnumeric():
                        price = price + price_line[count]
                    elif price_line[count].isalpha():
                        count = len(price_line)
                    count += 1
                    if count == len(price_line):
                        price_full = True
        if "Valor do boleto" in text_file[contador]:
            price = text_file[contador + 1]
            price = price.replace(",", "")

    if price == "":
        for count in range(0, len(text_file)):
            if "valor" in text_file[count]:
                price = text_file[count][:text_file[count].index("valor")]
                if "pagamento efetuado em" in price:
                    price = price[price.index("pagamento efetuado em") + 21:]
                price = price.replace(".", "")

    price = price.strip()
    if ((len(price) > 5) & ("." not in price)):
        price = insertString(price, len(price) - 5, ".")
    price = insertString(price, (len(price) - 2), ",")
    price = insertString(price, 0, "R$ ")

    return price


def findName(text_file):
    name = ""
    nome_do_pagador = ""
    nome_do_recebedor = ""
    proxima_linha = ""

    if "-" in text_file[1]:
        name = text_file[1][text_file[1].index("-") + 1:]
        name = name.lstrip()
    # caso TED
    if "TED" in text_file[0]:
        name = text_file[1]

    for contador in range(0, len(text_file)):
        if "nome" in text_file[contador]:
            if name == "":
                name_line = text_file[contador]
                name = name_line.replace("nome ", "")
                name = name_line.replace("nome:", "")
            if "nome do recebedor" in text_file[contador]:
                name = text_file[contador][19:]
        if "nome do pagador" in text_file[contador]:
            nome_do_pagador = text_file[contador]
            proxima_linha = text_file[contador + 1]
        if "nome do recebedor" in text_file[contador]:
            nome_do_recebedor = text_file[contador][text_file[contador].index("nome do recebedor") + 19:]
        if "Identificação no extrato: " in text_file[contador]:
            name = text_file[contador][text_file[contador].index("Identificação no extrato: ") + 26:]
        if "Nome Favorecido: " in text_file[contador]:
            name = text_file[contador][text_file[contador].index("Nome Favorecido: ") + 17:]
        if "nome do favorecido" in text_file[contador]:
            name = text_file[contador + 1]
        if "Nome do favorecido:" in text_file[contador]:
            name = text_file[contador][text_file[contador].index("Nome do favorecido:") + 19:]
        if "JRnome" in text_file[contador]:
            proxima_linha = text_file[contador + 1]
            if "data de pagamento" in proxima_linha:
                name = proxima_linha[proxima_linha.index("data de pagamento") + 17:]
                if "empresa" in text_file[contador + 2]:
                    name = name + text_file[contador + 2][:text_file[contador + 2].index("empresa")]
        if "agente arrecadadoremitido" in text_file[contador]:
            for contador in range(0, len(text_file)):
                if "código de barras" in text_file[contador]:
                    name = text_file[contador][text_file[contador].index("código de barras") + 16:]
        if "valor transferido via Pix" in text_file[contador]:
            count = contador + 1
            while (count < len(text_file)):
                if "par" in text_file[count]:
                    name = text_file[count + 1]
                    if "Bco" in text_file[count + 3]:
                        name = name + text_file[count + 2]
                    count = len(text_file)
                    while ("  " in name):
                        name = name.replace("  ", " ")
                    name = name.replace("•", "")
                else:
                    count += 1

    name = name.strip()

    if nome_do_pagador != "":
        name = nome_do_pagador[nome_do_pagador.index("nome do pagador") + 15:]
        if "raz" in proxima_linha:
            name = name + proxima_linha[:proxima_linha.index("raz")]
    if len(name) > 0:
        if name[0].isnumeric():
            if "final" in proxima_linha:
                name = proxima_linha[proxima_linha.index("final") + 5:]
    if len(nome_do_recebedor) > 0:
        name = nome_do_recebedor
    if "nome " in name:
        name = name.replace("nome ", "")
    if "da concessionária: " in name:
        name = name.replace("da concessionária: ", "")
    if "conta:agência:" in name:
        name = text_file[1]
    if "nomeemitido" in name:
        for contador in range(0, len(text_file)):
            if "data de pagamento" in text_file[contador]:
                name_line = text_file[contador]
                name = name_line[name_line.index("data de pagamento") + 17:]
                if "empresa" in name:
                    name = name[:name.index("empresa")]
                    name = name.strip()
                if "empresa" in text_file[contador + 1]:
                    name = name + text_file[contador + 1][:text_file[contador + 1].index("empresa")]
    if "da empresa: " in name:
        for contador in range(0, len(text_file)):
            if "descrição: " in text_file[contador]:
                name = text_file[contador][text_file[contador].index("descrição: ") + 11:]

    if name == "":
        for contador in range(0, len(text_file)):
            if "tipo de pagamento: " in text_file[contador]:
                name = text_file[contador][text_file[contador].index("tipo de pagamento: ") + 19:]
            if text_file[contador] == "para  ":
                name = text_file[contador + 1] + text_file[contador + 2]
                while ("  " in name):
                    name = name.replace("  ", " ")
            if "Beneficiário:" in text_file[contador]:
                name = text_file[contador][
                       text_file[contador].index("Beneficiário:") + 13: text_file[contador].index("CPF/CNPJ")]
                name = name.strip()

    if name == "  ":
        for contador in range(0, len(text_file)):
            if "nome do recebedor" in text_file[contador]:
                name = text_file[contador + 1]
    if name[0].isnumeric():
        found_Comprovante = False
        for contador in range(0, len(text_file)):
            if (("Comprovante" in text_file[contador]) & (found_Comprovante == False)):
                name = text_file[contador][text_file[contador].index("Comprovante") + 11:]
                name = name.strip()
                found_Comprovante = True

    if name[0].isnumeric():
        for contador in range(0, len(text_file)):
            if "CNPJ do beneficiário final" in text_file[contador]:
                name = text_file[contador][text_file[contador].index("CNPJ do beneficiário final") + 26:]
    name = name.strip()

    return name