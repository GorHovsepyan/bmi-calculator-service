import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def calculate_bmi(weight, height):
    bmi = weight / (height / 100) ** 2

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obesity"

    return round(bmi, 2), category


class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {
                "service": "BMI Calculator Service",
                "usage": "Send weight and height to POST /calculate"
            })
        elif self.path == "/health":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/calculate":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(content_length))
            weight = float(data["weight_kg"])
            height = float(data["height_cm"])

            if weight <= 0 or height <= 0:
                raise ValueError

            bmi, category = calculate_bmi(weight, height)
            self.send_json(200, {"bmi": bmi, "category": category})
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            self.send_json(400, {
                "error": "Send positive weight_kg and height_cm values"
            })

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), RequestHandler)
    print(f"Server is running on port {port}")
    server.serve_forever()
