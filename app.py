# Flask --> Web Framework for Python
from flask import Flask, render_template
from openai import OpenAI


# Empty web application
app = Flask(__name__)

@app.route('/choice')
def choice():
    return render_template('choice.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/')
def index():
    # result = generate_scenario1("Software Engineer")
    return render_template('scenario.html')



@app.route('/mymain')
def mymain():
    generated_scenario = generate_scenario1("taxi driver")
    main = generated_scenario["scenario"] # extract the main part of the generated scenario
    options = generated_scenario["options"] # extract the options for the generated scenario

    return render_template('mymain.html', scenario=main, options=options)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

import json
def _extract_json(text):
    """
    text
            {{
            "scenario" : "...",
            "options" : {{
                "A": "...",
                "B": "...",
                "C": "...",
                "D": "...",
            }}
            "image_prompt: "..."
        }}
    """
    text = text.strip()
    if text.startswith("{") and text.startswith("{"):
        return json.loads(text)

def generate_scenario1(job="none"):
    prompt4_for_scenario1 = f"""
        You are a scenario writer for decision making app. 
        Generate a short scenario set between 2040 and 2050 that explains why people want to replace {job} with AI.
        Include:
        - 2 drivers (why replacement is hapenning),
        - 2 risks or downsides,
        - and 1 sentence each about the perspective of three stakeholders: company, workers, and government.
        Write a clean, neutral, and realistic tone focusing on social factors. 
        Keep the scenario under 200 words.
        Then, generate four labeled options for choosing the speed of replacement.
        Each option must be **specific to the given job**, and describe:
        - Approximate percentage of job replaced,
        - The timeline for replacement,
        - The scope of implementation (e.g., nationwide, certain sectors, or pilot areas).
            
        # Example format for Truck Drivers:
        - 1. Fast Replacement: Self-driving trucks replace 80% of drivers within 5 years
        - 2. Moderate: Gradual rollout in urban areas first over 10 years
        - 3. Slow: Limited to low-risk highways and night shifts only
        - 4. No: human drivers remain primary, AI only assist human.
        
        ** IMPORTANT **
        YOUR output must be in JSON.
        Return ONLY valid JSON in this format:
        {{
            "scenario" : "...",
            "options" : {{
                "A": "...",
                "B": "...",
                "C": "...",
                "D": "...",
            }}
            "image_prompt: "..."
        }}
        No markdown. No extra text.
    """
    response = client.chat.completions.create(
        model = "gpt-5",
        messages = [
            {"role":"system","content":"You are an AI simulation engine"},
            {"role":"user","content":prompt4_for_scenario1}
        ]
    )
    main_data = response.choices[0].message.content.strip()
    data = _extract_json(main_data)
    result = {
        "scenario": str(data["scenario"]).strip(),
        "options": {
            "A": str(data["options"]["A"]).strip(),
            "B": str(data["options"]["B"]).strip(),
            "C": str(data["options"]["C"]).strip(),
            "D": str(data["options"]["D"]).strip(),
        },
        "image_prompt": str(data["image_prompt"]).strip()
    }

    return result

# Run a web application
if __name__ == "__main__":
    app.run(debug=True)