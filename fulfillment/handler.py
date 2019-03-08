# -*- coding: utf-8 -*-
import json
import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# =========================================================================================================================================
# Constants
# =========================================================================================================================================


SKILL_NAME = "Endangered Species Facts"
GET_FACT_MESSAGE = "Here's your fact:"
HELP_MESSAGE = "You can say tell me a Endangered Species fact, how many species are endangered, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Endangered Species Facts skill can't help you with that.  It can help you discover facts about endangered species if you say tell me an endangered species fact. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."


# =========================================================================================================================================
# Lambda function handler
# =========================================================================================================================================


sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_random_yes_no_question():
    """Return random question for YES/NO answering."""
    questions = [
        "Would you like another fact?", "Can I tell you another fact?",
        "Do you want to hear another fact?"]
    return random.choice(questions)


def get_random_goodbye():
    """Return random goodbye message."""
    goodbyes = ["OK.  Goodbye!", "Have a great day!", "Come back again soon!"]
    return random.choice(goodbyes)


class LaunchRequestHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         return is_request_type("LaunchRequest")(handler_input)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         speech_text = f"Welcome to {SKILL_NAME}. " + HELP_MESSAGE

         handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(
            False)
         return handler_input.response_builder.response

         
class GetRandomFactHandler(AbstractRequestHandler):
    """Handler for GetRandomFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetRandomFactIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetRandomFactHandler")
        
        with open('./fulfillment/data/data.json') as f:
            data = json.loads(f.read())
        
        while True:
            fact = random.choice(data[random.choice(list(data))]['Facts'])
            if fact:
                break
            else:
                continue

        speech = "{intro} {fact} {reprompt}".format(
            intro=GET_FACT_MESSAGE, 
            fact=fact, 
            reprompt=get_random_yes_no_question())

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, fact)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class GetNumberOfEndangeredSpeciesHandler(AbstractRequestHandler):
    """Handler for GetNumberOfEndangeredSpecies Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetNumberOfEndangeredSpecies")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNumberOfEndangeredSpeciesHandler")
        
        with open('./fulfillment/data/data.json') as f:
            data = json.loads(f.read())
        
        species = [species for species in data]
        num_species = len(species)
        critical_num = sum(1 for animal in species if data[animal]['Conservation Status']=="Critically Endangered (CR)")

        speech = "There are currently {number} endangered species. {critical_num} of which are critically endangered.".format(
            number=num_species,
            critical_num=critical_num)

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, num_species)).set_should_end_session(
            False)
        return handler_input.response_builder.response


# Built-in Intent Handlers
class YesHandler(AbstractRequestHandler):
    """If the user says Yes, they want another fact."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In YesHandler")
        return GetRandomFactHandler().handle(handler_input)


class NoHandler(AbstractRequestHandler):
    """If the user says No, then the skill should be exited."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NoHandler")

        return handler_input.response_builder.speak(
            get_random_goodbye()).set_should_end_session(True).response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetRandomFactHandler())
sb.add_request_handler(GetNumberOfEndangeredSpeciesHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(YesHandler())
sb.add_request_handler(NoHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Uncomment the following lines of code for request, response logs.
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
main = sb.lambda_handler()