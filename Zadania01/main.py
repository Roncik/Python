
class Kategoria:
    nazwa = ""
    id = ""

class Produkt:
    nazwa = ""
    kategoria = Kategoria
    cena_netto = 0.0
    stawka_vat = 0.0
    ilosc = 0
    sku = ""

class Klient:
    id = ""
    poziom_lojalnosciowy = 0

class Promocja_kategoria:
    