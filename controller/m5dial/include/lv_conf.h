/**
 * LVGL 8.3 — minimal config for M5Dial / desktop sim (240×240 logical)
 */
#ifndef LV_CONF_H
#define LV_CONF_H

#include <stdint.h>

#define LV_COLOR_DEPTH 32
#define LV_COLOR_32_SWAP 0

#define LV_TICK_CUSTOM 0

#define LV_MEM_CUSTOM 0
#define LV_MEM_SIZE (128U * 1024U)

#define LV_USE_LOG 0

#define LV_USE_ASSERT_NULL 0
#define LV_USE_ASSERT_MALLOC 0

/* Gömülü Montserrat yalnızca ASCII; Türkçe için src/ui/fonts/lv_font_tr_*.c */
#define LV_FONT_MONTSERRAT_12 0
#define LV_FONT_MONTSERRAT_14 0
#define LV_FONT_CUSTOM_DECLARE LV_FONT_DECLARE(lv_font_tr_12) LV_FONT_DECLARE(lv_font_tr_14) LV_FONT_DECLARE(lv_font_tr_20)
#define LV_FONT_DEFAULT &lv_font_tr_14

#define LV_USE_PERF_MONITOR 0
#define LV_USE_MEM_MONITOR 0

#define LV_USE_THEME_DEFAULT 1

#define LV_USE_FLEX 1

#endif /* LV_CONF_H */
