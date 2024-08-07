from groq import Groq
import os
import hal9 as h9

MODEL = "llama3-70b-8192"

prompt = input("")
h9.event('prompt', prompt)

system_prompt = open('system.txt', 'r').read()

messages = h9.load("messages", [{"role": "system", "content": system_prompt}])
messages.append({"role": "user", "content": prompt})

def calculate(expression):
    """Evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})

tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]

response = Groq().chat.completions.create(
  model = MODEL,
  messages = messages,
  temperature = 0,
  seed = 1,
  tools=tools,
  tool_choice="auto",
  stream = True)

response_message = response.choices[0].message
  tool_calls = response_message.tool_calls
  if tool_calls:
      available_functions = {
          "calculate": calculate,
      }
      messages.append(response_message)
      for tool_call in tool_calls:
          function_name = tool_call.function.name
          function_to_call = available_functions[function_name]
          function_args = json.loads(tool_call.function.arguments)
          function_response = function_to_call(
              expression=function_args.get("expression")
          )
          messages.append(
              {
                  "tool_call_id": tool_call.id,
                  "role": "tool",
                  "name": function_name,
                  "content": function_response,
              }
          )
      response = client.chat.completions.create(
          model=MODEL,
          messages=messages
      )
      return second_response.choices[0].message.content
  
messages.append({"role": "assistant", "content": response})
h9.save("messages", messages, hidden=True)
