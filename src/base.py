class DataConst:
    max_size = 10 * 1024 * 1024  # Максимальный размер файла - 10 Мб


class DataStructConst:
    date_changing = 'date_changing'
    name = 'name'
    tags = 'tags'

    note_struct = {tags: [], date_changing: ""}

    datetime_date_format = '%d.%m.%Y'
    light_theme = ':/styles/light_theme'
    dark_theme = ':/styles/dark_theme'


class GuiConst:
    max_text_view_length = 250  # Максимальная длина текста в предпросмотре (на виджете заметки)


class GuiLabels:
    create_note = 'Новая заметка'
    view_tags = 'Теги...'
    set_theme_dark = 'Темная'
    set_theme_light = 'Светлая'
