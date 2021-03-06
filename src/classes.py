class Contract:
    def __init__(self):
        self.Products = []
        self.Customer = Customer()
        self.Supplier = Supplier()
        self.Execution = Execution()
        self.Currency = Currency()
        self.Price = 'None'
        self.SignDate = 'None'
        self.id = 'None'
        self.RegNum = 'None'
        self.PublishDate = 'None'
        self.Price = 'None'
        self.Number = 'None'
        self.NotNumber = 'None'
        self.ProtocolDate = 'None'
        self.DocumentBase = 'None'
        self.Region = 'None'

class Customer:
    def __init__(self):
        self.inn = 'None'
        self.kpp = 'None'
        self.FullName = 'None'
        self.RegNum = 'None'

class Supplier:
    def __init__(self):
        self.inn = 'None'
        self.kpp = 'None'
        self.OrgName = 'None'
        self.CountryName = 'None'
        self.FactAddress = 'None'
        self.ContactInfo = 'None'
        self.ContactPhone = 'None'

class Product:
    def __init__(self):
        self.Name = 'None'
        self.Sid = 'None'
        self.Price = 'None'
        self.Code = 'None'

class Execution:
    def __init__(self):
        self.Month = 'None'
        self.Year = 'None'

class Currency:
    def __init__(self):
        self.Code = 'None'
        self.Name = 'None'