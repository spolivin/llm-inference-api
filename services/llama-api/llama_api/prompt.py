def compose_llama_prompt(question: str) -> str:
    prompt = (
        "[INST] <<SYS>>\n"
        "You are a helpful, knowledgeable assistant.\n"
        "<</SYS>>\n\n"
        f"{question}\n"
        "[/INST]"
    )

    return prompt
