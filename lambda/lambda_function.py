# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, AudioItemMetadata,
    StopDirective, ClearQueueDirective, ClearBehavior)
from ask_sdk_model.ui import StandardCard, Image, SimpleCard
from ask_sdk_model.interfaces import display
import pafy
import streamyt
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
en_us_audio_data = {
    "card": {
        "title": 'My Radio',
        "text": 'Less bla bla bla, more la la la',
        "small_image_url": 'https://alexademo.ninja/skills/logo-108.png',
        "large_image_url": 'https://alexademo.ninja/skills/logo-512.png'
    },
    "url": 'https://audio1.maxi80.com',
    "start_jingle": 'https://s3-eu-west-1.amazonaws.com/alexa.maxi80.com/assets/jingle.m4a'
}
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can now play songs!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .set_should_end_session(False)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to audioplayer sample"
        search_term=handler_input.request_envelope.request.intent.slots['song'].value
        title,url=streamyt.getvideos(search_term)
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        card = StandardCard(
                title=title,
                text=en_us_audio_data["card"]["text"],
                image=Image(
                    small_image_url=en_us_audio_data["card"]["small_image_url"],
                    large_image_url=en_us_audio_data["card"]["large_image_url"]
                )
        )
        directive = PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        expected_previous_token=None,
                        token=url,
                        url=playurl,
                        offset_in_milliseconds=0
                    ),
                    metadata=AudioItemMetadata(
                        title=title,
                        subtitle=en_us_audio_data["card"]["text"],
                        art=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        ),
                        background_image=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        )
                    )
                )
        )
        handler_input.response_builder.set_card(
        card).add_directive(directive).set_should_end_session(True)
        speech_text=title
        return handler_input.response_builder.speak(speech_text).response
        
                
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
class ArtistIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ArtistIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to audioplayer sample"
        search_term=handler_input.request_envelope.request.intent.slots['artist'].value
        titles,urls=streamyt.getchannel(search_term)
        title=titles[0]
        url=urls[0]
        attrs=handler_input.attributes_manager.session_attributes
        attrs['urls']=urls
        attrs['titles']=titles
        attrs['idx']=0
        handler_input.attributes_manager.session_attributes.update(attrs)
        logger.info(handler_input.attributes_manager.session_attributes)
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        token=url
        card = StandardCard(
                title=title,
                text=en_us_audio_data["card"]["text"],
                image=Image(
                    small_image_url=en_us_audio_data["card"]["small_image_url"],
                    large_image_url=en_us_audio_data["card"]["large_image_url"]
                )
        )
        directive = PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        expected_previous_token=None,
                        token=token,
                        url=playurl,
                        offset_in_milliseconds=0
                    ),
                    metadata=AudioItemMetadata(
                        title=title,
                        subtitle=en_us_audio_data["card"]["text"],
                        art=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        ),
                        background_image=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        )
                    )
                )
        )
        handler_input.response_builder.set_card(
        card).add_directive(directive).set_should_end_session(False)
        speech_text=titles[0]
        return handler_input.response_builder.speak(speech_text).response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"
        handler_input.response_builder.add_directive(StopDirective())
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = exception

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
class ResumeIntentHandler(AbstractRequestHandler):
    """Handler for resume intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.ResumeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        card = StandardCard(
        title=title,
        text=en_us_audio_data["card"]["text"],
        image=Image(
                    small_image_url=en_us_audio_data["card"]["small_image_url"],
                    large_image_url=en_us_audio_data["card"]["large_image_url"]
                )
            )
        directive = PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        expected_previous_token=None,
                        token=url,
                        url=playurl,
                        offset_in_milliseconds=0
                    ),
                    metadata=AudioItemMetadata(
                        title=title,
                        subtitle=en_us_audio_data["card"]["text"],
                        art=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        ),
                        background_image=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        )
                    )
                )
        )
        handler_input.response_builder.set_card(
        card).add_directive(directive).set_should_end_session(True)
        return handler_input.response_builder.response
class NextIntentHandler(AbstractRequestHandler):
    """Handler for resume intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NextIntent")(handler_input) or ask_utils.is_intent_name("next")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info(handler_input.attributes_manager.session_attributes)
        urls=handler_input.attributes_manager.session_attributes['urls']
        idx=handler_input.attributes_manager.session_attributes['idx']
        titles=handler_input.attributes_manager.session_attributes['titles']
        idx=min(idx+1,len(urls)-1)
        title=titles[idx]
        handler_input.attributes_manager.session_attributes['idx']=idx
        url=urls[idx]
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        token=url
        card = StandardCard(
        title=title,
        text=en_us_audio_data["card"]["text"],
        image=Image(
                    small_image_url=en_us_audio_data["card"]["small_image_url"],
                    large_image_url=en_us_audio_data["card"]["large_image_url"]
                )
            )
        directive = PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        expected_previous_token=None,
                        token=token,
                        url=playurl,
                        offset_in_milliseconds=0
                    ),
                    metadata=AudioItemMetadata(
                        title=title,
                        subtitle=en_us_audio_data["card"]["text"],
                        art=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        ),
                        background_image=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        )
                    )
                )
        )
        handler_input.response_builder.set_card(
        card).add_directive(directive).set_should_end_session(False)
        return handler_input.response_builder.speak(title).response
class PreviousIntentHandler(AbstractRequestHandler):
    """Handler for resume intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.PreviousIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info(handler_input.attributes_manager.session_attributes)
        urls=handler_input.attributes_manager.session_attributes['urls']
        idx=handler_input.attributes_manager.session_attributes['idx']
        titles=handler_input.attributes_manager.session_attributes['titles']
        idx=max(idx-1,0)
        title=titles[idx]
        handler_input.attributes_manager.session_attributes['idx']=idx
        url=urls[idx]
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        token=url
        card = StandardCard(
        title=title,
        text=en_us_audio_data["card"]["text"],
        image=Image(
                    small_image_url=en_us_audio_data["card"]["small_image_url"],
                    large_image_url=en_us_audio_data["card"]["large_image_url"]
                )
            )
        directive = PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        expected_previous_token=None,
                        token=token,
                        url=playurl,
                        offset_in_milliseconds=0
                    ),
                    metadata=AudioItemMetadata(
                        title=title,
                        subtitle=en_us_audio_data["card"]["text"],
                        art=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        ),
                        background_image=display.Image(
                            content_description=en_us_audio_data["card"]["title"],
                            sources=[
                                display.ImageInstance(
                                    url="https://alexademo.ninja/skills/logo-512.png"
                                )
                            ]
                        )
                    )
                )
        )
        handler_input.response_builder.set_card(
        card).add_directive(directive).set_should_end_session(False)
        return handler_input.response_builder.speak(title).response
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(ArtistIntentHandler())
sb.add_request_handler(ResumeIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()