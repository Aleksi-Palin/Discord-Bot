import translators


def translate(text,destlang):
  #translator = Translator()
  return translators.google(text,from_language="auto",to_language=destlang)
  