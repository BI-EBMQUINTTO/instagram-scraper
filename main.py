# encoding: utf-8

from pathlib import Path
from flet import *
from winotify import Notification, audio
from instagram_scraper import extrair_comentarios
import fontawesome as fa
from bi_ebmquintto.instagram.utils import sentimentalização, process_topics
import sys
sys.path
sys.path.append(r'C:\Users\EBMquintto\Desktop\app\env\Lib\site-packages')

def main(page: Page):
    page.theme_mode='light'
    page.title = "Instagram Scraper" 
    page.bgcolor = 'white'
    page.window_height = 600
    page.window_width = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.fonts = {
        "Oswald": r"assets\fonts\Oswald\Oswald-VariableFont_wght.ttf",
        "Righteous": r"assets\fonts\Righteous\Righteous-Regular.ttf",
        "Roboto_Slab": r"assets\fonts\Roboto_Slab\RobotoSlab-VariableFont_wght.ttf"
    }
    page.theme = Theme(font_family="Roboto_Slab")

    def scraper_notification(number):
        return Notification(
            app_id="Instagram Scraper",
            title="Extração Finalizada",
            msg=f"A extração dos comentários foi finalizada! Foram extraidos {number} comentários.",
            duration="long",
            icon=r"C:\Users\EBMquintto\Desktop\app\assets\favicon.png"
        )

    sentimento_notification = Notification(
            app_id="Instagram Scraper",
            title="Sentimentalização Finalizada",
            msg=f"A sentimentização dos comentários foi finalizada!",
            duration="long",
            icon=r"C:\Users\EBMquintto\Desktop\app\assets\favicon.png"
        )

    topicos_notification = Notification(
            app_id="Instagram Scraper",
            title="Geração de Tópicos Finalizada",
            msg=f"A Geração de Tópicos dos comentários foi finalizada!",
            duration="long",
            icon=r"C:\Users\EBMquintto\Desktop\app\assets\favicon.png"
        )
    
    sentimento_notification.set_audio(audio.Default, loop=True)
    topicos_notification.set_audio(audio.Default, loop=True)

    carregando = ProgressBar(height=3, color=colors.AMBER_700, bgcolor="#eeeeee", visible=False)
    carregando_scraper = ProgressBar(height=3, color=colors.AMBER_700, bgcolor="#eeeeee", visible=False)
    carregando_topicos = ProgressBar(height=3, color=colors.AMBER_700, bgcolor="#eeeeee", visible=False)

    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else 'Nenhum arquivo selecionado'
        )
        selected_files.update()
        page.update()

    def pick_files_result_topicos(e: FilePickerResultEvent):
        selected_files_topicos.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else 'Nenhum arquivo selecionado'
        )
        selected_files_topicos.update()
        page.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text('Nenhum arquivo selecionado', weight=FontWeight.W_500, overflow=TextOverflow.CLIP)
    pick_files_topicos = FilePicker(on_result=pick_files_result_topicos)
    selected_files_topicos = Text('Nenhum arquivo selecionado', weight=FontWeight.W_500, overflow=TextOverflow.CLIP)

    page.overlay.append(pick_files_dialog)
    page.overlay.append(pick_files_topicos)

    def close_banner(e):
        page.banner.open = False
        page.update()

    def banner(number): 
        return Banner(
            bgcolor=colors.AMBER_700,
            content_padding=10,
            leading=Icon(icons.CHECK_CIRCLE_ROUNDED, color='white', size=40),
            content=Text(
                f'Processo finalizado. Foram carregados: {number} comentários!',
                color='white',
                weight=FontWeight.W_500,
                size=15
            ),
            actions=[
                IconButton(icon=icons.CLOSE_ROUNDED, on_click=close_banner, icon_color='white'),
            ],
        )

    def show_banner_click(numero):
        page.banner = banner(numero)
        page.banner.open = True
        page.update()

    def save_data(url, arquivo, cliques):
        values = []
        values.append(url.value)
        values.append(arquivo.value)
        values.append(cliques.value)
        page.update()
        carregando_scraper.visible = True
        carregando_scraper.update()
        page.update()
        numero_comentarios = extrair_comentarios(values[0], values[1], values[2])
        carregando_scraper.visible = False
        carregando_scraper.update()
        page.update()
        notf = scraper_notification(numero_comentarios)
        notf.set_audio(audio.Default, loop=True)
        notf.show()
        show_banner_click(numero_comentarios)

    def sentimentalizar():
        print(selected_files.value)
        if selected_files.value != 'Nenhum arquivo selecionado!' and selected_files.value != None:
            carregando.visible = True
            carregando.update()
            page.update()
            sentimentalização(fr"{selected_files.value}", r"config\ebmquinto-sentiment-analisis-146a9bd5715d.json")
            sentimento_notification.show()
            carregando.visible = False
            carregando.update()
            page.update()
        else:
            print("Invalido!")

    def topicos():
        print(selected_files_topicos.value)
        if selected_files_topicos.value != 'Nenhum arquivo selecionado!' and selected_files_topicos.value != None:
            carregando_topicos.visible = True
            carregando_topicos.update()
            page.update()
            process_topics(fr"{selected_files_topicos.value}")
            topicos_notification.show()
            carregando_topicos.visible = False
            carregando_topicos.update()
            page.update()
        else:
            print("Invalido!")


    url = TextField(
            label='URL',
            label_style=TextStyle(color=colors.AMBER_700, weight=FontWeight.W_500),
            border_color=colors.AMBER_700,
            border_width=2,
            value=None,
        )

    arquivo = TextField(
            label='Arquivo',
            label_style=TextStyle(color=colors.AMBER_700, weight=FontWeight.W_500),
            border_color=colors.AMBER_700,
            border_width=2,
            value=None,
        )

    cliques = TextField(
            label='Cliques',
            label_style=TextStyle(color=colors.AMBER_700, weight=FontWeight.W_500),
            border_color=colors.AMBER_700,
            border_width=2,
            value=None,
        )

    footer = Container(
        margin=margin.only(right=10, bottom=10),
        content=Row(
            alignment = MainAxisAlignment.CENTER,
            controls=[
                Container(
                    height=2,
                    bgcolor=colors.AMBER_700,
                    expand=True,
                    margin=margin.only(right=10),
                    border_radius=10
                ),
                Image(
                    r"assets\logo.png", 
                    width=60,
                    border_radius=10
                ),
                Container(
                    height=2,
                    bgcolor=colors.AMBER_700,
                    expand=True,
                    margin=margin.only(left=10),
                    border_radius=10
                ),
            ]
        )
    )

    pages = Tabs(
        selected_index=0,
        animation_duration=200,
        tabs=[
            Tab(
                tab_content=Row(
                    controls=[
                        Icon(icons.DOWNLOAD_ROUNDED, color=colors.BLACK),
                        Text("Extrair", color=colors.BLACK, weight=FontWeight.W_500),
                    ]
                ),
                content = Container(
                    padding=padding.only(top=20),
                    content=Column(
                        controls=[
                            Container(
                                content=url,
                                padding=padding.symmetric(horizontal=10),
                            ),
                            Container(
                                content=arquivo,
                                padding=padding.symmetric(horizontal=10)
                            ),
                            Container(
                                content=cliques,
                                padding=padding.symmetric(horizontal=10)
                            ),
                            Container(
                                content=ElevatedButton(
                                    content=Text('Extrair Comentários', color='white', weight=FontWeight.W_500),
                                    style=ButtonStyle(
                                        color='white',
                                        bgcolor=colors.BLACK,
                                        shape=RoundedRectangleBorder(radius=5),
                                        padding=Padding(20, 15, 20, 15)
                                    ),
                                    on_click= lambda e: save_data(url, arquivo, cliques)
                                ),
                                padding=padding.symmetric(horizontal=10, vertical=10)
                            ),
                            Container(
                                content=carregando_scraper,
                                padding=padding.symmetric(vertical=15, horizontal=10)
                            ),
                            Container(expand=True),
                            footer
                        ]
                    )
                )
            ),
            Tab(
                tab_content=Row(
                    controls=[
                        Icon(icons.RULE_SHARP, color=colors.BLACK),
                        Text("Sentimentalizar", color=colors.BLACK, weight=FontWeight.W_500),
                    ]
                ),
                content=Container(
                    padding = padding.only(top=20),
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Container(
                                        content=Row(
                                            controls=[
                                                Text("Arquivo selecionado: ", color=colors.AMBER_700, weight=FontWeight.W_500),
                                                Container(
                                                    width=400,
                                                    content=selected_files
                                                ),
                                            ]
                                        ),
                                        padding=padding.all(10),
                                        expand=True,
                                        border=border.all(width=2, color=colors.AMBER_700),
                                        border_radius=8,
                                        margin=margin.only(left=10)
                                    ),
                                    IconButton(
                                        icon=icons.UPLOAD_FILE,
                                        style=ButtonStyle(
                                            color='white',
                                            bgcolor=colors.AMBER_700,
                                            shape=CircleBorder(),
                                            padding=Padding(10, 5, 10, 5)
                                        ),
                                        on_click=lambda _: pick_files_dialog.pick_files(
                                            allow_multiple=True
                                        ),
                                    ),
                                    Container(width=10),
                                ]
                            ),
                            Container(
                                content=ElevatedButton(
                                    'Sentimentalizar arquivo',
                                    style=ButtonStyle(
                                        color='white',
                                        bgcolor=colors.BLACK,
                                        padding=Padding(15, 10, 15, 10),
                                        shape=RoundedRectangleBorder(radius=5),
                                    ),
                                    on_click=lambda _: sentimentalizar(),
                                ),
                                padding=padding.all(10)
                            ),
                            Container(
                                content=carregando,
                                padding=padding.symmetric(horizontal=10, vertical=15)
                            ),
                            Container(expand=True),
                            footer
                        ]
                    ),
                )
            ),
            Tab(
                tab_content=Row(
                    controls=[
                        Icon(icons.TOPIC, color=colors.BLACK),
                        Text("Tópicos", color=colors.BLACK, weight=FontWeight.W_500),
                    ]
                ),
                content=Container(
                    padding = padding.only(top=20),
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Container(
                                        content=Row(
                                            controls=[
                                                Text("Arquivo selecionado: ", color=colors.AMBER_700, weight=FontWeight.W_500),
                                                Container(
                                                    width=400,
                                                    content=selected_files_topicos
                                                ),
                                            ]
                                        ),
                                        padding=padding.all(10),
                                        expand=True,
                                        border=border.all(width=2, color=colors.AMBER_700),
                                        border_radius=8,
                                        margin=margin.only(left=10)
                                    ),
                                    IconButton(
                                        icon=icons.UPLOAD_FILE,
                                        style=ButtonStyle(
                                            color='white',
                                            bgcolor=colors.AMBER_700,
                                            shape=CircleBorder(),
                                            padding=Padding(10, 5, 10, 5)
                                        ),
                                        on_click=lambda _: pick_files_topicos.pick_files(
                                            allow_multiple=True
                                        ),
                                    ),
                                    Container(width=10),
                                ]
                            ),
                            Container(
                                content=ElevatedButton(
                                    'Gerar tópicos',
                                    style=ButtonStyle(
                                        color='white',
                                        bgcolor=colors.BLACK,
                                        padding=Padding(15, 10, 15, 10),
                                        shape=RoundedRectangleBorder(radius=5),
                                    ),
                                    on_click=lambda _: topicos(),
                                ),
                                padding=padding.all(10)
                            ),
                            Container(
                                content=carregando_topicos,
                                padding=padding.symmetric(horizontal=10, vertical=15)
                            ),
                            Container(expand=True),
                            footer
                        ]
                    ),
                )
            ),
        ],
        expand=1,
    )
            
    page.update()
    page.add(pages)
    page.update()
    

if __name__ == "__main__":
    app(target=main, assets_dir="assets", view=FLET_APP)