#pragma once

#include "../core/app_state.hpp"
#include "radial_menu_view.hpp"
#include <lvgl.h>

namespace m5dial {

class Renderer {
public:
    void init();
    void sync(const AppState& state);

private:
    lv_obj_t* round_cont_{nullptr};
    RadialMenuView radial_;

    lv_obj_t* sub_panel_{nullptr};
    lv_obj_t* sub_title_{nullptr};
    lv_obj_t* sub_hint_{nullptr};
};

} // namespace m5dial
