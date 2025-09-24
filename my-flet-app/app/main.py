import flet as ft
import pandas as pd
from services import (ShannonFano, Huffman)


def df_to_container(df: pd.DataFrame, num1: float, num2: float) -> ft.Container:
    header = ft.Row([
        ft.Text(f"Средняя длинна: {num1}", size=14),
        ft.Text(f"Энтропия: {num2}", size=14)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    columns = [ft.DataColumn(ft.Text(col)) for col in df.columns] if not df.empty else []
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
    return ft.Container(content=content, padding=10,
                        border=ft.border.all(1, ft.Colors.BLACK12),
                        bgcolor=ft.Colors.WHITE)


def main(page: ft.Page):
    page.title = "Шифрование — выбор метода"

    txt = ft.TextField(label="Текст для кодирования", width=400, multiline=False)

    method_dd = ft.Dropdown(
        width=200,
        label="Метод",
        value="shannon",
        options=[
            ft.dropdown.Option("shannon", text="Shannon-Fano"),
            ft.dropdown.Option("huffman", text="Huffman"),
        ],
    )

    results_column = ft.Column([], spacing=12)

    encoded_result = {"encoded": "", "decoded": ""}  # будем хранить, чтобы сохранять в файл

    def show_snack(message: str):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    # === Чтение текста из файла ===
    def on_file_upload(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            if not file.name.endswith(".txt"):
                show_snack("Можно загружать только .txt файлы")
                return

            try:
                with open(file.path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if not content:
                    show_snack("Файл пуст")
                    return
                txt.value = content
                page.update()
            except Exception as ex:
                show_snack(f"Ошибка при чтении файла: {ex}")

    file_picker = ft.FilePicker(on_result=on_file_upload)
    page.overlay.append(file_picker)

    upload_btn = ft.ElevatedButton("Загрузить .txt", on_click=lambda e: file_picker.pick_files())

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
        return "Не реализовано"

    def try_call_decode(algo, encoded_text) -> str:
        fn = getattr(algo, "decode", None)
        if callable(fn):
            try:
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

        algo = ShannonFano() if method_dd.value == "shannon" else Huffman()

        if hasattr(algo, "text"):
            try:
                algo.text = text
            except Exception:
                pass

        try:
            df, avg_len, entropy = algo.analytics()
        except Exception as ex:
            show_snack(f"Ошибка при расчётах: {ex}")
            return

        encoded = try_call_encode(algo, text)
        decoded = try_call_decode(algo, encoded if isinstance(encoded, str) else "")

        encoded_result["encoded"] = str(encoded)
        encoded_result["decoded"] = str(decoded)

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

        # кнопка сохранить в файл (внизу результатов)
        save_btn = ft.ElevatedButton("Сохранить в файл", on_click=on_save_click)
        results_column.controls.append(save_btn)

        page.update()

    # === Сохранение вывода в файл ===
    def on_save_click(e):
        try:
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write("Закодированное:\n")
                f.write(encoded_result["encoded"] + "\n\n")
                f.write("Декодированное:\n")
                f.write(encoded_result["decoded"] + "\n")
            show_snack("Результат сохранён в output.txt")
        except Exception as ex:
            show_snack(f"Ошибка при сохранении: {ex}")

    btn = ft.ElevatedButton("Кодировать", on_click=on_encode_click)

    controls = ft.Column([
        ft.Row([txt, upload_btn, method_dd, btn],
               alignment=ft.MainAxisAlignment.START, spacing=12),
        ft.Divider(),
        results_column
    ], spacing=12)

    page.add(controls)
    page.update()


ft.app(target=main)
