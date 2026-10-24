
EN_dict = {
    "Homebuyer classes" : "Class info: free, English & Spanish, in-person & virtual, registration link [VERIFY link]", 
    "Buying a home (counseling)" : "What counseling is, how to start, scheduling link, [VERIFY link]",
    "Down payment assistance" : "DPA programs vary; most require a homebuyer class. Start with class + counseling. No eligibility decisions",
    "Other help (rent, utilities, repairs)" : "Unfortunatley, Avenue HOC does not provide these services. Please dial 211 or visit 211texas.gov for more help on your request.",
    "Behind on my mortgage" : "Do you currently have a scheduled foreclosure sale date?",
    "Yes, I currently have a scheduled foreclosure sale date" : "This is an URGENT situation. Please call us now at 713-864-9099 between the hours of 9 AM and 4 PM and press 3. Then, complete the form linked here: [VERIFY link]. We will contact you as soon as possible to discuss your options.",
    "No, I currently do not have a scheduled foreclosure sale date" : "Give info about forclosure prevention and provide the contact form.",
    "I already own my home" : "Provide the post-purchase information and direct to contact form.",
    "Talk to a person" : "Provide hours and HOC phone number, 713-864-9099, and direct to contact form."
}

EN_options_dict = {
    "How can we help you today?" : ("Homebuyer classes", "Buying a home (counseling)", "Down payment assistance", "Other help (rent, utilities, repairs)", "Behind on my mortgage", "I already own my home", "Talk to a person"),
    "Do you currently have a scheduled foreclosure sale date?" : ("Yes, I currently have a scheduled foreclosure sale date", "No, I currently do not have a scheduled foreclosure sale date")
}

ES_dict = {
    "Clases para compradores de vivienda": "Información sobre las clases: gratuitas, en inglés y español, presenciales y virtuales, enlace de inscripción [VERIFY link]",
    "Comprar una vivienda (asesoría)": "Qué es la asesoría, cómo comenzar, enlace para programar una cita, [VERIFY link]",
    "Asistencia para el pago inicial": "Los programas de asistencia para el pago inicial varían; la mayoría requiere completar una clase para compradores de vivienda. Comience con una clase y asesoría. No se toman decisiones sobre elegibilidad.",
    "Otro tipo de ayuda (alquiler, servicios públicos, reparaciones)": "Lamentablemente, Avenue HOC no ofrece estos servicios. Por favor, llame al 211 o visite 211texas.gov para obtener más ayuda con su solicitud.",
    "Estoy atrasado en los pagos de mi hipoteca": "¿Tiene actualmente una fecha programada para la subasta de su vivienda por ejecución hipotecaria?",
    "Sí, actualmente tengo una fecha programada para la subasta de mi vivienda por ejecución hipotecaria": "Esta es una situación URGENTE. Por favor, llámenos ahora al 713-864-9099 entre las 9:00 a. m. y las 4:00 p. m. y presione 3. Después, complete el formulario disponible aquí: [VERIFY link]. Nos comunicaremos con usted lo antes posible para hablar sobre sus opciones.",
    "No, actualmente no tengo una fecha programada para la subasta de mi vivienda por ejecución hipotecaria": "Proporcione información sobre la prevención de ejecuciones hipotecarias y el formulario de contacto.",
    "Ya soy propietario de una vivienda": "Proporcione información sobre los servicios posteriores a la compra de una vivienda y dirija al formulario de contacto.",
    "Hablar con una persona": "Proporcione el horario de atención y el número de teléfono de HOC, 713-864-9099, y dirija al formulario de contacto."
}

ES_options_dict = {
    "¿Cómo podemos ayudarle hoy?": (
        "Clases para compradores de vivienda",
        "Comprar una vivienda (asesoría)",
        "Asistencia para el pago inicial",
        "Otro tipo de ayuda (alquiler, servicios públicos, reparaciones)",
        "Estoy atrasado en los pagos de mi hipoteca",
        "Ya soy propietario de una vivienda",
        "Hablar con una persona"
    ),
    "¿Tiene actualmente una fecha programada para la subasta de su vivienda por ejecución hipotecaria?": (
        "Sí, actualmente tengo una fecha programada para la subasta de mi vivienda por ejecución hipotecaria",
        "No, actualmente no tengo una fecha programada para la subasta de mi vivienda por ejecución hipotecaria"
    )
}

language = "EN"

def get_response(question, language="EN"):
    """
    Gets a respone from the chatbot based on the question and language provided.

    @param question: The question to ask the chatbot. Should be one of the supported questions only.
    @param language: The language to use for the response. Default is English ("EN"). Supports "ES" for Spanish.
    
    @return: The response from the chatbot.
    @throws: ValueError: If the question is not in the supported questions list or if the language is not supported.

    @author: Max Spier, October 24, 2026
    """

    if language == "EN":
        if question in EN_dict:
            return EN_dict[question]
        else:
            raise ValueError(f"Question '{question}' is not in the supported questions list for English.")
    elif language == "ES":
        if question in ES_dict:
            return ES_dict[question]
        else:
            raise ValueError(f"Question '{question}' is not in the supported questions list for Spanish.")
    else:
        raise ValueError(f"Language '{language}' is not supported. Please use 'EN' for English or 'ES' for Spanish.")

def get_next_options(question, language="EN"):
    """
    Gets the next options for the chatbot based on the question and language provided.

    @param question: The question to ask the chatbot. Should be one of the supported questions only.
    @param language: The language to use for the response. Default is English ("EN"). Supports "ES" for Spanish.
    
    @return: A tuple of the next options for the chatbot.
    @throws: ValueError: If the question is not in the supported questions list or if the language is not supported.
    @author: Max Spier, October 24, 2026
    """

    if language == "EN":
        if question in EN_options_dict:
            return EN_options_dict[question]
        else:
            raise ValueError(f"Question '{question}' is not in the supported questions list for English.")
    elif language == "ES":
        if question in ES_options_dict:
            return ES_options_dict[question]
        else:
            raise ValueError(f"Question '{question}' is not in the supported questions list for Spanish.")
    else:
        raise ValueError(f"Language '{language}' is not supported. Please use 'EN' for English or 'ES' for Spanish.")

def set_language(lang):
    """
    Sets the language for the chatbot responses.

    @param lang: The language to set. Should be "EN" for English or "ES" for Spanish.
    
    @return: None
    @throws: ValueError: If the language is not supported.

    @author: Max Spier, October 24, 2026
    """
    if lang in ["EN", "ES"]:
        language = lang
    else:
        raise ValueError(f"Language '{lang}' is not supported. Please use 'EN' for English or 'ES' for Spanish.")

