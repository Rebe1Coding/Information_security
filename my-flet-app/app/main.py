import flet as ft
import pandas as pd
from services import (ShannonFano, Huffman)

# Функция преобразует DataFrame и два числа в визуальный контейнер Flet.
def df_to_container(df: pd.DataFrame, num1: float, num2: float) -> ft.Container:
    # header: показывает среднюю длину и энтропию.
    header = ft.Row([
        ft.Text(f"Средняя длинна: {num1}", size=14),
        ft.Text(f"Энтропия: {num2}", size=14)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Преобразуем колонки DataFrame в колонки таблицы Flet.
    columns = [ft.DataColumn(ft.Text(col)) for col in df.columns] if not df.empty else []

    # Формируем строки таблицы по строкам DataFrame.
    rows = []
    for _, r in df.iterrows():
        cells = [ft.DataCell(ft.Text(str(v))) for v in r.tolist()]
        rows.append(ft.DataRow(cells=cells))

    # Создаём DataTable; если DataFrame пуст — показываем текст.
    table = ft.DataTable(
        columns=columns,
        rows=rows,
        show_checkbox_column=False,
        column_spacing=20,
        heading_row_height=40,
        data_row_min_height=30,
    ) if columns else ft.Text("DataFrame пуст", italic=True)

    # Возвращаем контейнер с таблицей и заголовком.
    content = ft.Column([ft.Divider(), table, header], spacing=10, tight=True)
    return ft.Container(content=content, padding=10, border=ft.border.all(1, ft.Colors.BLACK12), bgcolor=ft.Colors.WHITE)


def main(page: ft.Page):
    # Заголовок окна
    page.title = "Шифрование — выбор метода"
    # Поле ввода текста для кодирования
    txt = ft.TextField(label="Текст для кодирования", width=400, multiline=False)
    # Выпадающий список выбора метода: shannon или huffman
    method_dd = ft.Dropdown(
        width=200,
        label="Метод",
        value="shannon",
        options=[
            ft.dropdown.Option("shannon", text="Shannon-Fano"),
            ft.dropdown.Option("huffman", text="Huffman"),
        ],
    )

    # Колонка для отображения результатов (таблица, закодированное, декодированное)
    results_column = ft.Column([], spacing=12)

    def show_snack(message: str):
        # Показывает короткое уведомление на странице.
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    def try_call_encode(algo, text) -> str:
        # Универсально вызывает метод encode у объекта алгоритма.
        # Обрабатывает варианты сигнатур (с аргументом/без) и исключения.
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
        # Аналогично вызывает decode.
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
        # Обработчик кнопки: валидация, выбор алгоритма, сбор статистики, кодирование.
        text = txt.value or ""
        if not text.strip():
            show_snack("Поле пустое — введите текст")
            return

        # Создаём экземпляр выбранного алгоритма.
        if method_dd.value == "shannon":
            algo = ShannonFano()
        else:
            algo = Huffman()

        # Присваиваем текст в объект алгоритма (триггерит пересчёт кодов)
        if hasattr(algo, "text"):
            try:
                algo.text = text
            except Exception:
                pass

        # Получаем статистику: DataFrame, средняя длина, энтропия.
        try:
            df, avg_len, entropy = algo.analytics()
        except Exception as ex:
            show_snack(f"Ошибка при расчётах: {ex}")
            return

        # Попытка закодировать и декодировать текст безопасно.
        encoded = try_call_encode(algo, text)
        decoded = try_call_decode(algo, encoded if isinstance(encoded, str) else "")

        # Формируем три контейнера: таблица со статистикой, закодированное и декодированное.
        tbl_container = df_to_container(df, avg_len, entropy)
        enc_container = ft.Container(
            content=ft.Column([ft.Text("Закодированное:"), ft.Text(str(encoded))]),
            padding=8, border=ft.border.all(1, ft.Colors.BLACK12), bgcolor=ft.Colors.WHITE
        )
        dec_container = ft.Container(
            content=ft.Column([ft.Text("Декодированное:"), ft.Text(str(decoded))]),
            padding=8, border=ft.border.all(1, ft.Colors.BLACK12), bgcolor=ft.Colors.WHITE
        )

        # Обновляем область результатов и страницу.
        results_column.controls.clear()
        results_column.controls.append(tbl_container)
        results_column.controls.append(enc_container)
        results_column.controls.append(dec_container)
        page.update()

    # Кнопка запуска кодирования
    btn = ft.ElevatedButton("Кодировать", on_click=on_encode_click)

    # Собираем элементы управления на странице
    controls = ft.Column([
        ft.Row([txt, method_dd, btn], alignment=ft.MainAxisAlignment.START, spacing=12),
        ft.Divider(),
        results_column
    ], spacing=12)

    page.add(controls)
    page.update()

# Запуск приложения Flet
ft.app(target=main)
