# Swift

A desktop music player for YouTube Music, built with **Qt 6, Qt Quick (QML) and C++20**.

Swift has a clean, Apple Music-inspired interface: a full-height sidebar with search, a top toolbar
with transport controls and a now-playing display, striped song tables, an Up Next panel and a
full-screen player. It runs on Linux and Windows and plays music from YouTube Music without a browser.

> **Unofficial project.** Swift is not affiliated with, endorsed by, or sponsored by Google,
> YouTube, YouTube Music or Apple. It uses no Apple assets: every icon is drawn in code.

<!-- Add screenshots here:
![Swift home screen](docs/screenshots/home.png)
-->

## Features

- **Browse and search** YouTube Music: home feed, songs, albums, artists and playlists
- **Playback queue** with Up Next, shuffle, repeat and restoring your last session
- **Your account playlists**: sign in once and see, create, rename, edit, reorder and delete your
  real YouTube Music playlists (changes sync back to YouTube Music)
- **Private sign-in**: an isolated in-app Google sign-in window; your session is stored in the
  operating system's credential vault (QtKeychain), never in plain text
- **Customizable look**: light, dark or system theme, accent colors, optional custom window
  buttons, docked or floating player bar, a "Liquid Glass" player bar shader
- **System tray** support, likes, recently played, and an on-disk artwork cache
- **Replaceable backend**: all music data goes through a `MusicProvider` interface, so another
  service can be plugged in

## How it works

- All networking is in C++. QML only sees a small set of objects (`player`, `library`,
  `playlists`, `account`, `settings`, and so on).
- Music data comes from YouTube Music's **unofficial InnerTube API**.
- For most tracks, playback needs a **stream resolver**. Swift runs
  [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) (configurable in *Settings > Network*) to get an
  audio URL, then plays it with Qt Multimedia. Without it, browsing and search still work.

## Download

Releases are on the [Releases](../../releases) page.

- **Linux:** `Swift-x86_64.AppImage`. Built on Arch Linux, so it targets Arch and other recent
  distributions. Run `chmod +x Swift-x86_64.AppImage && ./Swift-x86_64.AppImage`. It needs
  FUSE 2 (`libfuse2`), or run it with `--appimage-extract-and-run`. To pin it to a dock or add it
  to your launcher, use a tool such as Gear Lever or AppImageLauncher.
- **Windows:** build from source (see below).

You also need `yt-dlp` on your `PATH`, or set its path in *Settings > Network*, to play most tracks.

## Build from source

Requirements:

- Qt **6.5+** with Core, Gui, Qml, Quick, QuickControls2, Network, Multimedia, Widgets, ShaderTools,
  WebEngineCore and WebEngineWidgets
- CMake 3.21+ and a C++20 compiler (GCC 11+, Clang 14+, MSVC 2022)
- [QtKeychain](https://github.com/frankosterfeld/qtkeychain) (Arch: `qtkeychain-qt6`,
  Debian/Ubuntu: `qtkeychain-qt6-dev`)
- Optional but recommended: `yt-dlp`

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/SwiftApp          # build\Release\SwiftApp.exe on Windows
```

Useful options:

| Option | Effect |
|---|---|
| `-DSWIFT_ENABLE_EMBEDDED_LOGIN=OFF` | Build without Qt WebEngine (smaller; sign in by importing a session instead) |
| `-DSWIFT_REQUIRE_SECURE_SESSION_STORE=OFF` | Development only: allows building without QtKeychain; sessions then live in memory only |
| `-DCMAKE_PREFIX_PATH=/path/to/Qt/6.x/<kit>` | Point CMake at a specific Qt install |

## Project layout

```text
src/api/        MusicProvider interface, YouTubeMusicClient (InnerTube requests and parsers)
src/models/     SongModel, QueueModel, CollectionModel
src/playback/   MusicPlayer: queue, shuffle/repeat, session restore
src/services/   Account, Playlist, Settings, Library, Cache, System tray
qml/            Main.qml, theme, reusable components and pages
docs/           YouTube Music integration notes and validation report
```

## Linux notes

- Works on **Wayland and X11**. Tested on Hyprland.
- The window class is `SwiftApp`; use it in window rules.
- Saved sign-in needs a Secret Service provider (GNOME Keyring, KWallet, and so on).

## Legal notice

Swift uses undocumented YouTube Music endpoints and stream extraction. This may conflict with
YouTube's Terms of Service, and the endpoints can change without notice. You are responsible for how
you use it. Do not use it to download or redistribute content you do not have rights to.

## Status

Not yet implemented: OS media controls (MPRIS, media keys), tray notifications, and automated tests for live API behavior.

## License

Add your license here (for example MIT or GPL-3.0). If you distribute builds that bundle FFmpeg
(Qt Multimedia's FFmpeg backend), Qt or Chromium (WebEngine), follow their license terms and list them
under third-party notices.
