import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from threading import Thread
import logging

log = logging.getLogger(__name__)


class WebServer:
    def __init__(self, image_dir):
        self.app = Flask(__name__)
        CORS(self.app,
             resources={r"/*": {"origins": ["http://localhost:8080",
                                            "http://localhost:6421",
                                            "https://manik.cc",
                                            "http://manik.cc"]}})
        self.image_dir = os.path.abspath(image_dir)

        @self.app.route('/api/images')
        def get_images():
            images = [
                f for f in os.listdir(
                    self.image_dir) if f.endswith(
                    ('.png', '.jpg', '.jpeg'))]
            images.sort(reverse=True)  # Show newest images first
            image_urls = [
                f'http://localhost:8080/images/{image}' for image in images]
            return jsonify({'images': image_urls})

        @self.app.route('/images/<path:filename>')
        def serve_image(filename):
            return send_from_directory(self.image_dir, filename)

    def start(self):
        def run_server():
            self.app.run(host='0.0.0.0', port=6421)

        server_thread = Thread(target=run_server, daemon=True)
        server_thread.start()
        log.info("Web server started on http://localhost:8080")
