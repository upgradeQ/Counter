import obspython as S

__version__ = "1.2.0"


class TextContent:
    def __init__(self, source_name=None, text_string="This is default text", suffix=""):
        self.source_name = source_name
        self.counter_text = text_string  # prefix
        self.counter_suffix = suffix     # suffix
        self.counter = 0

    def update_text(self, prefix, suffix, counter_value=0):
        source = S.obs_get_source_by_name(self.source_name)
        settings = S.obs_data_create()
        if counter_value == 1:
            self.counter += 1
        if counter_value == -1:
            self.counter -= 1
        if counter_value == 0:
            self.counter = 0
        if isinstance(counter_value, str):
            self.counter = int(counter_value)

        self.text_string = f"{prefix}{self.counter}{suffix}"
        S.obs_data_set_string(settings, "text", self.text_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)


class Driver(TextContent):
    def increment(self):
        self.update_text(self.counter_text, self.counter_suffix, 1)

    def decrement(self):
        self.update_text(self.counter_text, self.counter_suffix, -1)

    def reset(self):
        self.update_text(self.counter_text, self.counter_suffix, 0)

    def do_custom(self, val):
        self.update_text(self.counter_text, self.counter_suffix, str(val))


class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = S.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        description = "Htk " + str(self._id)
        self.hotkey_id = S.obs_hotkey_register_frontend(
            "htk_id" + str(self._id), description, self.callback
        )
        S.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        self.hotkey_saved_key = S.obs_data_get_array(
            self.obs_data, "htk_id" + str(self._id)
        )
        S.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        self.hotkey_saved_key = S.obs_hotkey_save(self.hotkey_id)
        S.obs_data_set_array(
            self.obs_data, "htk_id" + str(self._id), self.hotkey_saved_key
        )
        S.obs_data_array_release(self.hotkey_saved_key)


class HotkeyDataHolder:
    htk_copy = None  # this attribute will hold instance of Hotkey


hotkeys_counter_1 = Driver()
hotkeys_counter_2 = Driver()

h01 = HotkeyDataHolder()
h02 = HotkeyDataHolder()
h03 = HotkeyDataHolder()
h11 = HotkeyDataHolder()
h12 = HotkeyDataHolder()
h13 = HotkeyDataHolder()
# ------------------------------------------------------------------------------


def callback_up1(pressed):
    if pressed:
        return hotkeys_counter_1.increment()


def callback_down1(pressed):
    if pressed:
        return hotkeys_counter_1.decrement()


def callback_custom1(*args):
    hotkeys_counter_1.do_custom(S.obs_data_get_int(args[2], "counter_1"))
    return True


def callback_reset1(pressed):
    if pressed:
        return hotkeys_counter_1.reset()


def callback_up2(pressed):
    if pressed:
        return hotkeys_counter_2.increment()


def callback_down2(pressed):
    if pressed:
        return hotkeys_counter_2.decrement()


def callback_reset2(pressed):
    if pressed:
        return hotkeys_counter_2.reset()


def callback_custom2(*args):
    hotkeys_counter_2.do_custom(S.obs_data_get_int(args[2], "counter_2"))
    return True


def script_description():
    return "COUNTER 2"


def script_update(settings):
    hotkeys_counter_1.source_name = S.obs_data_get_string(settings, "source1")
    hotkeys_counter_1.counter_text = S.obs_data_get_string(settings, "counter_text1")
    hotkeys_counter_1.counter_suffix = S.obs_data_get_string(settings, "counter_suffix1")

    hotkeys_counter_2.source_name = S.obs_data_get_string(settings, "source2")
    hotkeys_counter_2.counter_text = S.obs_data_get_string(settings, "counter_text2")
    hotkeys_counter_2.counter_suffix = S.obs_data_get_string(settings, "counter_suffix2")


def script_properties():
    props = S.obs_properties_create()

    # Counter 1 properties
    S.obs_properties_add_text(
        props, "counter_text1", "[1] Set counter prefix", S.OBS_TEXT_DEFAULT
    )
    S.obs_properties_add_text(
        props, "counter_suffix1", "[1] Set counter suffix", S.OBS_TEXT_DEFAULT
    )
    p = S.obs_properties_add_int(
        props, "counter_1", "Set custom value", -999999, 999999, 1
    )
    S.obs_property_set_modified_callback(p, callback_custom1)
    p1 = S.obs_properties_add_list(
        props,
        "source1",
        "[1]Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )

    # Counter 2 properties
    S.obs_properties_add_text(
        props, "counter_text2", "[2] Set counter prefix", S.OBS_TEXT_DEFAULT
    )
    S.obs_properties_add_text(
        props, "counter_suffix2", "[2] Set counter suffix", S.OBS_TEXT_DEFAULT
    )
    p = S.obs_properties_add_int(
        props, "counter_2", "Set custom value", -999999, 999999, 1
    )
    S.obs_property_set_modified_callback(p, callback_custom2)
    p2 = S.obs_properties_add_list(
        props,
        "source2",
        "[2]Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = S.obs_source_get_name(source)
                S.obs_property_list_add_string(p1, name, name)
                S.obs_property_list_add_string(p2, name, name)

        S.source_list_release(sources)
    return props


def script_load(settings):
    hotkeys_counter_1.counter = S.obs_data_get_int(settings, "counter1")
    hotkeys_counter_2.counter = S.obs_data_get_int(settings, "counter2")
    h01.htk_copy = Hotkey(callback_up1, settings, "count_up1")
    h02.htk_copy = Hotkey(callback_down1, settings, "count_down1")
    h03.htk_copy = Hotkey(callback_reset1, settings, "reset1")

    h11.htk_copy = Hotkey(callback_up2, settings, "count_up2")
    h12.htk_copy = Hotkey(callback_down2, settings, "count_down2")
    h13.htk_copy = Hotkey(callback_reset2, settings, "reset2")


def script_save(settings):
    S.obs_data_set_int(settings, "counter1", hotkeys_counter_1.counter)
    S.obs_data_set_int(settings, "counter2", hotkeys_counter_2.counter)
    for h in [h01, h02, h03, h11, h12, h13]:
        h.htk_copy.save_hotkey()


description = """
<h2>Version : {__version__}</h2>
<a href="https://github.com/upgradeQ/Obscounter"> Webpage </a>
<h3 style="color:orange">Authors</h3>
<a href="https://github.com/upgradeQ"> upgradeQ </a> <br>
""".format(
    **locals()
)


def script_description():
    print(description, "Released under MIT license")
    return description
