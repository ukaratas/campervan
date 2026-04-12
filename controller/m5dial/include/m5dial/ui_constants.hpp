#pragma once

#include <lvgl.h>

namespace m5dial::ui {

struct RadialMenuStyle {
    static constexpr int kCenterX = 120;
    static constexpr int kCenterY = 102;

    static constexpr int kCenterDiameter = 90;
    static constexpr int kPreviewDiameter = 38;

    static constexpr int kOrbitOffset = 48;

    static constexpr int kTitleY = 180;

    static constexpr uint32_t kColorBg        = 0x0e1118;
    static constexpr uint32_t kColorAccent     = 0xd4a24e;
    static constexpr uint32_t kColorPreviewBg  = 0x384050;
    static constexpr uint32_t kColorPreviewIcon= 0x9098ac;
    static constexpr uint32_t kColorCenterIcon = 0x1a1a1a;
    static constexpr uint32_t kColorTitle      = 0x707888;

    static constexpr uint32_t kAnimMs          = 250;

    static constexpr int      kCenterShadowW   = 20;
    static constexpr lv_opa_t kCenterShadowOpa = LV_OPA_40;
};

} // namespace m5dial::ui
