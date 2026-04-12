#pragma once

#include <cstdint>
#include "m5dial_display.hpp"

namespace m5dial::platform {

static constexpr uint16_t kDispW = m5dial::kDisplaySize;
static constexpr uint16_t kDispH = m5dial::kDisplaySize;

/** SDL2 + LVGL display (native sim only) */
bool sdl_display_init();
void sdl_display_deinit();

} // namespace m5dial::platform
