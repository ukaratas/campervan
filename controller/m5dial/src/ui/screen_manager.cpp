#include "screen_manager.hpp"

namespace m5dial {

void ScreenManager::handle_event(const AppEvent& e, AppState& state) {
    switch (e.type) {
    case AppEventType::EncoderLeft:
        if (state.layer == UiLayer::MainMenu) {
            state.main_menu_index =
                (state.main_menu_index + AppState::kMainMenuCount - 1) % AppState::kMainMenuCount;
        }
        break;
    case AppEventType::EncoderRight:
        if (state.layer == UiLayer::MainMenu) {
            state.main_menu_index = (state.main_menu_index + 1) % AppState::kMainMenuCount;
        }
        break;
    case AppEventType::ButtonPress:
        if (state.layer == UiLayer::MainMenu) {
            state.layer = UiLayer::SubMenu;
        }
        break;
    case AppEventType::LongPress:
        if (state.layer == UiLayer::SubMenu) {
            state.layer = UiLayer::MainMenu;
        }
        break;
    case AppEventType::Touch:
    case AppEventType::Tick:
    default:
        break;
    }
}

} // namespace m5dial
