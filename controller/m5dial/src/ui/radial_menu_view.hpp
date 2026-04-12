#pragma once

#include "m5dial/ui_constants.hpp"
#include "../core/app_state.hpp"
#include <lvgl.h>

namespace m5dial {

class RadialMenuView {
public:
    void init(lv_obj_t* parent);
    void sync(const AppState& state);
    lv_obj_t* root() const { return root_; }

private:
    void snap_layout(int sel);
    void animate_transition(int from, int to);

    static void anim_x_cb(void* var, int32_t v);
    static void anim_y_cb(void* var, int32_t v);
    static void anim_zoom_cb(void* var, int32_t v);

    static constexpr int kItemCount = AppState::kMainMenuCount;

    lv_obj_t* root_{nullptr};
    lv_obj_t* disc_[kItemCount]{};
    lv_obj_t* icon_[kItemCount]{};
    lv_obj_t* title_label_{nullptr};

    int last_sel_{-1};
    UiLayer last_layer_{UiLayer::SubMenu};
};

} // namespace m5dial
