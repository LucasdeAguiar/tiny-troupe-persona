from tinytroupe.agent import TinyPerson
from tinytroupe.factory import TinyPersonFactory


def create_demo_personas():
    # Persona manual 
    persona1 = TinyPerson("Alice")
    persona1.define("age", 28)
    persona1.define("occupation", "Software Engineer")
    persona1.define("personality", "curious and analytical")

    # Persona via factory 
    persona2 = None
    try:
        factory = TinyPersonFactory(context="POC")
        persona2 = factory.generate_person(
            agent_particularities="A tech enthusiast who loves watches"
        )
    except Exception:
        persona2 = TinyPerson("FactoryFallback")
        persona2.define("occupation", "Tech Enthusiast")

    return {
        "personas": [
            {
                "name": persona1.name,
                "age": persona1.get("age"),
                "occupation": persona1.get("occupation") if not isinstance(persona1.get("occupation"), dict) else persona1.get("occupation").get("title")
            },
            {
                "name": persona2.name,
                "age": persona2.get("age"),
                "occupation": persona2.get("occupation") if not isinstance(persona2.get("occupation"), dict) else persona2.get("occupation").get("title")
            }
        ]
    }
