from aiogram.fsm.state import State, StatesGroup


class Subscribe(StatesGroup):
    sub_check = State()
    get_photo = State()
    in_proc = State()
    decline = State()
    free = State()


class Help(StatesGroup):
    help_state = State()


class PrivateRoom(StatesGroup):
    main_room = State()
    second_stage_rooms = State()
    channel_state = State()
    channel_delete = State()
    send_file = State()
    get_analytic_code = State()
    get_data_code = State()
    auth = State()
    in_req = State()
    period_enter_for_views = State()
    period_enter_for_videos = State()
    period_enter_for_subs = State()
    period_enter_for_agv_view = State()

    main_period_enter_for_views = State()
    main_period_enter_for_videos = State()
    main_period_enter_for_subs = State()
    main_period_enter_for_agv_view = State()

    back_to_channel = State()


class AdminState(StatesGroup):
    admin_room = State()
    uid_enter = State()
