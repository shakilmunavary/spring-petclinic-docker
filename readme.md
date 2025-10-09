

## Containerising Pet Clinic app using Docker

This is a [dockerized version of the original app](https://github.com/spring-projects/spring-petclinic) published by Spring Boot community. 


## Running PetClinic app locally

Petclinic is a [Spring Boot](https://spring.io/guides/gs/spring-boot) application built using Maven. It is an application designed to show how the Spring stack can be used to build simple, but powerful database-oriented applications. The official version of PetClinic demonstrates the use of Spring Boot with Spring MVC and Spring Data JPA.

## How it works?

Spring boot works with MVC (Model-View-Controller) is a pattern in software design commonly used to implement user interfaces, data and control logic. It emphasizes a separation between business logic and its visualization. This "separation of concerns" provides a better division of labor and improved maintenance.We can work with the persistence or data access layer with [spring-data](https://spring.io/projects/spring-data) in a simple and very fast way, without the need to create so many classes manually. Spring data comes with built-in methods below or by default that allow you to save, delete, update and/or create.


## Getting Started


```
git clone https://github.com/dockersamples/spring-petclinic.git
cd spring-petclinic
./mvnw package
java -jar target/*.jar
```

You can then access petclinic here: http://localhost:8080/

<img width="625" alt="image" src="https://user-images.githubusercontent.com/313480/179161406-54a28200-d52e-411f-bfbe-463cf64b64b3.png">

The applications allows you to perform the following set of functions:

- Add Pets
- Add Owners
- Finding Owners
- Finding Veterinarians
- Exceptional handling


Or you can run it from Maven directly using the Spring Boot Maven plugin. If you do this it will pick up changes that you make in the project immediately (changes to Java source files require a compile as well - most people use an IDE for this):

```
./mvnw spring-boot:run
```

> NOTE: Windows users should set `git config core.autocrlf true` to avoid format assertions failing the build (use `--global` to set that flag globally).

> NOTE: If you prefer to use Gradle, you can build the app using `./gradlew build` and look for the jar file in `build/libs`.

## Building a Container

```
 docker build -t petclinic-app . -f Dockerfile
```

## Multi-Stage Build

```
 docker build -t petclinic-app . -f Dockerfile.multi
```

## Using Docker Compose

```
 docker-compose up -d
```



## References

- [Building PetClinic app using Dockerfile](https://docs.docker.com/language/java/build-images/)



Absolutely, Shakil — here’s a polished `README.md` tailored for your GitHub repo. It includes:

- ✅ Project overview
- ✅ Architecture diagram (described in Markdown)
- ✅ Setup instructions
- ✅ Usage flow
- ✅ Tech stack
- ✅ Contribution and license sections

---

### ✅ `README.md`

```markdown
# 🧠 AI-Powered RCA Dashboard for Kubernetes Applications

This project provides a full-stack, agentic RCA (Root Cause Analysis) dashboard that combines Kubernetes pod log monitoring, vector-based code retrieval, and Azure OpenAI-powered RCA synthesis. Designed for BFSI-grade observability, it enables real-time diagnostics with traceable source context.

---

## 📐 Architecture Overview

```plaintext
┌────────────────────────────┐
│        User Browser        │
│  (Accesses RCA Dashboard)  │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│         Flask App          │
│  - Extracts pod logs       │
│  - Retrieves code chunks   │
│  - Synthesizes RCA         │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│     retrieve_chunks.py     │
│  - Loads FAISS vector DB   │
│  - Matches error context   │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│         FAISS DB           │
│  - Indexed repo chunks     │
│  - Azure embeddings        │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│        Azure OpenAI        │
│  - GPT for RCA synthesis   │
│  - Embedding API for FAISS │
└────────────────────────────┘
```

---

## 🚀 Features

- ✅ Real-time RCA from Kubernetes pod logs
- ✅ Code-aware diagnostics using FAISS vector search
- ✅ Azure OpenAI-powered RCA agent
- ✅ Source file traceability for every RCA
- ✅ Modular shell scripts for reproducible setup

---

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/your-org/ai-code.git
cd ai-code

# Configure environment
cp .env.template .env
# Fill in your Azure and Kubernetes credentials

# Run the full pipeline
./run.sh

# Stop the dashboard
./stop.sh
```

---

## 🧪 Usage

- Visit `http://localhost:5004/fd_eks/`
- View recent error logs from your Kubernetes namespace
- See RCA explanation with matching code chunks and source files
- RCA is generated using Azure GPT and indexed repo context

---

## 🧰 Tech Stack

- **Flask** — RCA dashboard backend
- **LangChain + FAISS** — Vector search over codebase
- **Azure OpenAI** — GPT + Embedding APIs
- **Kubernetes Python Client** — Pod log extraction
- **Shell Scripts** — Reproducible setup (`run.sh`, `stop.sh`)
- **Spring Petclinic** — Sample repo for indexing

---

## 📁 Folder Structure

```
ai-code/
├── app.py
├── index.py
├── retrieve_chunks.py
├── run.sh
├── stop.sh
├── requirements.txt
├── flask.log
├── flask.pid
├── vector_db/
├── spring-petclinic-docker/
├── venv2/
└── .env.template
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

