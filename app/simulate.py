from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

def run_simulation(topic: str, steps: int):
    steps = max(1, int(steps or 1))
    topic = topic or "Say hello"

    import uuid
    name1 = f"Bob-{uuid.uuid4().hex[:4]}"
    name2 = f"Carol-{uuid.uuid4().hex[:4]}"

    # Criar personas simples
    persona1 = TinyPerson(name1)
    persona1.define("occupation", "Product Manager")

    persona2 = TinyPerson(name2)
    persona2.define("occupation", "Designer")

    # Criar mundo e adicionar personas
    world = TinyWorld("Room", [persona1, persona2])

    # Primeira persona escuta o tópico
    try:
        persona1.listen(topic)
    except Exception:
        persona1.episodic_memory.add_event(f"USER: {topic}")

    try:
        world.run(steps)
    except Exception:
        pass

    transcript = []
    try:
        for agent in world.agents:
            recent = agent.episodic_memory.retrieve_recent(6)
            for m in recent:
                try:
                    if isinstance(m, str):
                        transcript.append(f"{agent.name}: {m}")
                    elif isinstance(m, dict):
                        content = (
                            m.get("content")
                            or m.get("text")
                            or m.get("message")
                            or m.get("event")
                        )
                        if isinstance(content, str):
                            transcript.append(f"{agent.name}: {content}")
                        elif isinstance(content, dict):
                            inner = content.get("text") or content.get("content")
                            if isinstance(inner, str):
                                transcript.append(f"{agent.name}: {inner}")
                    else:
                        s = str(m)
                        if s:
                            transcript.append(f"{agent.name}: {s}")
                except Exception:
                    continue
    except Exception:
        pass

    if not transcript:
        transcript = [
            f"{persona1.name}: {topic}",
            f"{persona2.name}: (ack)",
            "System: Simulation finished"
        ]

    return {"transcript": transcript[: max(3, min(6, len(transcript)))], "notes": "POC-only"}
