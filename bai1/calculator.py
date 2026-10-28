import math

from flask import Flask, render_template, request

app = Flask(__name__)

OPS = ("+", "-", "*", "/")


def parse_number(raw):
    """Chuyển chuỗi thành số, chấp nhận dấu phẩy (2,5). Lỗi -> None."""
    raw = raw.strip().replace(",", ".")
    if raw == "":
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    if not math.isfinite(value):   # loại nan, inf
        return None
    return value


def fmt(x):
    """8.0 -> '8', 3.5 -> '3.5', -2.5 -> '-2.5'."""
    if x == int(x):
        return str(int(x))
    return str(round(x, 10))


@app.route("/", methods=["GET", "POST"])
def index():
    a_raw = ""
    b_raw = ""
    op = "+"
    errors = {}
    result = None

    if request.method == "POST":
        a_raw = request.form.get("a", "")
        b_raw = request.form.get("b", "")
        op = request.form.get("op", "")

        a = parse_number(a_raw)
        b = parse_number(b_raw)

        if a is None:
            errors["a"] = "Vui lòng nhập một số."
        if b is None:
            errors["b"] = "Vui lòng nhập một số."
        if op not in OPS:
            errors["op"] = "Phép toán không hợp lệ."
        if op == "/" and b == 0:
            errors["b"] = "Không thể chia cho 0."

        if not errors:
            if op == "+":
                r = a + b
            elif op == "-":
                r = a - b
            elif op == "*":
                r = a * b
            else:
                r = a / b
            result = f"{fmt(a)} {op} {fmt(b)} = {fmt(r)}"

    return render_template("index.html", a=a_raw, b=b_raw, op=op,
                           errors=errors, result=result, ops=OPS)


if __name__ == "__main__":
    app.run(debug=True)
