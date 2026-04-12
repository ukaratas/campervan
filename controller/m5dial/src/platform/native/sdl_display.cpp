#include "sdl_display.hpp"
#include <lvgl.h>
#include <SDL.h>
#include <cstring>

namespace m5dial::platform {

namespace {

SDL_Window* window = nullptr;
SDL_Renderer* renderer = nullptr;
SDL_Texture* texture = nullptr;
uint32_t fb[kDispW * kDispH];

lv_disp_draw_buf_t draw_buf;
lv_color_t draw_buf_pixels[kDispW * kDispH];
lv_disp_drv_t disp_drv;

/** GC9A01 yuvarlak panel: kare buffer’da daire dışı pikseller cihazda görünmez — sim’de çerçeve rengi */
constexpr uint32_t kBezelArgb = 0xFF101010u;

void apply_round_bezel_to_fb() {
    const float cx = (static_cast<float>(kDispW) - 1.0f) * 0.5f;
    const float cy = (static_cast<float>(kDispH) - 1.0f) * 0.5f;
    const float r = m5dial::kRoundRadiusPx;
    const float r2 = r * r;
    for (int y = 0; y < kDispH; ++y) {
        for (int x = 0; x < kDispW; ++x) {
            const float dx = static_cast<float>(x) - cx;
            const float dy = static_cast<float>(y) - cy;
            if (dx * dx + dy * dy > r2) {
                fb[static_cast<size_t>(y) * kDispW + static_cast<size_t>(x)] = kBezelArgb;
            }
        }
    }
}

void flush_cb(lv_disp_drv_t* driver, const lv_area_t* area, lv_color_t* color_p) {
    for (lv_coord_t y = area->y1; y <= area->y2; y++) {
        for (lv_coord_t x = area->x1; x <= area->x2; x++) {
            fb[static_cast<size_t>(y) * kDispW + static_cast<size_t>(x)] = lv_color_to32(*color_p);
            color_p++;
        }
    }

    if (lv_disp_flush_is_last(driver)) {
        apply_round_bezel_to_fb();
        SDL_Rect r{0, 0, kDispW, kDispH};
        SDL_UpdateTexture(texture, &r, fb, static_cast<int>(kDispW * sizeof(uint32_t)));
        SDL_SetRenderDrawColor(renderer, 0x08, 0x08, 0x08, 0xFF);
        SDL_RenderClear(renderer);
        SDL_RenderCopy(renderer, texture, nullptr, nullptr);
        SDL_RenderPresent(renderer);
    }
    lv_disp_flush_ready(driver);
}

} // namespace

bool sdl_display_init() {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) < 0) {
        return false;
    }

    window = SDL_CreateWindow("M5Dial · 240×240 yuvarlak 1.28\" (GC9A01) sim", SDL_WINDOWPOS_CENTERED,
                              SDL_WINDOWPOS_CENTERED, 480, 480, SDL_WINDOW_ALLOW_HIGHDPI);
    if (!window) {
        return false;
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) {
        SDL_DestroyWindow(window);
        window = nullptr;
        return false;
    }

    SDL_RenderSetLogicalSize(renderer, kDispW, kDispH);

    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STATIC, kDispW, kDispH);
    if (!texture) {
        sdl_display_deinit();
        return false;
    }

    for (size_t i = 0; i < sizeof(fb) / sizeof(fb[0]); ++i) {
        fb[i] = kBezelArgb;
    }

    lv_init();

    lv_disp_draw_buf_init(&draw_buf, draw_buf_pixels, nullptr, kDispW * kDispH);
    lv_disp_drv_init(&disp_drv);
    disp_drv.hor_res = kDispW;
    disp_drv.ver_res = kDispH;
    disp_drv.flush_cb = flush_cb;
    disp_drv.draw_buf = &draw_buf;

    lv_disp_t* disp = lv_disp_drv_register(&disp_drv);
    if (!disp) {
        sdl_display_deinit();
        return false;
    }

    lv_theme_t* th = lv_theme_default_init(disp, lv_palette_main(LV_PALETTE_BLUE), lv_color_hex(0x888888), true,
                                           &lv_font_tr_14);
    lv_disp_set_theme(disp, th);

    return true;
}

void sdl_display_deinit() {
    if (texture) {
        SDL_DestroyTexture(texture);
        texture = nullptr;
    }
    if (renderer) {
        SDL_DestroyRenderer(renderer);
        renderer = nullptr;
    }
    if (window) {
        SDL_DestroyWindow(window);
        window = nullptr;
    }
    SDL_Quit();
}

} // namespace m5dial::platform
