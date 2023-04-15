import customtkinter
import database
from widgets import SearchFrame, ButtonListFrame


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("500x500")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.session = database.get_database_session()

        self.search_frame = SearchFrame(self, command=self.handle_search)
        self.search_frame.pack()

        self.button_list = ButtonListFrame(self,
                                           command=self.handle_button_click)
        self.button_list.pack()

    def run(self):
        self.create_stock_buttons()
        self.mainloop()

    def on_closing(self, event=0):
        self.destroy()

    def create_stock_buttons(self):
        characters = database.fetch_characters(self.session)

        for character in characters:
            self.button_list.add_item(character)

    def handle_button_click(self, character):
        print(f"label button frame clicked: {character}")

    def handle_search(self, event=0):
        print(self.search_frame.entry.get())


if __name__ == "__main__":
    app = App()
    app.run()
