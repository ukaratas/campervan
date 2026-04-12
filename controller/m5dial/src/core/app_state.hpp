#pragma once

#include <cstdint>

namespace m5dial {

/** Ana menü ↔ alt menü (içerik derinleşecek) */
enum class UiLayer : uint8_t {
    MainMenu = 0,
    SubMenu = 1,
};

struct AppState {
    static constexpr int kMainMenuCount = 5;

    UiLayer layer{UiLayer::MainMenu};
    /** 0..4 — açılışta her zaman 0 = (1) Aydınlatma */
    int main_menu_index{0};
};

} // namespace m5dial
