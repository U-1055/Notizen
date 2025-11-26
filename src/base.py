class DataConst:
    max_size = 10 * 1024 * 1024  # Максимальный размер файла - 10 Мб


class DataStructConst:
    date_changing = 'date_changing'
    name = 'name'
    tags = 'tags'

    note_struct = {tags: [], date_changing: ""}
    common_data_struct = {tags: []}

    datetime_date_format = '%d.%m.%Y'
    light_theme = ':/styles/light_theme'
    dark_theme = ':/styles/dark_theme'
    style = 'style'
    access_token = 'access_token'
    refresh_token = 'refresh_token'


class GuiConst:
    max_text_view_length = 250  # Максимальная длина текста в предпросмотре (на виджете заметки)


class GuiLabels:
    create_note = 'Новая заметка'
    view_tags = 'Теги...'
    set_theme_dark = 'Темная'
    set_theme_light = 'Светлая'
    damaged_notes_message = 'Обнаружены повреждённые заметки. Восстановить выбранные?'
    reclaim = 'Восстановить'
    search = 'Найти'
    update = 'Обновить'
    notes_reclaimed = 'Заметки восстановлены'
    unknown_error = 'Что-то пошло не так...'
    delete = 'Удалить'
    save = 'Сохранить'
    dont_save = 'Не сохранять'
    name_is_not_unique_error = 'Невозможно создать заметку - такая заметка уже существует'
    save_message = 'Несохранённые изменения будут утеряны.\nВы уверены, что хотите выйти?'
    no_found = 'Ничего не найдено :('
    base_note_name = 'Новая заметка'
    confirm = ''
    add_tag = '+'
    tag_exists_message = 'Такой тег уже существует'
    title_win_message = 'Сообщение'
    title_tags_manage_widget = 'Редактирование тегов'


class APIResponses:
    unauth = 'Unauthorized'
    unknown_arg = 'Unknown arg'
