# M5Dial UI (cross-platform)

C++ / PlatformIO. **Desktop sim:** LVGL 8 + SDL2 (`env:native`). **Device:** `env:m5dial` (Arduino + M5Unified) — placeholder `setup`/`loop` until donanım tarafı bağlanır.

## Gereksinimler (macOS sim)

- Python 3 + PlatformIO: `pip3 install --user platformio`  
  (CLI genelde `~/Library/Python/3.9/bin` altında; `export PATH="$HOME/Library/Python/3.9/bin:$PATH"` veya aynı dizini PATH’e ekleyin.)
- SDL2: `brew install sdl2` (Apple Silicon: `/opt/homebrew`, Intel: `/usr/local`)

## Çalıştırma (simülatör)

```bash
cd controller/m5dial
pio run -e native
# Çıktı ikili dosyası genelde:
#   .pio/build/native/program
```

**Ana menü:** odaklı radial düzen — ortada tek **accent** daire (seçili), etrafta **3** soluk gri önizleme; border yok, `include/m5dial/ui_constants.hpp` içinden ölçü/renk ayarı.

- **← / →** — encoder sol / sağ (yalnızca ana menüde; 5 kategori arasında döner)
- **Enter (kısa basış, ~40–500 ms)** — seçili maddeye **alt menü** (şimdilik yer tutucu)
- **Enter (uzun basış, ≥500 ms)** veya **Esc** — alt menüden **ana menüye** dönüş

## M5Dial ekran (cihazla uyum)

- **240×240** mantıksal çözünürlük, **1.28" yuvarlak** TFT (GC9A01), dokunmatik FT3267 — sabitler: `include/m5dial_display.hpp`
- Simülatör: her kare sonunda daire dışı pikseller **çerçeve rengine** maskelenir (fiziksel panelde köşeler yok)
- UI: **~36px** iç boşluk — içerik dairenin “güvenli” orta alanında kalır

## Mimari

- `core/` — `AppEvent`, `AppState`, `EventQueue`
- `ui/` — `ScreenManager` (mantık), `Renderer` + `RadialMenuView` (LVGL), `include/m5dial/ui_constants.hpp` / `menu_strings.hpp`
- `hardware/` — `HardwareAdapter`; `SimAdapter` (SDL klavye), `M5DialAdapter` (cihaz — stub)
- `mqtt/` — `MqttClientMock`
- `platform/native/` — SDL2 ekran sürücüsü + `run_native_app()`

Donanım kodu ile iş mantığı ayrı; olaylar kuyruktan işlenir.
