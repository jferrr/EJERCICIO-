from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

    @abstractmethod
    def handle(self, amount):
        pass


class BillHandler(Handler):
    def __init__(self, denomination):
        super().__init__()
        self.denomination = denomination

    def handle(self, amount):
        if amount >= self.denomination:
            num_bills = amount // self.denomination
            remaining_amount = amount % self.denomination
            print(f"Dispensando {num_bills} billetes de ${self.denomination}")
            if remaining_amount != 0 and self.next_handler:
                self.next_handler.handle(remaining_amount)
            elif remaining_amount != 0:
                print(f"Error: No se puede dispensar el monto restante de ${remaining_amount}.")
        else:
            if self.next_handler:
                self.next_handler.handle(amount)


class ATM:
    def __init__(self):
        self.bill_100000 = BillHandler(100000)
        self.bill_50000 = BillHandler(50000)
        self.bill_20000 = BillHandler(20000)
        self.bill_10000 = BillHandler(10000)
        self.bill_5000 = BillHandler(5000)

        self.bill_100000.set_next(self.bill_50000)
        self.bill_50000.set_next(self.bill_20000)
        self.bill_20000.set_next(self.bill_10000)
        self.bill_10000.set_next(self.bill_5000)

    def withdraw_money(self, amount):
        if amount % 5000 != 0:
            print("Error: El monto a retirar debe ser múltiplo de 5000.")
            return

        self.bill_100000.handle(amount)


def main():
    atm = ATM()
    
    while True:
        try:
            amount = int(input("Ingrese el monto que desea retirar: "))
            if amount <= 0:
                print("El monto debe ser mayor que 0.")
            else:
                atm.withdraw_money(amount)
                break
        except ValueError:
            print("Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()