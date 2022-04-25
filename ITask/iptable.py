class InnerPagesTable:
    # noinspection PyPep8Naming
    def __init__(self, Nf: int):
        self.Nf = Nf

        self.P = True  # в ОЗУ?
        self.A = False  # Обращались?
        self.D = True  # Модифицировали? True чтобы записалось в paging
