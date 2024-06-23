import matplotlib.pyplot as plt
import io
import base64

def generate_graph():
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 9, 11]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o')
    plt.title('Simple Line Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return graph_url