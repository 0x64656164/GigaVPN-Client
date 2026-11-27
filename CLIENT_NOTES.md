# GigaVPN Client — заметки по ребрендингу и сборке

## 1. Фактический стек (важное отклонение от ТЗ)

Официальный репозиторий `WhiteDNS/WhiteVPN` **не является Flutter-проектом**. Это нативное
Android-приложение на Kotlin + Android Views, Gradle (AGP), JDK 21, Android SDK 36/NDK 29
и ядре Mihomo/FlClash. Поэтому:

| Требование ТЗ | Реализация в форке |
|---|---|
| `android/app/src/main/AndroidManifest.xml` | `app/src/main/AndroidManifest.xml`, `android:label="GigaVPN"` |
| `android/app/build.gradle` → `applicationId` | `app/build.gradle.kts` → `applicationId = "com.gigavpn.client"` |
| `pubspec.yaml` | отсутствует; имя/описание заданы в `settings.gradle.kts`, `README.md`, `strings.xml` |
| `FlutterThemeData / ColorScheme` | `res/values/colors.xml`, `values-night/colors.xml`, `DashboardViews.kt`, `tokens.css` |
| `assets/config/app_config.json` + `pubspec assets` | `assets/config/app_config.json` + `sourceSets` подключает корневой `assets/` как источник Android assets |
| `flutter build apk --release --split-per-abi` | `./scripts/release.sh` → `:app:assembleRelease` с `splits.abi` (universal + 4 ABI) |
| Java 17 | JDK **21** (AGP/compileSdk 36 требует 21; `sourceCompatibility` остаётся Java 17) |

Локально Flutter/Android SDK **не устанавливались** и сборка не выполнялась — только облачный CI.

## 2. Что изменено

- **Идентичность**: `applicationId=com.gigavpn.client`, `rootProject.name=GigaVPN`, label `GigaVPN`,
  пользовательские строки переведены на бренд GigaVPN; доступны два языка: русский (по умолчанию)
  и английский (`values-ru`, `values`). Фарси удалён полностью.
- **Пакет Kotlin** оставлен `com.whitedns.vpn` намеренно: это `namespace` AGP, от него зависят
  `R`-класс, manifest-ссылки `.WhiteDnsApplication` и ProGuard-правила. `applicationId` при этом
  изменён на `com.gigavpn.client` — для пользователя и Google Play это и есть идентификатор приложения.
- **Цвета**: акцент `#9B51E0` (светлая тема) / `#C084FC` (тёмная), градиент `#9B51E0 → #A855F7`,
  мягкие фиолетовые фоны `#F7F3FB` / `#0D0714`. Палитра задана в XML и продублирована в
  `WhiteDnsDesignTokens` (Kotlin), чтобы програмные View использовали тот же акцент.
- **Иконка**: сгенерирована скриптом `scripts/generate_gigavpn_icon.py` (Pillow) — щит с буквой G
  на тёмно-фиолетовом фоне. Обновлены adaptive icon, legacy mipmap WebP всех плотностей,
  иконка уведомления и TV-баннер.
- **Один профиль и токен**: вкладки «Профили» и самого списка профилей больше нет — нижняя
  навигация содержит только «Настройки» и «VPN». Экран подписки удалён; выбранная подписка
  отображается в настройках, а токен вводится в диалоге при нажатии «Подключить».
  Подсказка под полем ввода токена удалена.
  После успешной активации подключение продолжается автоматически. Токен сохраняется в
  `gigavpn_access_token` и проверяется regex, затем склеивается с `baseSubscriptionUrl`
  из `assets/config/app_config.json` и передаётся в `UserSubscriptionManager`.
  Встроенный источник только один: `whitevpn-private`; старый публичный источник остался
  только для чтения legacy-кэша.
- **Локальный прокси закрыт**: режим Proxy (прозрачный прокси для приложений устройства)
  скрыт и принудительно нормализуется в VPN. LAN-доступ всегда требует имя пользователя и
  сгенерированный пароль; `skip-auth-prefixes: 127.0.0.0/8` удалён — тот же пароль используется
  и для внутренних HTTPS-проб приложения (`LocalProxyAuth`), поэтому другое приложение на
  устройстве не может беспрепятственно пользоваться mixed-port.
- **Обновления**: проверка GitHub Releases переведена на `0x64656164/GigaVPN-Client`;
  поддерживаются `GigaVPN.apk` (universal) и `GigaVPN-V<version>-<abi>.apk`.
- **Тесты**: `WhiteDnsDesignTokensTest` обновлён под фиолетовую палитру GigaVPN — старые
  проверки ожидали зелёный акцент WhiteDNS и падали в CI. Остальные 385 тестов проходят без правок.

## 3. Конфигурация подключения

Файл `assets/config/app_config.json` — единственное место, где меняется адрес подписки:

```json
{
  "baseSubscriptionUrl": "https://gigavpn.example.com/sub/"
}
```

Перед пушем в `main` отредактируйте этот файл под свой домен. Каталог `assets/` подключён
через `sourceSets` как ещё один источник Android assets, поэтому отдельная задача копирования
не нужна. Токен выдаёт Telegram-бот (раздел бота «Личный кабинет»).

## 4. CI/CD

Workflow: `.github/workflows/build_apk.yml`.

1. Триггеры: `push` в `main`, тег `v*`, `workflow_dispatch`.
2. Параллельно собираются нативный ядро Mihomo/FlClash и три группы движков (Go + NDK, кэш actions/cache).
3. Устанавливаются JDK 21, Android SDK 36, build-tools, CMake 3.22.1, NDK 29.
4. Создаётся демо-ключ подписи (для продакшена нужно подключить repository secrets).
5. `scripts/release.sh` запускает тесты, `:app:assembleRelease`, `:app:bundleRelease`,
   переименовывает APK в `GigaVPN-V<version>-<abi>.apk`, проверяет подпись и пишет `SHA256SUMS`.
6. Универсальный APK копируется в `GigaVPN.apk`, публикуется в Artifacts и в GitHub Releases
   через `softprops/action-gh-release@v2`.

Старый `.github/workflows/android.yml` оставлен только для проверки Pull Request.

## 5. Проверка сборки

После пуша:

```bash
gh run list --workflow build_apk.yml
gh run view <run-id> --log
```

Или через REST API:

```bash
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/0x64656164/GigaVPN-Client/actions/runs?per_page=5
```

Готовый APK: https://github.com/0x64656164/GigaVPN-Client/releases/latest

## 6. Лицензия

Fork сохраняет GPL-3.0-only upstream-лицензию и авторские уведомления Third-party компонентов.
