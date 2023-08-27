import customtkinter


class ButtonListFrame(customtkinter.CTkFrame):
    def __init__(self, parent: any, gen_command=None, edit_command=None, delete_command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.gen_command = gen_command
        self.edit_command = edit_command
        self.delete_command = delete_command
        self.labels = []
        self.gen_buttons = []
        self.edit_buttons = []
        self.delete_buttons = []
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

    def update_item(self, graph):
        label_attr_name = f"item_{graph['id']}_label"
        getattr(self, label_attr_name).configure(text=graph['title'])

    def add_item(self, item):
        label_attr_name = f"item_{item.id}_label"
        gen_button_attr_name = f"gen_{item.id}_button"
        edit_button_attr_name = f"edit_{item.id}_button"
        delete_button_attr_name = f"delete_{item.id}_button"
        symbol_text = item.title

        setattr(self, label_attr_name, customtkinter.CTkLabel(self, text=symbol_text, width=100))
        setattr(self, gen_button_attr_name,
                customtkinter.CTkButton(self, text="Generate", width=50, fg_color="green"))
        setattr(self, edit_button_attr_name,
                customtkinter.CTkButton(self, text="Edit", width=50))
        setattr(self, delete_button_attr_name,
                customtkinter.CTkButton(self, text="Delete", width=50, fg_color="red"))

        self.labels.append(label_attr_name)
        self.gen_buttons.append(gen_button_attr_name)
        self.edit_buttons.append(edit_button_attr_name)
        self.delete_buttons.append(delete_button_attr_name)

        getattr(self, label_attr_name).grid(row=item.id, column=0, padx=0, pady=10, sticky="ew")
        getattr(self, gen_button_attr_name).grid(row=item.id, column=1, padx=10, pady=10, sticky="e")
        getattr(self, edit_button_attr_name).grid(row=item.id, column=2, padx=10, pady=10, sticky="e")
        getattr(self, delete_button_attr_name).grid(row=item.id, column=3, padx=10, pady=10, sticky="e")

        if self.edit_command and self.delete_command is not None:
            getattr(self, gen_button_attr_name).configure(
                command=lambda: self.gen_command(item))
            getattr(self, edit_button_attr_name).configure(
                command=lambda: self.edit_command(item))
            getattr(self, delete_button_attr_name).configure(
                command=lambda: self.delete_command(item))

    def remove_item(self, item):
        label_attr_name = f"item_{item.id}_label"
        gen_button_attr_name = f"gen_{item.id}_button"
        edit_button_attr_name = f"edit_{item.id}_button"
        delete_button_attr_name = f"delete_{item.id}_button"
        self.labels.remove(label_attr_name)
        self.gen_buttons.remove(gen_button_attr_name)
        self.edit_buttons.remove(edit_button_attr_name)
        self.delete_buttons.remove(delete_button_attr_name)
        getattr(self, label_attr_name).destroy()
        getattr(self, gen_button_attr_name).destroy()
        getattr(self, edit_button_attr_name).destroy()
        getattr(self, delete_button_attr_name).destroy()
