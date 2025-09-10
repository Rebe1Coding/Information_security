import flet as ft




import pandas as pd

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




def main(page: ft.Page):
    page.title = "DataFrame в Flet"
    page.scroll = "auto"  # если таблица большая — добавится скролл
    page.add(ft.Container(

    content=[ft.Text("Пример DataFrame в Flet", size=20), ft.Text("Пример DataFrame в Flet2", size=20)],
    padding=10,
    margin=5,
    border=ft.border.all(1, "blue"),
    border_radius=10,
    bgcolor="lightblue",
    width=200, height=500
    ))
    input_field = ft.TextField(label="Введите текст", width=300)
    output_container = ft.Column()  # сюда будем выводить таблицу

    # Обработчик кнопки
    def on_submit(e):
        df = char_probabilities(input_field.value)

        # преобразуем DataFrame в DataTable
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in df.columns],
            rows=[
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(value))) for value in row]
                )
                for row in df.values
            ]
        )

        # очищаем контейнер и добавляем таблицу
        output_container.controls.clear()
        output_container.controls.append(table)
        page.update()

    page.add(
        input_field,
        ft.ElevatedButton("Преобразовать", on_click=on_submit),
        output_container
    )

ft.app(target=main)
