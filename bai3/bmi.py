import re

from flask import Flask, render_template, request

app = Flask(__name__)

NUMBER = re.compile(r"^[+-]?(\d+([.,]\d*)?|[.,]\d+)$")


def check_number(raw, lo, hi):
    """MỘT hàm kiểm tra dùng chung cho cả 2 ô. Trả về (giá trị, lỗi).

    Sai khoảng thì vẫn trả giá trị đã đọc được để nơi gọi gợi ý thêm."""
    raw = (raw or "").strip()
    if not NUMBER.match(raw):
        return None, "Vui lòng nhập một số."
    value = float(raw.replace(",", "."))
    if not lo <= value <= hi:
        return value, f"Giá trị phải từ {lo} đến {hi}."
    return value, None


def classify(bmi):
    """Chuẩn người châu Á. Trả về (nhãn, màu)."""
    if bmi < 18.5:
        return "Thiếu cân", "vang"
    if bmi < 23:
        return "Bình thường", "xanh"
    if bmi < 25:
        return "Thừa cân", "vang"
    return "Béo phì", "do"


@app.route("/", methods=["GET", "POST"])
def index():
    values = {"cao": "", "nang": ""}
    errors = {}
    result = None

    if request.method == "POST":
        values["cao"] = request.form.get("cao", "")
        values["nang"] = request.form.get("nang", "")

        cao, err = check_number(values["cao"], 50, 250)
        if err:
            if cao is not None and cao < 3:             # 1,70 -> chắc là nhập mét
                err += " (nhập mét thay vì cm)"
            errors["cao"] = err
        nang, err = check_number(values["nang"], 10, 300)
        if err:
            errors["nang"] = err

        if not errors:
            m = cao / 100
            bmi = round(nang / m ** 2, 1)
            label, color = classify(bmi)
            result = {
                "text": f"{bmi:.1f} · {label}",
                "color": color,
                # cân nặng ứng với BMI 18,5 – 22,9
                "range": f"{round(18.5 * m ** 2, 1):.1f} – {round(22.9 * m ** 2, 1):.1f} kg",
            }

    return render_template("index.html", values=values, errors=errors, result=result)


if __name__ == "__main__":
    app.run(debug=True)
