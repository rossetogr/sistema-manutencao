def get_int_input(prompt, min_value=0):
    """Lê um inteiro do usuário, garantindo que é um número válido e maior ou igual a min_value."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"O valor deve ser maior ou igual a {min_value}.")
            else:
                return value
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def get_float_input(prompt, min_value=0):
    """Lê um número flutuante do usuário, garantindo que é um número válido e maior ou igual a min_value."""
    while True:
        try:
            # Substitui vírgulas por pontos para garantir a leitura correta de floats em diferentes locais
            raw_input = input(prompt).replace(',', '.')
            value = float(raw_input)
            if value < min_value:
                print(f"O valor deve ser maior ou igual a {min_value}.")
            else:
                return value
        except ValueError:
            print("Entrada inválida. Por favor, digite um número (ex: 75.5).")