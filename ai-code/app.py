import os
from flask import Flask, render_template_string
from kubernetes import client, config
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from retrieve_chunks import retrieve_relevant_code

load_dotenv()
config.load_kube_config(config_file=os.getenv("KUBECONFIG_PATH"))

app = Flask(__name__)

def extract_recent_errors(namespace, keywords=["ERROR", "Exception", "Traceback"], count=2):
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace)
    error_lines = []
    for pod in pods.items:
        try:
            raw_log = v1.read_namespaced_pod_log(pod.metadata.name, namespace)
            filtered = [line for line in raw_log.splitlines() if any(k in line for k in keywords)]
            error_lines.extend(filtered)
        except Exception as e:
            error_lines.append(f"[ERROR] Failed to read logs from {pod.metadata.name}: {str(e)}")
    return error_lines[-count:] if error_lines else ["No recent errors found."]

def generate_rca(error_lines, repo_code):
    llm = AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_GPT_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_GPT_API_VERSION")
    )
    prompt = (
        "You are an SRE assistant. Based on the following error messages from Kubernetes pod logs "
        "and the application source code, identify the root cause and explain whether the issue is code-related:\n\n"
        f"Errors:\n{chr(10).join(error_lines)}\n\n"
        f"Code:\n{repo_code}"
    )
    return llm.invoke([HumanMessage(content=prompt)]).content

@app.route('/fd_eks/')
def dashboard():
    try:
        namespace = "petclinic"
        app_name = "Petclinic"
        error_lines = extract_recent_errors(namespace)
        repo_code, sources = retrieve_relevant_code(error_lines)
        rca = generate_rca(error_lines, repo_code)

        return render_template_string("""
        <h2>Application Name: {{ app_name }}</h2>

        <h3>Error</h3>
        <ul>{% for line in errors %}<li>{{ line }}</li>{% endfor %}</ul>

        <h3>Source Files</h3>
        <ul>{% for src in sources %}<li>{{ src }}</li>{% endfor %}</ul>

        <h3>RCA</h3>
        <pre>{{ rca }}</pre>
        """, app_name=app_name, errors=error_lines, sources=sources, rca=rca)

    except Exception as e:
        return render_template_string("""
        <h2>Application Name: Petclinic</h2>
        <h3>Error</h3>
        <p>❌ Internal Error</p>
        <pre>{{ error }}</pre>
        """, error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False, use_reloader=False)
