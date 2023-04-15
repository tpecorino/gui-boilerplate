import customtkinter


class ButtonListFrame(customtkinter.CTkFrame):
    def __init__(self, parent: any, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.buttons = []

    def add_item(self, user):
        button_attr_name = f"user_{user.id}_button"
        symbol_text = user.name

        setattr(self, button_attr_name,
                customtkinter.CTkButton(self,
                                        text=f"{symbol_text}", width=140))

        self.buttons.append(button_attr_name)

        getattr(self, button_attr_name).pack(padx=10, pady=10)

        if self.command is not None:
            getattr(self, button_attr_name).configure(
                command=lambda: self.command(user))
