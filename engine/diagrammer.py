import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import os

# Ensure output directory exists for asset compilation relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, '..', 'generated_assets')
os.makedirs(assets_dir, exist_ok=True)

def draw_physics_circuit(question_id):
    """
    Programmatically generates a professional physics circuit vector diagram.
    Returns the file path for LaTeX inclusion.
    """
    filename = os.path.abspath(os.path.join(assets_dir, f"circuit_{question_id}.png"))
    
    with schemdraw.Drawing(file=filename, show=False) as d:
        d.config(fontsize=12)
        d += elm.Battery().label('12V')
        d += elm.Resistor().label('10 $\\Omega$')
        d += elm.Switch().right()
        d += elm.Line().down()
        d += elm.MeterA().label('A')
        d += elm.Line().left()
        d += elm.Wire().to(d.here)

    return filename

def draw_mathematics_graph(question_id):
    """
    Programmatically generates a precise Cartesian graph for math assessments.
    """
    filename = os.path.abspath(os.path.join(assets_dir, f"graph_{question_id}.png"))
    
    plt.figure(figsize=(4, 4))
    plt.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16]) 
    plt.grid(True)
    plt.title("Assessment Function Plot")
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    
    return filename
