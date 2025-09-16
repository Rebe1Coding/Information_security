import flet as ft
import pandas as pd
from services import (ShannonFano, Huffman)

def char_probabilities(text: str) -> pd.DataFrame:
    
    total = len(text)
    if total == 0:
        return pd.DataFrame(columns=["char", "count", "probability"])
    
   
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1

    
    df = pd.DataFrame([
        {"char": ch, "count": cnt, "probability": cnt / total}
        for ch, cnt in counts.items()
    ])
    
    
    df = df.sort_values("probability", ascending=False).reset_index(drop=True)
    
    return df







def df_to_container(df: pd.DataFrame, num1: float, num2: float) -> ft.Container:
    """
    Возвращает flet.Container с выводом DataFrame и двух чисел в виде текста.
    """
    # Текстовые блоки для чисел
    header = ft.Row([
        ft.Text(f"Средняя длинна: {num1}", size=14),
        ft.Text(f"Энтропия: {num2}", size=14)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Столбцы таблицы
    columns = [ft.DataColumn(ft.Text(col)) for col in df.columns] if not df.empty else []

    # Строки таблицы
    rows = []
    for _, r in df.iterrows():
        cells = [ft.DataCell(ft.Text(str(v))) for v in r.tolist()]
        rows.append(ft.DataRow(cells=cells))

    table = ft.DataTable(
        columns=columns,
        rows=rows,
        show_checkbox_column=False,
        column_spacing=20,
        heading_row_height=40,
        data_row_min_height=30,
    ) if columns else ft.Text("DataFrame пуст", italic=True)

    content = ft.Column([ft.Divider(), table, header], spacing=10, tight=True)
    return ft.Container(content=content, padding=10, border=ft.border.all(1, ft.Colors.BLACK12), bgcolor=ft.Colors.WHITE)


def main(page: ft.Page):
    page.title = "Шифрование — выбор метода"
    # Ввод текста
    txt = ft.TextField(label="Текст для кодирования", width=400, multiline=False)
    # Выбор метода
    method_dd = ft.Dropdown(
        width=200,
        label="Метод",
        value="shannon",
        options=[
            ft.dropdown.Option("shannon", text="Shannon-Fano"),
            ft.dropdown.Option("huffman", text="Huffman"),
        ],
    )

    # Контейнеры результатов (будем обновлять)
    results_column = ft.Column([], spacing=12)

    def show_snack(message: str):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    def try_call_encode(algo, text) -> str:
        fn = getattr(algo, "encode", None)
        if callable(fn):
            try:
                return fn() if fn.__code__.co_argcount == 1 else fn(text)
            except Exception:
                try:
                    return fn(text)
                except Exception:
                    return "Ошибка при кодировании"
        # fallback
        return "Не реализовано"

    def try_call_decode(algo, encoded_text) -> str:
        fn = getattr(algo, "decode", None)
        if callable(fn):
            try:
                # попытка вызвать с аргументом, иначе без
                return fn(encoded_text)
            except Exception:
                try:
                    return fn()
                except Exception:
                    return "Ошибка при декодировании"
        return "Не реализовано"

    def on_encode_click(e):
        text = txt.value or ""
        if not text.strip():
            show_snack("Поле пустое — введите текст")
            return

        # выбрать алгоритм
        algo = None
        if method_dd.value == "shannon":
            algo = ShannonFano()
        else:
            algo = Huffman()

        # присвоить текст если есть атрибут
        if hasattr(algo, "text"):
            try:
                algo.text = text
            except Exception:
                pass

        # analytics
        try:
            df, avg_len, entropy = algo.analytics()
        except Exception as ex:
            show_snack(f"Ошибка при расчётах: {ex}")
            return

        # попытка кодирования/декодирования (без падений)
        encoded = try_call_encode(algo, text)
        decoded = try_call_decode(algo, encoded if isinstance(encoded, str) else "")

        # контейнеры
        tbl_container = df_to_container(df, avg_len, entropy)
        enc_container = ft.Container(
            content=ft.Column([ft.Text("Закодированное:"), ft.Text(str(encoded))]),
            padding=8, border=ft.border.all(1, ft.Colors.BLACK12), bgcolor=ft.Colors.WHITE
        )
        dec_container = ft.Container(
            content=ft.Column([ft.Text("Декодированное:"), ft.Text(str(decoded))]),
            padding=8, border=ft.border.all(1, ft.Colors.BLACK12), bgcolor=ft.Colors.WHITE
        )

        results_column.controls.clear()
        results_column.controls.append(tbl_container)
        results_column.controls.append(enc_container)
        results_column.controls.append(dec_container)
        page.update()

    btn = ft.ElevatedButton("Кодировать", on_click=on_encode_click)

    controls = ft.Column([
        ft.Row([txt, method_dd, btn], alignment=ft.MainAxisAlignment.START, spacing=12),
        ft.Divider(),
        results_column
    ], spacing=12)

    page.add(controls)
    page.update()


# def df_to_container(df: pd.DataFrame, num1: float, num2: float) -> ft.Container:
#     """
#     Возвращает flet.Container с выводом DataFrame и двух чисел в виде текста.
#     """
#     # Текстовые блоки для чисел
#     header = ft.Row([
#         ft.Text(f"Число 1: {num1}", size=14),
#         ft.Text(f"Число 2: {num2}", size=14)
#     ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

#     # Столбцы таблицы
#     columns = [ft.DataColumn(ft.Text(col)) for col in df.columns] if not df.empty else []

#     # Строки таблицы
#     rows = []
#     for _, r in df.iterrows():
#         cells = [ft.DataCell(ft.Text(str(v))) for v in r.tolist()]
#         rows.append(ft.DataRow(cells=cells))

#     table = ft.DataTable(
#         columns=columns,
#         rows=rows,
#         show_checkbox_column=False,
#         column_spacing=20,
#         heading_row_height=40,
#         data_row_min_height=30,  
#     ) if columns else ft.Text("DataFrame пуст", italic=True)
# # ...existing code...

#     content = ft.Column([header, ft.Divider(), table], spacing=10, tight=True)
#     return ft.Container(content=content, padding=10, border=ft.border.all(1, ft.Colors.BLACK12), bgcolor=ft.Colors.WHITE)


# def main(page: ft.Page):
#     sh = ShannonFano()
#     h = Huffman()
#     text = "hello world"
#     sh.text = text  
#     df = pd.DataFrame()
#     df, avg_len, entropy = sh.analytics()
    
#     c = df_to_container(df, avg_len, entropy)
#     page.add(c)
#     page.update()



ft.app(target=main)
