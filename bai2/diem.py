import re
from decimal import Decimal, ROUND_HALF_UP

from flask import Flask, render_template, request

app = Flask(__name__)

# (tên ô trong form, nhãn, trọng số %)
FIELDS = [
    {"key": "cc", "label": "Chuyên cần", "weight": 10},
    {"key": "gk", "label": "Giữa kỳ", "weight": 30},
    {"key": "ck", "label": "Cuối kỳ", "weight": 60},
]

# số nguyên hoặc thập phân, dấu thập phân là . hoặc ,  (loại nan, inf, 1e5, 1_0)
NUMBER = re.compile(r"^[+-]?(\d+([.,]\d*)?|[.,]\d+)$")


def check_score(raw):
    """MỘT hàm kiểm tra dùng chung cho cả 3 ô. Trả về (giá trị, lỗi)."""
    raw = (raw or "").strip()
    if not NUMBER.match(raw):
        return None, "Vui lòng nhập một số."
    value = Decimal(raw.replace(",", "."))
    if not 0 <= value <= 10:
        return None, "Điểm phải từ 0 đến 10."
    return value, None


def letter_grade(score, ck):
    """Điểm chữ. Điểm cuối kỳ dưới 1 là điểm liệt -> F."""
    if ck < 1:
        return "F"
    if score >= Decimal("8.5"):
        return "A"
    if score >= Decimal("7.0"):
        return "B"
    if score >= Decimal("5.5"):
        return "C"
    if score >= Decimal("4.0"):
        return "D"
    return "F"


@app.route("/", methods=["GET", "POST"])
def index():
    values = {f["key"]: "" for f in FIELDS}
    errors = {}
    result = None

    if request.method == "POST":
        scores = {}
        for f in FIELDS:
            raw = request.form.get(f["key"], "")
            values[f["key"]] = raw                      # giữ nguyên giá trị đã nhập
            scores[f["key"]], err = check_score(raw)
            if err:
                errors[f["key"]] = err

        if not errors:
            total = sum(scores[f["key"]] * f["weight"] for f in FIELDS) / 100
            # làm tròn 1 chữ số kiểu học thuật: 8.45 -> 8.5 (Decimal, không sai số số thực)
            score = total.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            grade = letter_grade(score, scores["ck"])
            result = {
                "text": f"{score} · {grade}",
                "grade": grade,
                "liet": scores["ck"] < 1,
            }

    return render_template("index.html", fields=FIELDS, values=values,
                           errors=errors, result=result)


if __name__ == "__main__":
    app.run(debug=True)
