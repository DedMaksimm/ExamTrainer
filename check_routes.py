import sys
import traceback

try:
    from app import create_app
except Exception as e:
    print("Ошибка при импорте create_app():", e)
    traceback.print_exc()
    sys.exit(1)

try:
    app = create_app()
except Exception as e:
    print("Ошибка при создании приложения (create_app()):", e)
    traceback.print_exc()
    sys.exit(1)

print("=== URL map (routes) ===")
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    print(f"{rule.rule:30} -> endpoint: {rule.endpoint}")

print("\n=== Тест GET / ===")
with app.test_client() as c:
    res = c.get("/")
    print("GET / status code:", res.status_code)
    print("GET / content-type:", res.content_type)
    data = res.get_data(as_text=True)
    print("GET / response (first 500 chars):")
    print(data[:500].replace("\n", "\\n"))

print("\n=== Конец проверки ===")
