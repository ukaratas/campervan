#include "radial_menu_view.hpp"
#include "m5dial/menu_strings.hpp"
#include "m5dial_display.hpp"

static_assert(m5dial::ui::kMainMenuTitleCount == m5dial::AppState::kMainMenuCount);

namespace m5dial {

using S = ui::RadialMenuStyle;

namespace {

struct SlotDef {
    int cx, cy, diameter;
    uint32_t bg_color, icon_color;
    const lv_font_t* font;
};

constexpr int kOff = S::kOrbitOffset;

/*
 *  Slot 0 = center (selected, large, accent)
 *  Slot 1 = NE   (next clockwise)
 *  Slot 2 = SE
 *  Slot 3 = SW
 *  Slot 4 = NW   (previous clockwise)
 *
 *  Item i occupies slot (i - selected + 5) % 5.
 */
const SlotDef kSlots[] = {
    {S::kCenterX,        S::kCenterY,        S::kCenterDiameter,
     S::kColorAccent,    S::kColorCenterIcon, &lv_font_tr_20},

    {S::kCenterX + kOff, S::kCenterY - kOff, S::kPreviewDiameter,
     S::kColorPreviewBg, S::kColorPreviewIcon, &lv_font_tr_14},

    {S::kCenterX + kOff, S::kCenterY + kOff, S::kPreviewDiameter,
     S::kColorPreviewBg, S::kColorPreviewIcon, &lv_font_tr_14},

    {S::kCenterX - kOff, S::kCenterY + kOff, S::kPreviewDiameter,
     S::kColorPreviewBg, S::kColorPreviewIcon, &lv_font_tr_14},

    {S::kCenterX - kOff, S::kCenterY - kOff, S::kPreviewDiameter,
     S::kColorPreviewBg, S::kColorPreviewIcon, &lv_font_tr_14},
};

int slot_for(int item, int sel) {
    return (item - sel + AppState::kMainMenuCount) % AppState::kMainMenuCount;
}

void apply_slot(lv_obj_t* disc, lv_obj_t* icon, const SlotDef& s) {
    const int h = s.diameter / 2;
    lv_obj_set_pos(disc, s.cx - h, s.cy - h);
    lv_obj_set_size(disc, s.diameter, s.diameter);
    lv_obj_set_style_radius(disc, h, LV_PART_MAIN);
    lv_obj_set_style_bg_color(disc, lv_color_hex(s.bg_color), LV_PART_MAIN);
    lv_obj_set_style_bg_opa(disc, LV_OPA_COVER, LV_PART_MAIN);
    lv_obj_set_style_text_color(icon, lv_color_hex(s.icon_color), LV_PART_MAIN);
    lv_obj_set_style_text_font(icon, s.font, LV_PART_MAIN);
    lv_obj_align(icon, LV_ALIGN_CENTER, 0, 0);

    lv_obj_set_style_transform_pivot_x(disc, h, LV_PART_MAIN);
    lv_obj_set_style_transform_pivot_y(disc, h, LV_PART_MAIN);
    lv_obj_set_style_transform_zoom(disc, 256, LV_PART_MAIN);

    const bool is_center = (s.diameter == S::kCenterDiameter);
    lv_obj_set_style_shadow_width(disc, is_center ? S::kCenterShadowW : 0, LV_PART_MAIN);
    if (is_center) {
        lv_obj_set_style_shadow_opa(disc, S::kCenterShadowOpa, LV_PART_MAIN);
        lv_obj_set_style_shadow_color(disc, lv_color_hex(S::kColorAccent), LV_PART_MAIN);
        lv_obj_set_style_shadow_ofs_y(disc, 2, LV_PART_MAIN);
    }
}

} // anonymous namespace

/* ── animation callbacks ───────────────────────────────────────── */

void RadialMenuView::anim_x_cb(void* var, int32_t v) {
    lv_obj_set_x(static_cast<lv_obj_t*>(var), static_cast<lv_coord_t>(v));
}
void RadialMenuView::anim_y_cb(void* var, int32_t v) {
    lv_obj_set_y(static_cast<lv_obj_t*>(var), static_cast<lv_coord_t>(v));
}
void RadialMenuView::anim_zoom_cb(void* var, int32_t v) {
    lv_obj_set_style_transform_zoom(static_cast<lv_obj_t*>(var),
                                    static_cast<lv_coord_t>(v), LV_PART_MAIN);
}

/* ── init ──────────────────────────────────────────────────────── */

void RadialMenuView::init(lv_obj_t* parent) {
    root_ = lv_obj_create(parent);
    lv_obj_set_size(root_, kDisplaySize, kDisplaySize);
    lv_obj_set_pos(root_, 0, 0);
    lv_obj_set_style_bg_opa(root_, LV_OPA_TRANSP, LV_PART_MAIN);
    lv_obj_set_style_border_width(root_, 0, LV_PART_MAIN);
    lv_obj_set_style_pad_all(root_, 0, LV_PART_MAIN);
    lv_obj_clear_flag(root_, LV_OBJ_FLAG_SCROLLABLE);

    for (int i = 0; i < kItemCount; i++) {
        disc_[i] = lv_obj_create(root_);
        lv_obj_set_style_border_width(disc_[i], 0, LV_PART_MAIN);
        lv_obj_clear_flag(disc_[i], LV_OBJ_FLAG_SCROLLABLE);

        icon_[i] = lv_label_create(disc_[i]);
        lv_label_set_text(icon_[i], ui::kMainMenuIcons[i]);
        lv_obj_align(icon_[i], LV_ALIGN_CENTER, 0, 0);
    }

    title_label_ = lv_label_create(root_);
    lv_obj_set_width(title_label_, 140);
    lv_label_set_long_mode(title_label_, LV_LABEL_LONG_WRAP);
    lv_obj_set_style_text_font(title_label_, &lv_font_tr_12, LV_PART_MAIN);
    lv_obj_set_style_text_color(title_label_, lv_color_hex(S::kColorTitle), LV_PART_MAIN);
    lv_obj_set_style_text_align(title_label_, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN);
    lv_obj_set_pos(title_label_, (kDisplaySize - 140) / 2, S::kTitleY);

    snap_layout(0);
}

/* ── snap (instant, no animation) ──────────────────────────────── */

void RadialMenuView::snap_layout(int sel) {
    for (int i = 0; i < kItemCount; i++) {
        lv_anim_del(disc_[i], nullptr);
        apply_slot(disc_[i], icon_[i], kSlots[slot_for(i, sel)]);
    }
    lv_label_set_text(title_label_, ui::kMainMenuTitles[sel]);
    lv_obj_move_foreground(disc_[sel]);
    lv_obj_move_foreground(title_label_);
}

/* ── animated transition ───────────────────────────────────────── */

void RadialMenuView::animate_transition(int from, int to) {
    for (int i = 0; i < kItemCount; i++) {
        lv_anim_del(disc_[i], nullptr);

        const int old_s = slot_for(i, from);
        const int new_s = slot_for(i, to);
        if (old_s == new_s) continue;

        const auto& src = kSlots[old_s];
        const auto& dst = kSlots[new_s];

        /* Apply destination style instantly (size, color, shadow, font) */
        const int dh = dst.diameter / 2;
        lv_obj_set_size(disc_[i], dst.diameter, dst.diameter);
        lv_obj_set_style_radius(disc_[i], dh, LV_PART_MAIN);
        lv_obj_set_style_bg_color(disc_[i], lv_color_hex(dst.bg_color), LV_PART_MAIN);
        lv_obj_set_style_bg_opa(disc_[i], LV_OPA_COVER, LV_PART_MAIN);
        lv_obj_set_style_text_color(icon_[i], lv_color_hex(dst.icon_color), LV_PART_MAIN);
        lv_obj_set_style_text_font(icon_[i], dst.font, LV_PART_MAIN);
        lv_obj_align(icon_[i], LV_ALIGN_CENTER, 0, 0);
        lv_obj_set_style_transform_pivot_x(disc_[i], dh, LV_PART_MAIN);
        lv_obj_set_style_transform_pivot_y(disc_[i], dh, LV_PART_MAIN);
        lv_obj_set_style_transform_zoom(disc_[i], 256, LV_PART_MAIN);

        const bool going_center = (new_s == 0);
        lv_obj_set_style_shadow_width(disc_[i], going_center ? S::kCenterShadowW : 0, LV_PART_MAIN);
        if (going_center) {
            lv_obj_set_style_shadow_opa(disc_[i], S::kCenterShadowOpa, LV_PART_MAIN);
            lv_obj_set_style_shadow_color(disc_[i], lv_color_hex(S::kColorAccent), LV_PART_MAIN);
            lv_obj_set_style_shadow_ofs_y(disc_[i], 2, LV_PART_MAIN);
        }

        /* Animate position: visual center travels from src → dst */
        const int from_x = src.cx - dh;
        const int from_y = src.cy - dh;
        const int to_x   = dst.cx - dh;
        const int to_y   = dst.cy - dh;

        lv_anim_t a;
        lv_anim_init(&a);
        lv_anim_set_var(&a, disc_[i]);
        lv_anim_set_time(&a, S::kAnimMs);
        lv_anim_set_path_cb(&a, lv_anim_path_ease_in_out);

        lv_anim_set_exec_cb(&a, anim_x_cb);
        lv_anim_set_values(&a, from_x, to_x);
        lv_anim_start(&a);

        lv_anim_set_exec_cb(&a, anim_y_cb);
        lv_anim_set_values(&a, from_y, to_y);
        lv_anim_start(&a);
    }

    lv_label_set_text(title_label_, ui::kMainMenuTitles[to]);
    lv_obj_move_foreground(disc_[to]);
    lv_obj_move_foreground(title_label_);

    /* Subtle zoom pulse on the new center disc */
    lv_anim_t pulse;
    lv_anim_init(&pulse);
    lv_anim_set_var(&pulse, disc_[to]);
    lv_anim_set_exec_cb(&pulse, anim_zoom_cb);
    lv_anim_set_values(&pulse, 272, 256);
    lv_anim_set_time(&pulse, 180);
    lv_anim_set_delay(&pulse, S::kAnimMs);
    lv_anim_set_path_cb(&pulse, lv_anim_path_ease_out);
    lv_anim_start(&pulse);
}

/* ── sync (called every tick) ──────────────────────────────────── */

void RadialMenuView::sync(const AppState& state) {
    if (state.layer != UiLayer::MainMenu) {
        last_layer_ = state.layer;
        return;
    }

    const int sel = state.main_menu_index;
    const bool need_snap = (last_layer_ != UiLayer::MainMenu) || (last_sel_ < 0);

    if (need_snap) {
        snap_layout(sel);
    } else if (sel != last_sel_) {
        animate_transition(last_sel_, sel);
    }

    last_sel_ = sel;
    last_layer_ = state.layer;
}

} // namespace m5dial
