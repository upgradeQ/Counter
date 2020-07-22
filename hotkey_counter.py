import obspython as obs


class TextContent:
    def __init__(self, source_name=None, text_string="This is default text"):
        self.source_name = source_name
        self.text_string = text_string
        self.counter = 0

    def update_text(self, counter_text, counter_value=0):
        source = obs.obs_get_source_by_name(self.source_name)
        settings = obs.obs_data_create()
        if counter_value == 1:
            self.counter += 1
        if counter_value == -1:
            self.counter -= 1
        if counter_value == 0:
            self.counter = 0
        self.text_string = f"{counter_text}{self.counter}"

        obs.obs_data_set_string(settings, "text", self.text_string)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)


class Driver(TextContent):
    def increment(self):
        self.update_text(self.counter_text, 1)

    def decrement(self):
        self.update_text(self.counter_text, -1)

    def reset(self):
        self.update_text(self.counter_text, 0)


class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = obs.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        description = "Htk " + str(self._id)
        self.hotkey_id = obs.obs_hotkey_register_frontend(
            "htk_id" + str(self._id), description, self.callback
        )
        obs.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        self.hotkey_saved_key = obs.obs_data_get_array(
            self.obs_data, "htk_id" + str(self._id)
        )
        obs.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        self.hotkey_saved_key = obs.obs_hotkey_save(self.hotkey_id)
        obs.obs_data_set_array(
            self.obs_data, "htk_id" + str(self._id), self.hotkey_saved_key
        )
        obs.obs_data_array_release(self.hotkey_saved_key)


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


def script_description():
    return "COUNTER 2"


def script_update(settings):
    hotkeys_counter_1.source_name = obs.obs_data_get_string(settings, "source1")
    hotkeys_counter_1.counter_text = obs.obs_data_get_string(settings, "counter_text1")

    hotkeys_counter_2.source_name = obs.obs_data_get_string(settings, "source2")
    hotkeys_counter_2.counter_text = obs.obs_data_get_string(settings, "counter_text2")


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(
        props, "counter_text1", "[1]Set counter text", obs.OBS_TEXT_DEFAULT
    )

    p1 = obs.obs_properties_add_list(
        props,
        "source1",
        "[1]Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )

    obs.obs_properties_add_text(
        props, "counter_text2", "[2]Set counter text", obs.OBS_TEXT_DEFAULT
    )
    p2 = obs.obs_properties_add_list(
        props,
        "source2",
        "[2]Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p1, name, name)
                obs.obs_property_list_add_string(p2, name, name)

        obs.source_list_release(sources)
    return props


def script_load(settings):
    h01.htk_copy = Hotkey(callback_up1, settings, "count_up1")
    h02.htk_copy = Hotkey(callback_down1, settings, "count_down1")
    h03.htk_copy = Hotkey(callback_reset1, settings, "reset1")

    h11.htk_copy = Hotkey(callback_up2, settings, "count_up2")
    h12.htk_copy = Hotkey(callback_down2, settings, "count_down2")
    h13.htk_copy = Hotkey(callback_reset2, settings, "reset2")


def script_save(settings):
    for h in [h01, h02, h03, h11, h12, h13]:
        h.htk_copy.save_hotkey()
