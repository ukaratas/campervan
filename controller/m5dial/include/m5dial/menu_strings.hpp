#pragma once

#include <lvgl.h>

namespace m5dial::ui {

inline constexpr int kMainMenuTitleCount = 5;

/** Ana menü başlıkları */
inline constexpr const char* const kMainMenuTitles[] = {
    "Enerji",
    "Sensörler",
    "Işıklar",
    "İklim",
    "Ayarlar",
};

/** Merkez dairede gösterilecek FontAwesome ikonları */
inline constexpr const char* const kMainMenuIcons[] = {
    LV_SYMBOL_CHARGE,
    LV_SYMBOL_EYE_OPEN,
    LV_SYMBOL_TINT,
    LV_SYMBOL_REFRESH,
    LV_SYMBOL_SETTINGS,
};

/** Preview dairelerde gösterilecek küçük ikonlar (aynı set) */
inline constexpr const char* const kMainMenuIconsSmall[] = {
    LV_SYMBOL_CHARGE,
    LV_SYMBOL_EYE_OPEN,
    LV_SYMBOL_TINT,
    LV_SYMBOL_REFRESH,
    LV_SYMBOL_SETTINGS,
};

} // namespace m5dial::ui
