#include <iostream>
#include <Windows.h>
#include <Winuser.h>
#include <conio.h>
#include <string>
#include <thread>
#include <chrono>

std::string previous_text = "";

void show_message_box() {
    std::string current_text;
    
    // Copy the highlighted text
    keybd_event(VK_CONTROL, 0, 0, 0);
    keybd_event('C', 0, 0, 0);
    keybd_event('C', 0, KEYEVENTF_KEYUP, 0);
    keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0);

    // Retrieve the copied text
    if (OpenClipboard(NULL)) {
        HANDLE clipboard_handle = GetClipboardData(CF_TEXT);
        char* clipboard_text = static_cast<char*>(GlobalLock(clipboard_handle));
        current_text = clipboard_text;
        GlobalUnlock(clipboard_handle);
        CloseClipboard();
    }

    if (!current_text.empty()) {
        // There is highlighted text
        if (current_text != previous_text) {
            // Show message box
            MessageBox(NULL, current_text.c_str(), "InstantGPT says:", MB_OK | MB_SETFOREGROUND);
        } else {
            // No highlighted text, open OpenAI website
            ShellExecute(NULL, "open", "https://chat.openai.com", NULL, NULL, SW_SHOWNORMAL);
        }
    }

    previous_text = current_text;
}

int main() {
    previous_text = "";
    bool running = true;
    
    // Start a separate thread for the hotkey listener
    std::thread hotkey_thread([&running]() {
        while (running) {
            if (_kbhit()) {
                int key = _getch();
                if (key == 27) { // ESC key
                    running = false;
                }
            }
        }
    });

    // Register the hotkey
    if (!RegisterHotKey(NULL, 1, MOD_CONTROL | MOD_SHIFT, 'O')) {
        std::cout << "Failed to register hotkey" << std::endl;
        return 1;
    }

    // Message loop to process hotkey messages
    MSG msg = { 0 };
    while (GetMessage(&msg, NULL, 0, 0) != 0 && running) {
        if (msg.message == WM_HOTKEY && msg.wParam == 
