import asyncio


def format_response(given_command_type: str, command_dict: dict, execution_result: str) -> dict:
    """Format the response to be sent back to the client."""
    math_expression = command_dict.get("expression", None)
    output = {
        given_command_type: command_dict.get('command_name', math_expression) + " " + " ".join(
            command_dict.get("parameters", [])),
        "result": execution_result
    }
    return output


async def systemic_processing(command_name: str, parameters: list) -> str:
    """Perform some systemic processing on the command."""
    proc = await asyncio.create_subprocess_exec(command_name, *parameters, stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    await proc.wait()
    result = await proc.stdout.read()

    # If the result is empty, then there was an error
    if result == b'':
        result = await proc.stderr.read()

    return result.decode()


async def computational_command_processing(expression: str) -> str:
    result = eval(expression)
    return str(result)
