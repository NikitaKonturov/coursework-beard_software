#                                    Курсовая работа
##                               Требования по клинкоду

1. Функции и методы `snake_case`, классы `PascalCase`, переменные `camelCase`;
2. Решение задачи оформлять в отдельной папке с модулем CMake;
3. Пушить файл `main.cpp` не надо;
4. Все файлы классов функций должны быть логически разбиты по папкам;
5. Платформа на которой работаем `Windows`;
6. Комментируем отдельные участки кода, все сомнительные места, над каждым классом и функцией комментарии на русском что это такое
7. Адекватные и информативные названия переменных
8. Перед пушем точно убедитесь что нет ни каких багов
9. Прошу добросовестно отнестись к заданиям

## Задания каждому

|  Сотрудник | Задание                                     |
|------------|---------------------------------------------|
| Вруновский | Конвертирование .doc в .txt                 |
| Дегтяренко | Вывод результатов в .doc                    |
|  Контуров  | Qt реализация окна и интерфейса             |
|  Стариков  | Класс матрица                               |
|   Юрков    | Выбор ключей из словаря .txt                |
|   Рубец    | Выборка телеграмм из открытого текста       |
|   Дрозд    | Класс подстановок                           |         

## Небольшой туториал как вообще работать с CMake и git на Windows

Для работы с git вам надо скачать его с [официального сайта](https://git-scm.com/downloads/win) 
- Производите установку следуя простым инструкциям установщика;
- **ВАЖНЫЙ ПУНКТ** Для работы c git через косоль "как на Linux" необходимо добавить в переменную среды PATH путь к папке гита;

1. Заходите в меню пуск вводите изменеие системных переменных сред;
2. Выбираете перменные среды;
3. В окне переменные среды пользователя кликаете на переменную PATH и выбираете изменить; 
4. Вводите туда путь к папке `path\to\folder\Git\bin` вместо `path\to\folder` указываете путь своей папке куда установили git;
5. Перезагружаете компьютер;

- Далее устанавливаем [СMake](https://cmake.org/download/) и также добавляем его в переменную среды PATH;
- В качестве среды разработки рекомендую использовать VS code;
- C его установкой думаю все справяться;
- В нём уже качаем плагины `С/С++ Extension Pack`, `CMake`, `CMake Language Support`, `CMake Tools`;
- Далее для большего удобства скачиваете файл `configuration_cpp_project.bat` он будет в этом репозитории в папке tools 
- этот файл помещаем в какую нибудь папку на своём компьютере и добавляем путь к этой папке в PATH
- теперь дабы создать начальный проек в vs code
    1. Нужно создать папку c именем проекта 
    2. Открываете её в vs code 
    3. Открываете терминал и вводите команду `configuration_cpp_project`

## Рассмотрим синтаксис CMake

В начальном проекте если рассматривать CMakeLists.txt
мы увидем следующий код 
```
cmake_minimum_required(VERSION 3.10)

project(project_name)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

add_executable(project_name src/main.cpp)

```
`cmake_minimum_required(VERSION 3.10)` в этой строчке мы объявляем версию CMake которую мы используем для сборки для проекта
`project(project_name)` эта функция объявляет основной модуль нашей программы
`set(CMAKE_CXX_STANDARD 20)` задаём стандарт с++ который используем при сборке
`set(CMAKE_CXX_STANDARD_REQUIRED TRUE)` выставляем флаг на обязательное использование определённого стандарта языка C++ в проекте
`add_executable(project_name src/main.cpp)` указываем на необходимость создание исполняемого файла где `project_name` имя будущего .exe файла, `src/main.cpp` путь к ресурсным файлам

Так как нам придёться создавать многофайловый проект то нам необходимо в каждой папке классе прописывать свой CMakeLists.txt "как MODEULE.bazel в Bazel"
Он отличаеться от основного CMakeLists.txt 

Мы попрежнему прописываем `cmake_minimum_required(VERSION 3.10)`
далее создаём библиотеку `add_library(library_name library_file.cpp)`
указываем директорию для поиска заголовочных файлов `target_include_directories(library_name PUBLIC{CMAKE_CURRENT_SOURCE_DIR})`

Для подключения этой библиотеки в другой CMaleLists.txt в том числе и к главному модулю
необходимо добавить строчки 
`add_subdirectory("path\to\library\folder" "${CMAKE_BINARY_DIR}/library_name")` добавляем поддиректорию в основной проект в которых находяться свои собственные CMakeLists.txt, путь к основной папке библиотеке указываеться относительно той папки в которой применяеться эта команда
`target_link_libraries(this_module library_module)` эта строка подключает библиотеку непосредственно к самому модулю где вместо `this_module` мы прописываем название того модуля к которому подключаем библиотеку, в `library_module` название модуля подключаемой библиотеки 
















