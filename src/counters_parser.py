from src.globals import UI_TIMEOUT
from src.navigation import Tabs, navigate
from src.utils import *


def parse(device, text):
    multiplier = 1
    text = text.replace(",", "")
    if "K" in text:
        text = text.replace("K", "")
        multiplier = 1000
    if "M" in text:
        text = text.replace("M", "")
        multiplier = 1000000
    try:
        count = int(float(text) * multiplier)
    except ValueError:
        print_timeless(COLOR_FAIL + "Cannot parse \"" + text + "\". Probably wrong language, will set English now." +
                       COLOR_ENDC)
        take_screenshot(device)
        _switch_to_english(device)
        raise LanguageChangedException()
    return count


def _switch_to_english(device):
    print(COLOR_OKGREEN + "Switching to English locale" + COLOR_ENDC)
    navigate(device, Tabs.PROFILE)
    print("Changing language in settings")

    action_bar = device(resourceId='com.instagram.android:id/action_bar',
                        className='android.widget.LinearLayout')
    options_view = action_bar.child(index=1)
    options_view.click(timeout=UI_TIMEOUT)

    settings_button = device(resourceId='com.instagram.android:id/menu_settings_row',
                             className='android.widget.TextView')
    settings_button.click(timeout=UI_TIMEOUT)

    for account_item_index in range(6, 9):
        list_view = device(resourceId='android:id/list',
                           className='android.widget.ListView')
        account_item = list_view.child(index=account_item_index)
        account_item.click(timeout=UI_TIMEOUT)

        list_view = device(resourceId='android:id/list',
                           className='android.widget.ListView')
        language_item = list_view.child(index=3)
        if not language_item.exists(timeout=UI_TIMEOUT):
            print(COLOR_FAIL + "Oops, went the wrong way" + COLOR_ENDC)
            device.press("back")
            continue
        language_item.click(timeout=UI_TIMEOUT)

        search_edit_text = device(resourceId='com.instagram.android:id/search',
                                  className='android.widget.EditText')
        if not search_edit_text.exists(timeout=UI_TIMEOUT):
            print(COLOR_FAIL + "Oops, went the wrong way" + COLOR_ENDC)
            device.press("back")
            device.press("back")
            continue
        search_edit_text.set_text("english")
        device.wait.idle()

        list_view = device(resourceId='com.instagram.android:id/language_locale_list',
                           className='android.widget.ListView')
        english_item = list_view.child(index=0)
        english_item.click(timeout=UI_TIMEOUT)

        break


class LanguageChangedException(Exception):
    pass
