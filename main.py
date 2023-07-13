import customtkinter
from data import database
from widgets import ButtonListFrame
from util import graph_generator


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graphs = []
        self.geometry("500x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.session = database.get_database_session()
        self.update_view = True

        # Frames
        self.graph_form_frame = customtkinter.CTkFrame(self)
        self.graph_form_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="new")

        self.graph_list_frame = customtkinter.CTkFrame(self)
        self.graph_list_frame.columnconfigure(0, weight=1)
        self.graph_list_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="new")

        # create main entry and button
        self.graph_title_entry = customtkinter.CTkEntry(self.graph_form_frame, placeholder_text="Title")
        self.graph_title_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="new")

        self.x_axis_label_entry = customtkinter.CTkEntry(self.graph_form_frame, placeholder_text="X Axis Label")
        self.x_axis_label_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nw")

        self.x_axis_values_entry = customtkinter.CTkEntry(self.graph_form_frame, placeholder_text="Jan Feb Mar Apr...")
        self.x_axis_values_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="new")

        self.y_axis_label_entry = customtkinter.CTkEntry(self.graph_form_frame, placeholder_text="Y Axis Label")
        self.y_axis_label_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nw")

        self.y_axis_values_entry = customtkinter.CTkEntry(self.graph_form_frame, placeholder_text="100 200 300 400...")
        self.y_axis_values_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="new")

        self.graph_form_submit_btn = customtkinter.CTkButton(self.graph_form_frame, text="Save",
                                                             command=self.handle_save)
        self.graph_form_submit_btn.grid(row=3, column=0, padx=10, pady=5, sticky="new")

        self.graph_form_submit_btn = customtkinter.CTkButton(self.graph_form_frame, text="Clear",
                                                             command=self.clear_form)
        self.graph_form_submit_btn.grid(row=3, column=1, padx=10, pady=5, sticky="new")

        self.button_list = ButtonListFrame(self.graph_list_frame, gen_command=self.generate_graph,
                                           edit_command=self.edit_graph,
                                           delete_command=self.delete_graph)
        self.button_list.grid(row=1, column=0, pady=0, sticky="new")

    def run(self):
        self.load_graphs()
        self.mainloop()

    def on_closing(self, event=0):
        self.destroy()

    def load_graphs(self):
        self.graphs = database.fetch_graphs(self.session)

        for graph in self.graphs:
            self.button_list.add_item(graph)

    def generate_graph(self, graph):
        x_label = graph.x_axis_label
        y_label = graph.y_axis_label
        x_values = graph.x_axis_values.split()
        y_values = list(map(int, graph.y_axis_values.split()))
        graph_generator.generate_line_graph(x_label, y_label, x_values, y_values)

        print(f"Generate: {graph}")

    def edit_graph(self, item):
        for widget in filter(lambda w: isinstance(w, customtkinter.CTkEntry),
                             self.graph_form_frame.children.values()):
            widget.delete(0, customtkinter.END)
        self.graph_title_entry.insert(customtkinter.END, item.title)
        self.x_axis_label_entry.insert(customtkinter.END, item.x_axis_label)
        self.y_axis_label_entry.insert(customtkinter.END, item.y_axis_label)
        self.x_axis_values_entry.insert(customtkinter.END, item.x_axis_values)
        self.y_axis_values_entry.insert(customtkinter.END, item.y_axis_values)
        print(f"Edit: {item}")

    def delete_graph(self, graph):
        database.delete_graph(self.session, graph.id)
        self.button_list.remove_item(graph)
        print(f"Delete: {graph}")

    def update_graph_list(self, graph):
        if self.update_view:
            self.button_list.add_item(graph)
            self.update_view = False

    def handle_save(self, event=0):
        title = self.graph_title_entry.get()
        x_axis_label = self.x_axis_label_entry.get()
        y_axis_label = self.y_axis_label_entry.get()
        x_axis_values = self.x_axis_values_entry.get()
        y_axis_values = self.y_axis_values_entry.get()

        graph = {
            "title": title,
            "x_axis_label": x_axis_label,
            "y_axis_label": y_axis_label,
            "x_axis_values": x_axis_values,
            "y_axis_values": y_axis_values
        }

        result = database.save_graph(self.session, graph)
        print('result', result)
        self.graphs.append(graph)
        self.clear_form()
        self.update_view = True
        self.update_graph_list(result)

    def clear_form(self):
        for widget in filter(lambda w: isinstance(w, customtkinter.CTkEntry),
                             self.graph_form_frame.children.values()):
            widget.delete(0, customtkinter.END)


if __name__ == "__main__":
    app = App()
    app.run()
