import matplotlib.pyplot as plt


def generate_line_graph(x_label, y_label, x_values, y_values):
    plt.plot(x_values, y_values, x_values, 'o-r')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
