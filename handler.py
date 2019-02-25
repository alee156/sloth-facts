# -*- coding: utf-8 -*-

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
GET_FACT_MESSAGE = "Here's your fact: "
HELP_MESSAGE = "You can say tell me a Endangered Species fact, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Endangered Species Facts skill can't help you with that.  It can help you discover facts about endangered species if you say tell me an endangered species fact. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."


# =========================================================================================================================================
# Facts
# =========================================================================================================================================


data = [
  'The Blue Whale is the largest animal ever to have lived on earth. Their tongues alone can weigh as much as an elephant - their hearts, as much as a car.',
  'Despite being so massive, the blue whale feeds on some of the smallest marine life – tiny shrimp like animals called krill. A single adult blue whale can consume 36,000 kg of krill a day.',
  'Incredibly, Blue Whales are graceful swimmers cruise the ocean at over 8km/h, and can reach speeds of over 30km/h.',
  'Blue whales have few predators but are known to fall victim to attacks by sharks and killer whales, and many are injured or die each year from impacts with large ships.',
  'Though we can’t hear them, blue whales are one of the loudest animals on the planet, communicating with each other using a series of low frequency pulses, groans, and moans. It is thought that in good conditions blue whales can hear each other across distances of up to 1,600km.',
  'Researchers have proven that chimpanzees are self-aware and can anticipate the impact of their actions on the environment around them, an ability once thought to be uniquely human.',
  'Chimpanzees have been shown to have their own individual personalities.',
  'Chimpanzees behave in a way indicating that they feel empathy.',
  'Chimpanzees travel mostly on the ground but will mostly feed in trees during the day and make a new nest every night in the forest canopy to sleep.',
  'Chimpanzees are classified as endangered in the wild. Aside from habitat loss they are hunted for bushmeat and infants taken for sale into the pet trade.',
  'Chimpanzees have many different vocalizations from soft grunts and lip smacks to alarm barks and screams.  One of the most notable vocalizations is the pant hoot used in situations of increasing social excitement. Chimpanzees are also capable of learning basic human sign language.',
  'Chimpanzees have opposable thumbs and toes that allow for grasping, climbing, and object manipulation. Chimpanzees are very dexterous and are able to manipulate objects in their environment in order to fashion and use tools.  These tools are usually used to obtain food sources. Sticks are used for termite fishing and ant dipping, leaf sponges to soak up water and, in West Africa, chimpanzees use specially chosen rocks to crack hard palm nuts, a behaviour that can take many years to perfect. Baby female chimps were recently discovered playing with sticks like human children play with dolls.',
  'Chimpanzees have the same bones and muscles as humans with differences only in form (e.g. their arms are longer than their legs). Adapted for quadrupedal movement and movement through the trees, chimpanzees have robust bodies and powerful arms. Because of their dense bones and muscle tissue, the upper body strength of a mature chimpanzee is 8-10 times that than that of humans.',
  'Despite our increasing understanding of the significant similarity between humans and chimpanzees, humans continue to use chimpanzees in experiments, including experiments which cause them significant pain and suffering.',
  'As the largest member of the cat family, tigers are strong, powerful and one of nature’s most feared predators. Their beautiful orange and black striped coats provide camouflage when hunting prey at night when they can reach speeds of 40 miles per hour.',
  'Tigers are native to Asia, but their range today is much smaller than it used to be, and includes South-east Asia, India, western China, and some parts of Russia, with breeding populations present in Bhutan, Bangladesh, India, Malaysia, Indonesia, Thailand, Russia and Nepal.',
  'In terms of habitat, tigers inhabit a range of environments, but generally prefer areas with dense cover, like forests, with access to water and plenty of prey. Dens are positioned in secluded areas such as in caves, among dense vegetation or in hollow trees.',
  'Tigers are powerful apex predators that are at the top of the food chain and capable of killing animals over twice their size.  They are nocturnal hunters and will travel many miles to prey on a variety of animals including deer, buffalo and wild boar; native ungulates are the favourite. Not wanting to waste food, remains of large kills may be dragged to a thicket and loosely buried with leaves, ready to be returned to later.',
  'Tigers are solitary, living alone in scent-marked territories that vary in size depending on the availability of prey. If there is plenty of prey available, the area can support more tigers, so territories will be smaller and tiger numbers higher.',
  'Large predators need to be able to sneak up on their prey, and the tigers distinctive coat acts as camouflage, hiding them as they stalk prey in dense vegetation. No two tigers have the same stripes, enabling individuals to be identified by their unique pattern of stripes.',
  'Unlike other cats, tigers are good swimmers and often cool off in lakes and streams during the heat of the day.',
  'Three sub-species of tiger are already extinct and one species, the South China tiger, is thought only to survive in captivity. Tigers are endangered, and some the biggest threats to their survival include illegal poaching, loss of habitat due to agriculture and urbanisation, and reduction in prey availability. Increased interactions between tigers and humans and tiger attacks also results in tigers being killed.',
  'Like humans, orangutans have opposable thumbs. Their big toes are also opposable. Unlike humans, approximately one third of all orangutans do not have nails on their big toes.',
]


# =========================================================================================================================================
# Lambda function handler
# =========================================================================================================================================


sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        random_fact = random.choice(data)
        speech = GET_FACT_MESSAGE + random_fact

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, random_fact))
        return handler_input.response_builder.response


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
sb.add_request_handler(GetNewFactHandler())
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