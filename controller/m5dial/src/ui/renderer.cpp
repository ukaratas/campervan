#include "renderer.hpp"
#include "m5dial/menu_strings.hpp"
#include "m5dial/ui_constants.hpp"
#include "m5dial_display.hpp"
#include <lvgl.h>

namespace m5dial {

void Renderer::init() {
    lv_obj_t* scr = lv_scr_act();
    lv_obj_set_style_bg_color(scr, lv_color_hex(0x000000), LV_PART_MAIN);
    lv_obj_set_size(scr, LV_PCT(100), LV_PCT(100));
    lv_obj_set_style_pad_all(scr, 0, LV_PART_MAIN);
    lv_obj_clear_flag(scr, LV_OBJ_FLAG_SCROLLABLE);

    round_cont_ = lv_obj_create(scr);
    lv_obj_set_size(round_cont_, kDisplaySize, kDisplaySize);
    lv_obj_set_pos(round_cont_, 0, 0);
    lv_obj_set_style_radius(round_cont_, kDisplaySize / 2, LV_PART_MAIN);
    lv_obj_set_style_clip_corner(round_cont_, true, LV_PART_MAIN);
    lv_obj_set_style_bg_color(round_cont_, lv_color_hex(ui::RadialMenuStyle::kColorBg), LV_PART_MAIN);
    lv_obj_set_style_bg_opa(round_cont_, LV_OPA_COVER, LV_PART_MAIN);
    lv_obj_set_style_pad_all(round_cont_, 0, LV_PART_MAIN);
    lv_obj_set_style_border_width(round_cont_, 1, LV_PART_MAIN);
    lv_obj_set_style_border_color(round_cont_, lv_color_hex(0x2a2a2a), LV_PART_MAIN);
    lv_obj_clear_flag(round_cont_, LV_OBJ_FLAG_SCROLLABLE);

    radial_.init(round_cont_);

    sub_panel_ = lv_obj_create(round_cont_);
    lv_obj_set_size(sub_panel_, kDisplaySize, kDisplaySize);
    lv_obj_set_pos(sub_panel_, 0, 0);
    lv_obj_set_style_pad_all(sub_panel_, 40, LV_PART_MAIN);
    lv_obj_set_style_bg_color(sub_panel_, lv_color_hex(ui::RadialMenuStyle::kColorBg), LV_PART_MAIN);
    lv_obj_set_style_bg_opa(sub_panel_, LV_OPA_COVER, LV_PART_MAIN);
    lv_obj_set_style_border_width(sub_panel_, 0, LV_PART_MAIN);
    lv_obj_clear_flag(sub_panel_, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_add_flag(sub_panel_, LV_OBJ_FLAG_HIDDEN);

    sub_title_ = lv_label_create(sub_panel_);
    lv_label_set_long_mode(sub_title_, LV_LABEL_LONG_WRAP);
    lv_obj_set_width(sub_title_, LV_PCT(100));
    lv_obj_set_style_text_font(sub_title_, &lv_font_tr_14, LV_PART_MAIN);
    lv_obj_set_style_text_color(sub_title_, lv_color_hex(0xececf0), LV_PART_MAIN);
    lv_obj_set_style_text_align(sub_title_, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN);
    lv_obj_align(sub_title_, LV_ALIGN_CENTER, 0, -10);

    sub_hint_ = lv_label_create(sub_panel_);
    lv_label_set_long_mode(sub_hint_, LV_LABEL_LONG_WRAP);
    lv_obj_set_width(sub_hint_, LV_PCT(100));
    lv_label_set_text(sub_hint_, "Geri: uzun bas / Esc");
    lv_obj_set_style_text_color(sub_hint_, lv_color_hex(0x606070), LV_PART_MAIN);
    lv_obj_set_style_text_font(sub_hint_, &lv_font_tr_12, LV_PART_MAIN);
    lv_obj_set_style_text_align(sub_hint_, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN);
    lv_obj_align(sub_hint_, LV_ALIGN_CENTER, 0, 20);
}

void Renderer::sync(const AppState& state) {
    radial_.sync(state);

    if (state.layer == UiLayer::MainMenu) {
        lv_obj_clear_flag(radial_.root(), LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(sub_panel_, LV_OBJ_FLAG_HIDDEN);
    } else {
        lv_obj_add_flag(radial_.root(), LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(sub_panel_, LV_OBJ_FLAG_HIDDEN);
        lv_label_set_text(sub_title_, ui::kMainMenuTitles[state.main_menu_index]);
    }
}

} // namespace m5dial
