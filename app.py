import os
from flask import Flask, request, jsonify

import renderer
from renderer import RenderError

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def generate():
    try:
        req_data = request.get_json() or {}
        markdown_text = req_data.get('markdown', '')
        matkul = req_data.get('matkul_folder', 'GENERAL')
        judul = req_data.get('judul') or req_data.get('metadata', {}).get('judul_jobsheet', '')
        metadata = req_data.get('metadata', {})
        export_formats = req_data.get('export_formats', ['pdf', 'docx'])

        generated_files = renderer.render_markdown(
            markdown_text, matkul, judul, tuple(export_formats), metadata)

        return jsonify({
            "status": "success",
            "message": "File berhasil digenerate!",
            "folder": str(renderer.OUTPUT_DIR / matkul.strip().upper()),
            "files": [str(p) for p in generated_files],
        }), 200

    except RenderError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
