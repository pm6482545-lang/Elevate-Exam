import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import os

# Ensure output directory exists for asset compilation
os.makedirs('generated_assets', exist_ok=True)

def draw_physics_circuit(question_id):
    """
    Programmatically generates a professional physics circuit vector diagram.
    Returns the file path for LaTeX inclusion.
    """
    filename = f"generated_assets/circuit_{question_id}.png"
    
    with schemdraw.Drawing(file=filename, show=False) as d:
        d.config(fontsize=12)
        d += elm.Battery().label('12V')
        d += elm.Resistor().label('10 $\Omega$')
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
    filename = f"generated_assets/graph_{question_id}.png"
    
    plt.figure(figsize=(4, 4))
    plt.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16]) 
    plt.grid(True)
    plt.title("Assessment Function Plot")
    plt.savefig(filename)
    plt.close()
    
    return filename
