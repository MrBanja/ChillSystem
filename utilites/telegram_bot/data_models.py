from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel, Field


class PollTypesEnum(str, Enum):
    regular = 'regular'
    quiz = 'quiz'


class ChatTypesEnum(str, Enum):
    private = 'private'
    group = 'group'
    super_group = 'supergroup'
    channel = 'channel'


class MessageEntityTypeEnum(str, Enum):
    bold = 'bold'
    bot_command = 'bot_command'
    cashtag = 'cashtag'
    code = 'code'
    email = 'email'
    hashtag = 'hashtag'
    italic = 'italic'
    mention = 'mention'
    phone_number = 'phone_number'
    pre = 'pre'
    strikethrough = 'strikethrough'
    text_link = 'text_link'
    text_mention = 'text_mention'
    underline = 'underline'
    url = 'url'


class FileBaseModel(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None


class MaskPositionModel(BaseModel):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class ContactModel(BaseModel):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None


class InvoiceModel(BaseModel):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class LocationModel(BaseModel):
    longitude: float
    latitude: float


class LoginUrlModel(BaseModel):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None


class InlineKeyboardButtonModel(BaseModel):
    text: str
    url: Optional[str] = None
    login_url: Optional[LoginUrlModel] = None
    callback_data: Optional[str] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    callback_game: Optional[dict] = None  # TODO: Add CallBackGame (https://core.telegram.org/bots/api#callbackgame)
    pay: Optional[bool] = None


class InlineKeyboardMarkupModel(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButtonModel]]


class UserModel(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


class ChatPhotoModel(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatPermissionsModel(BaseModel):
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None


class ChatModel(BaseModel):
    id: int
    type_: ChatTypesEnum = Field(
        ...,
        alias='type',
        description='Type of chat, can be either “private”, “group”, “supergroup” or “channel”',
    )
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhotoModel] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['MessageModel'] = None
    permissions: Optional[ChatPermissionsModel] = None
    slow_mode_delay: Optional[int] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None


class DiceModel(BaseModel):
    emoji: str
    value: int


class VenueModel(BaseModel):
    location: LocationModel
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None


class PhotoSizeModel(FileBaseModel):
    width: int
    height: int


class AnimationModel(FileBaseModel):
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSizeModel] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None


class AudioModel(FileBaseModel):
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    mime_type: Optional[str] = None
    thumb: Optional[PhotoSizeModel] = None


class DocumentModel(FileBaseModel):
    thumb: Optional[PhotoSizeModel] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None


class StickerModel(FileBaseModel):
    width: int
    height: int
    is_animated: bool
    thumb: Optional[PhotoSizeModel] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    mask_position: Optional[MaskPositionModel] = None


class VideoModel(FileBaseModel):
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSizeModel] = None
    mime_type: Optional[str] = None


class VideoNoteModel(FileBaseModel):
    length: int
    duration: int
    thumb: Optional[PhotoSizeModel] = None


class VoiceModel(FileBaseModel):
    duration: int
    mime_type: Optional[str] = None


class MessageEntityModel(BaseModel):
    type_: MessageEntityTypeEnum = Field(..., alias='type')
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[UserModel] = None
    language: Optional[str] = None


class GameModel(BaseModel):
    title: str
    description: str
    photo: List[PhotoSizeModel]
    text: Optional[str] = None
    text_entities: Optional[List[MessageEntityModel]] = None
    animation: Optional[AnimationModel] = None


class PollOptionModel(BaseModel):
    text: str
    voter_count: int


class PollModel(BaseModel):
    id: str
    question: str
    options: List[PollOptionModel]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type_: PollTypesEnum = Field(..., alias='type')
    allows_multiple_answers: bool
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntityModel]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None


class MessageModel(BaseModel):
    message_id: int
    date: int
    chat: ChatModel
    animation: Optional[AnimationModel] = None
    audio: Optional[AudioModel] = None
    author_signature: Optional[str] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntityModel]] = None
    channel_chat_created: Optional[bool] = None
    connected_website: Optional[str] = None
    contact: Optional[ContactModel] = None
    delete_chat_photo: Optional[bool] = None
    dice: Optional[DiceModel] = None
    document: Optional[DocumentModel] = None
    edit_date: Optional[int] = None
    entities: Optional[List[MessageEntityModel]] = None
    forward_date: Optional[int] = None
    forward_from: Optional[UserModel] = None
    forward_from_chat: Optional[ChatModel] = None
    forward_from_message_id: Optional[int] = None
    forward_sender_name: Optional[str] = None
    forward_signature: Optional[str] = None
    from_: Optional[UserModel] = Field(None, alias='from')
    game: Optional[GameModel] = None
    group_chat_created: Optional[bool] = None
    invoice: Optional[InvoiceModel] = None
    left_chat_member: Optional[UserModel] = None
    location: Optional[LocationModel] = None
    media_group_id: Optional[str] = None
    migrate_from_chat_id: Optional[int] = None
    migrate_to_chat_id: Optional[int] = None
    new_chat_members: Optional[List[UserModel]] = None
    new_chat_photo: Optional[List[PhotoSizeModel]] = None
    new_chat_title: Optional[str] = None
    passport_data: Optional[dict] = None  # TODO: Add passport model (https://core.telegram.org/bots/api#passportdata)
    photo: Optional[List[PhotoSizeModel]] = None
    pinned_message: Optional['MessageModel'] = None
    poll: Optional[PollModel] = None
    reply_markup: Optional[InlineKeyboardMarkupModel] = None
    reply_to_message: Optional['MessageModel'] = None
    sticker: Optional[StickerModel] = None
    successful_payment: Optional[dict] = None  # TODO: Add SuccessfulPayment
    supergroup_chat_created: Optional[bool] = None
    text: Optional[str] = None
    venue: Optional[VenueModel] = None
    via_bot: Optional[UserModel] = None
    video: Optional[VideoModel] = None
    video_note: Optional[VideoNoteModel] = None
    voice: Optional[VoiceModel] = None


class InlineQueryModel(BaseModel):
    id: str
    from_: UserModel = Field(..., alias='from')
    query: str
    offset: str
    location: Optional[LocationModel] = None


class ChosenInlineResultModel(BaseModel):
    result_id: str
    from_: UserModel = Field(..., alias='from')
    query: str
    location: Optional[LocationModel] = None
    inline_message_id: Optional[str] = None


class CallbackQueryModel(BaseModel):
    id: str
    chat_instance: str
    from_: UserModel = Field(..., alias='from')
    message: Optional[MessageModel] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None


class PollAnswerModel(BaseModel):
    poll_id: str
    user: UserModel
    option_ids: List[int]


class UpdateModel(BaseModel):
    update_id: int
    message: Optional[MessageModel] = None
    edited_message: Optional[MessageModel] = None
    channel_post: Optional[MessageModel] = None
    edited_channel_post: Optional[MessageModel] = None
    poll: Optional[PollModel] = None
    inline_query: Optional[InlineQueryModel] = None
    chosen_inline_result: Optional[ChosenInlineResultModel] = None
    callback_query: Optional[CallbackQueryModel] = None
    shipping_query: Optional[dict] = None  # TODO: Add shipping query model.
    pre_checkout_query: Optional[dict] = None  # TODO: Add preCheckoutQuery model.
    poll_answer: Optional[PollAnswerModel] = None


class SendMessageModel(BaseModel):
    chat_id: Union[int, str]
    text: str
    parse_mode: Optional[str] = None
    disable_web_page_preview: Optional[bool] = None
    disable_notification: Optional[bool] = None
    reply_to_message_id: Optional[int] = None
    reply_markup: Optional[dict] = None  # TODO (https://core.telegram.org/bots/api#sendmessage)


class SetWebHookModel(BaseModel):
    url: str


MessageModel.update_forward_refs()
ChatModel.update_forward_refs()
