from flask import Flask, render_template, request
import ezdxf
import os
from ezdxf.addons.drawing import Frontend, RenderContext, layout, svg

app = Flask(__name__)


def dxf_to_svg_data(file_path: str) -> str:
    """
    Convert a DXF file into an SVG string using ezdxf's SVG backend.
    A page size of (0, 0) automatically fits the output to the extents of the drawing.
    """
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    backend = svg.SVGBackend()
    Frontend(RenderContext(doc), backend).draw_layout(msp)
    return backend.get_string(layout.Page(0, 0))


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Serve the index page and handle DXF uploads.
    On POST, convert the uploaded DXF into SVG for preview.
    """
    svg_data = None
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename.lower().endswith('.dxf'):
            file_path = 'uploaded.dxf'
            uploaded_file.save(file_path)
            try:
                svg_data = dxf_to_svg_data(file_path)
            except Exception:
                svg_data = None
    return render_template('index.html', svg_data=svg_data)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
