import obspython as obs


class TextContent:
    def __init__(self, text_string="This is default text", source_name=None):
        self.source_name = source_name
        self.text_string = text_string

    def update_text(self, counter_text, counter_value=0):
        source = obs.obs_get_source_by_name(self.source_name)
        settings = obs.obs_data_create()
        self.counter += 1
        if counter_value < 0:
            self.counter = 0
        self.text_string = f"{counter_text}{self.counter}"
        obs.obs_data_set_string(settings, "text", self.text_string)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)


class Driver(TextContent):
    def __init__(self, source_name, text_string):
        self.text_string = text_string
        self.counter_text = "counter text"
        self.source_name = source_name
        self.hotkey_id_count_up = obs.OBS_INVALID_HOTKEY_ID
        self.hotkey_id_reset = obs.OBS_INVALID_HOTKEY_ID
        self.counter = 0

    def hotkey_up(self):
        self.update_text(self.counter_text)

    def hotkey_reset(self):
        self.update_text(self.counter_text, -1)

    def refresh_text(self):
        self.update_text(self.counter_text, -1)


hotkeys_counter = Driver(source_name="default2", text_string="default string")
# --------------------------------------------------------------------------------
# ------------------------         obs loading                  ------------------
# --------------------------------------------------------------------------------


def refresh(prop, props):
    hotkeys_counter.refresh_text()


def script_description():
    return " Counter "


def script_update(settings):
    hotkeys_counter.source_name = obs.obs_data_get_string(settings, "source")
    hotkeys_counter.counter_text = obs.obs_data_get_string(settings, "counter_text")


def script_save(settings):
    hotkey_save_array_count_up = obs.obs_hotkey_save(hotkeys_counter.hotkey_id_count_up)
    hotkey_save_array_reset = obs.obs_hotkey_save(hotkeys_counter.hotkey_id_reset)
    obs.obs_data_set_array(settings, "count_up_hotkey", hotkey_save_array_count_up)
    obs.obs_data_set_array(settings, "reset_hotkey", hotkey_save_array_reset)
    obs.obs_data_array_release(hotkey_save_array_count_up)
    obs.obs_data_array_release(hotkey_save_array_reset)


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(
        props, "counter_text", "Set counter text", obs.OBS_TEXT_DEFAULT
    )

    p = obs.obs_properties_add_list(
        props,
        "source",
        "Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh)
    return props


def script_load(settings):
    def callback_up(pressed):
        if pressed:
            return hotkeys_counter.hotkey_up()

    def callback_reset(pressed):
        if pressed:
            return hotkeys_counter.hotkey_reset()

    hotkey_id_count_up = obs.obs_hotkey_register_frontend(
        "counter up !", "Count up ", callback_up
    )
    hotkey_id_reset = obs.obs_hotkey_register_frontend(
        "reset !", "Reset ", callback_reset
    )
    hotkey_save_array_count_up = obs.obs_data_get_array(settings, "count_up_hotkey")
    hotkey_save_array_reset = obs.obs_data_get_array(settings, "reset_hotkey")
    obs.obs_hotkey_load(hotkey_id_count_up, hotkey_save_array_count_up)
    obs.obs_hotkey_load(hotkey_id_reset, hotkey_save_array_reset)
    obs.obs_data_array_release(hotkey_save_array_count_up)
    obs.obs_data_array_release(hotkey_save_array_reset)
