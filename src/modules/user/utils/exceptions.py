class CanNotSendEmailError(Exception):
    def __init__(self, to: str) -> None:
        super().__init__(f"No se pudo enviar el correo a {to}")
