# GigaVPN for Android

> This repository is the GigaVPN fork of WhiteVPN (GPL-3.0). It is a **native Kotlin/Android**
> application built with Gradle — not a Flutter project. See [CLIENT_NOTES.md](CLIENT_NOTES.md)
> for the rebranding map, subscription configuration and CI/CD details.

[![Latest release](https://img.shields.io/github/v/release/0x64656164/GigaVPN-Client?label=download)](https://github.com/0x64656164/GigaVPN-Client/releases/latest)
[![License: GPL v3](https://img.shields.io/badge/license-GPL--3.0--only-blue.svg)](LICENSE)

<p>
  <a href="https://whitedns.github.io/GigaVPN-F-Droid/">
    <img src="https://f-droid.org/assets/fdroid-logo.svg" alt="" width="40" align="middle">
    <strong>Add the GigaVPN repository to F-Droid</strong>
  </a>
</p>

A simple, open-source Android VPN client powered by [Mihomo](https://github.com/MetaCubeX/mihomo). GigaVPN uses one private subscription activated by a token from the Telegram bot.

## Features

- One-tap **VPN** connection with no proxy-mode switch
- Single `GigaVPN Private` subscription with token activation and offline cache
- Manual server selection plus latency and download-speed tests
- Subscription, Iran-bypass and global-proxy routing modes
- Split tunnelling: bypass selected apps or proxy only selected apps
- Automatic DNS, DNS over HTTPS (DoH) and DNS over TLS (DoT)
- Clean-IP scanning, optional ByeDPI compatibility and authenticated LAN sharing
- Russian and English interfaces with system, light and dark themes

## Supported methods and inputs

Share links:

- VLESS
- VMess
- Trojan
- Shadowsocks (`ss://`)
- Hysteria 2 (`hysteria2://` and `hy2://`)
- WireGuard, including supported AmneziaWG options

Subscriptions can be added as an HTTPS URL or pasted directly. GigaVPN accepts plain or Base64-encoded link lists, Mihomo YAML, Clash JSON, and Xray JSON arrays. Clash JSON supports VLESS, VMess, Trojan, Shadowsocks and WireGuard entries; Xray JSON supports VLESS, VMess, Trojan and WireGuard outbounds.

## Built-in subscription

GigaVPN exposes one subscription, `GigaVPN Private`. The token issued by the Telegram bot is appended to `baseSubscriptionUrl` from `assets/config/app_config.json`; the app then loads the subscription automatically. The former public subscription constant is kept only for reading legacy cached data and is not selectable.

Set `baseSubscriptionUrl` to your own HTTPS endpoint before building. CI checks that the value uses HTTPS. The separate build-time `WHITEDNS_MIHOMO_SUBSCRIPTION_URL` and `WHITEDNS_PRIVATE_MIHOMO_SUBSCRIPTION_URL` variables remain for the legacy resolver, but the token flow uses `assets/config/app_config.json`.

## Community

- Telegram channel: [@whitedns](https://t.me/whitedns)
- Telegram group: [@whitedns_group](https://t.me/whitedns_group)

## Install

Download the latest APK from [GitHub Releases](https://github.com/0x64656164/GigaVPN-Client/releases/latest). GigaVPN requires Android 8.0 (API 26) or newer.

## Build

Requirements: JDK 21, Go, Android SDK and Android NDK.

```bash
./scripts/build-flclash-core.sh
./gradlew testDebugUnitTest assembleDebug
```

The build script checks out the pinned [`GigaVPN/FlClash`](https://github.com/GigaVPN/FlClash/tree/whitedns) integration and its pinned [`GigaVPN/mihomo`](https://github.com/GigaVPN/mihomo/tree/whitedns) core, builds Mihomo v1.19.34 for all supported Android ABIs, and generates the JNI files consumed by the app.

## Third-party software

- [GigaVPN/mihomo](https://github.com/GigaVPN/mihomo/tree/whitedns) — maintained proxy-core fork
- [GigaVPN/FlClash](https://github.com/GigaVPN/FlClash/tree/whitedns) — maintained Android core/JNI integration fork
- [SubConv](https://github.com/SubConv/SubConv) — adapted share-link conversion logic
- [ByeDPI](https://github.com/hufrea/byedpi) — optional DPI-bypass compatibility
- AndroidX, Material Components, Kotlin Coroutines and Firebase Analytics

Their respective licenses and notices continue to apply.

## Contributing

Issues and pull requests are welcome. Keep changes focused, avoid committing subscriptions or secrets, and run the local checks before opening a PR:

```bash
./gradlew testDebugUnitTest assembleDebug
git diff --check
```

Please describe what changed, why it is needed, and what you tested.

## License

GigaVPN is licensed under [GPL-3.0-only](LICENSE).
