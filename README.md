# The Binding of Isaac: Python

#### Копия видеоигры The Binding of Isaac ([2011](https://store.steampowered.com/app/113200/The_Binding_of_Isaac), [2014](https://store.steampowered.com/app/250900/The_Binding_of_Isaac_Rebirth/))

**The Binding of Isaac** — это двухмерный шутер со случайно генерируемыми уровнями и элементами ролевых и роуглайк **(Rogue-like)** игр. Сопровождая Исаака в его похождениях, игроки найдут множество необычных сокровищ, которые изменят внешность Исаака и дадут ему сверхчеловеческие способности, позволяющие победить толпы загадочных существ, открыть множество тайн и с боем пробить себе путь к спасению. 

### Запуск

1. Установить python версии **3.10**+
(Тестировалось на версии **3.10.8**)
2. Склонировать репозиторий и перейти в него: 
```commandline
git clone https://github.com/K1rL3s/The-Binding-of-Isaac-Python.git
cd ./The-Binding-of-Isaac-Python
```

3. Установить все библиотеки, перечисленные в `requirements.txt` файле:
```commandline
pip install -r ./requirements.txt
```

4. Запустить игру:
```commandline
python ./main.py
```

5. Для сбора .exe файла необходимо установить библиотеку **pyinstaller** и выполнить команду ниже.\
   (заменить `--add-data="./src/*:."` при ошибке добавления папки)\
   ([я собрал](https://drive.google.com/drive/folders/1dPlvhPORBvDJsscCtiBQHlM42Of4yZ1F))
```
pyinstaller --onefile --noconsole --icon="./src/data/images/icon/64x64.ico" --add-data="./src/*;." ./main.py
```

### Ключевые особенности: 

- Случайно генерируемые подземелья, артефакты, противники и боссы.
- Более 10 уникальных предметов, которые не только дают вам способности, но и внешне изменяют вашего персонажа.
- Более 5 разных противников, не считая боссов.
- Более 5 разных уровней.
- Три игровых персонажа.
- Различные концовки.

### Основное реализованное:

- Стартовый экран, меню выбора персонажа, меню паузы, смерти и победы.
- "Процедурная" генерация этажей.
- Класс Бога - Комната.
- ГГ (пока что не WP).
- Три основных вида врагов: стоячие, двигающиеся, стреляющие.
- Ловушки и препятствия (шипы, костры, камни).
- Подбираемые предметы, артефакты и магазин.
- Два вида слёз (не разработчиков).

### Как можно усовершенствовать проект:

- Увеличить разнообразие предметов, противников, боссов и игровых персонажей.
- Пошаманить над генерацией уровней.
- Сделать разные концовки.

### Скриншоты
![isaac_IPU55ODdsb](https://user-images.githubusercontent.com/104463209/215344266-21f53dc1-2f5f-46b0-9c60-246aeca3a754.png)
![isaac_2XHjvtHyfc](https://user-images.githubusercontent.com/104463209/215344280-3b2338db-5f86-469e-b109-7487e46fa72d.png)
![isaac_XZxB7cC1A9](https://user-images.githubusercontent.com/104463209/215344300-e97a3a59-0826-4c84-9bd6-f4e24f5fb280.png)
![isaac_CUBLM1jKSM](https://user-images.githubusercontent.com/104463209/215344301-43a5dd86-60a0-46d7-8e86-ed1911395c1e.png)
![isaac_SlTizpsGhf](https://user-images.githubusercontent.com/104463209/215344303-4f7429f5-0218-463b-87c5-8281e5ff4208.png)
![isaac_ZLJmv4O1KA](https://user-images.githubusercontent.com/104463209/215344306-8ae8b4fa-7bbd-4c11-aa13-40c14ed945e5.png)
![isaac_d6y5od8WbZ](https://user-images.githubusercontent.com/104463209/215344311-ae9b537e-16ad-4ad8-8a40-781df2877e44.png)
![isaac_hbMbEcGsDO](https://user-images.githubusercontent.com/104463209/215344317-f50f5e60-d73d-4c33-ab05-3f68c221e3dc.png)

### Пояснительная часть.
Проект "The Binding of Isaac: Python" был создан командой из трёх человек в рамках Лицея Академии Яндекса (Лесовым Кириллом, Дядечковым Иваном и Загитовым Ростиславом)\
Для реализации были применены библиотеки **pygame** (для рисования спрайтов и обработки коллизий) и **sqlite3** (для сохранения результатов пробегов).
