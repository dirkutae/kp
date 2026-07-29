# Citrus KP — iOS

Нативная iOS-обёртка (SwiftUI + WKWebView) над калькулятором `index.html` из корня репозитория.
Страница и логотип встроены в бандл приложения, поэтому калькулятор открывается офлайн; сетевые
запросы идут только к `WORKER_URL` (сохранение КП) и в браузере по кнопке «Ссылка КП».

## Структура

```
CitrusKP.xcodeproj/       — проект Xcode
CitrusKP/
  CitrusKPApp.swift       — точка входа
  ContentView.swift       — корневой экран
  WebView.swift           — обёртка WKWebView, грузит Resources/index.html
  Resources/index.html    — копия сайта (обновляется вручную при изменении корневого index.html)
  Resources/logo.png      — логотип, используемый в index.html
  Info.plist
  Assets.xcassets
```

## Сборка

1. Откройте `CitrusKP.xcodeproj` в Xcode 15+.
2. Выберите таргет `CitrusKP`, симулятор или устройство (iOS 16+).
3. Cmd+R — запуск.

Bundle ID по умолчанию — `com.citrushall.kp`, при необходимости смените в настройках таргета
и включите свою команду подписи (Signing & Capabilities).

## Обновление контента

Приложение не тянет сайт по сети — при изменении `index.html`/`logo.png` в корне репозитория
скопируйте их заново в `CitrusKP/Resources/` и пересоберите приложение:

```
cp ../../index.html CitrusKP/Resources/index.html
cp ../../logo.png    CitrusKP/Resources/logo.png
```

## Известные ограничения

- Верстка `index.html` рассчитана на компактный виджет (`height: 100vh; overflow: hidden`),
  поэтому на очень маленьких экранах (iPhone SE и меньше) нижняя часть списка залов может
  обрезаться. Сама разметка сайта не менялась — приложение показывает её как есть.
- Копирование в буфер (`navigator.clipboard.writeText`) работает из `WKWebView` при пользовательском
  жесте (тап по кнопке), как и в Safari; на случай сбоя в `index.html` уже есть фолбэк через
  `document.execCommand('copy')`.
