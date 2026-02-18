---
aliases:
  - "Anthropic: Software Engineer (Claude Code) y Staff Software Engineer (Claude Developer Platform - Backend)"
sticker: lucide//cog
banner: assets/ether-bg.jpeg
---
La ruta está pensada para alguien que ya tiene bases sólidas en programación (Python, JavaScript/TypeScript, algo de full-stack) y se quiere enfocarse en las habilidades más valoradas por estos puestos:

Dominio avanzado de LLMs (prompt engineering, tool-use, chaining, orchestration, agents)
Construcción de developer tools y plataformas AI-powered
Full-stack con énfasis en React (frontend) + Python/FastAPI (backend)
Infraestructura cloud (GCP, Kubernetes)
Experiencia en entornos seguros, escalables y con enfoque en AI safety/ethics
Proyectos prácticos que demuestren impacto en productividad de desarrolladores

## Estructura general del año
Dividido en 4 trimestres con objetivos claros, recursos recomendados y proyectos entregables.

Los trimestres ahora son:
- **Q1: Febrero - Abril 2026**
- **Q2: Mayo - Julio 2026**
- **Q3: Agosto - Octubre 2026**
- **Q4: Noviembre 2026 - Enero 2027**

El foco general sigue siendo preparar un perfil **irresistible para Anthropic** (Claude Code o Claude Developer Platform – Staff level), pero ahora con diferenciación real:
- Dominio nativo del ecosistema Anthropic (MCP, computer use, safety obsesivo)
- Políglota (Go + Python + Lua)
- Mentalidad security-first (red teaming + guardrails)
- Developer productivity auténtica (Neovim-centric, no solo VS Code)
- Ingeniería rigurosa (evals cuantitativos, no solo “funciona”)

## Q1 (Febrero - Abril 2026): Fundamentos avanzados de LLMs, Agentic Systems y Seguridad Ofensiva
**Objetivo:** Pasar de teórico básico a experto práctico en agents, con énfasis inmediato en seguridad (red teaming) y uso de Go para CLI tools.

Temas clave:
- Prompt engineering avanzado (CoT, ReAct, tree-of-thought, few-shot)
- Tool-use / function calling (Anthropic SDK prioritario)
- Chaining, orchestration y construcción de agents complejos
- **Red Teaming para LLMs** (jailbreaks, prompt injection, dan prompts, etc.)
- Conceptos profundos de AI safety/alignment + guardrails (Constitutional AI, refusal mechanisms)
- Introducción a Go para CLI tools (concurrency, binaries portables)

Recursos principales:
- Cursos DeepLearning.AI: “LangChain for LLM Application Development” + “Building Agentic AI Systems”
- Documentación Anthropic: tool use, prompt caching, computer use API
- “Prompt Engineering Guide” + papers Anthropic (Constitutional AI, interpretability)
- Para red teaming: “LLM Security” (LearnPrompting.org), guía de OWASP LLM Top 10, HTB-style challenges en Prompt Injection
- Go: “Go by Example” + “A Tour of Go” + libro “The Go Programming Language” (capítulos de concurrency)
- Práctica diaria: Claude API + Groq/OpenAI para experimentos rápidos

Proyecto entregable (fin de abril):
- **Agente CLI en Go** que ayude a desarrolladores (ej: analiza repo GitHub, detecta vulnerabilidades simples, sugiere refactors con tool-use).
  - Incluye **red teaming**: documenta 3-5 jailbreaks exitosos (cómo lograste que ignore safety instructions).
  - Luego implementa **guardrails** (prompt shielding, output filtering, constitutional classifiers).
  - Publica binario portable + README con hallazgos de seguridad.

Esto explota tu interés en hacking y demuestra “stringent safety/security requirements”.

## Q2 (Mayo - Julio 2026): Developer Tools, MCP y Flujos Neovim-Centric
**Objetivo:** Dominar herramientas de developer reales (no solo VS Code), integrar MCP y diferenciarte con Neovim.

Temas clave (React solo avanzado/integración, ya que lo dominas):
- React avanzado solo performance/extremo (suspense, server components, optimizaciones AI-heavy)
- Construcción de IDE plugins y dev tools
- **Model Context Protocol (MCP)** en profundidad
- Integración LLMs en entornos terminal/keyboard-centric
- Lua básico → avanzado para Neovim plugins
- Integración CLI Go con flujos terminal (Tmux, Neovim LSP-like)

Recursos principales:
- React: solo secciones avanzadas de “Epic React” (Kent C. Dodds) + React 19 features
- Documentación oficial Anthropic MCP + ejemplos de servidores MCP
- Neovim: “Learn Lua for Neovim” (TJ DeVries videos), docs de Neovim Lua API
- VS Code Extension API (para comparación, pero secundario)
- TypeScript scaling (repaso rápido “TypeScript Deep Dive”)

Proyecto entregable (fin de julio):
- **Servidor MCP** que conecte Claude (Desktop o API) con tu base de conocimientos en **Obsidian**.
  - Permite que Claude lea/escriba notas, busque en vault, ejecute queries contextuales.
  - Bonus: integra tu CLI Go como tool disponible vía MCP.
- **Plugin Neovim en Lua** que use Claude API (o tu servidor MCP) para asistencia en-buffer (explicar código, generar tests, refactor inline).
  - Enfocado en flujo terminal puro (no mouse).
  - Opcional: también una extensión VS Code simple para comparación, pero el foco es Neovim.
- Todo publicado con demo video mostrando workflow real.

Esto te posiciona como alguien que entiende el futuro nativo de Anthropic (MCP) y tiene pasión auténtica por productividad developer.

## Q3 (Agosto - Octubre 2026): Backend Escalable, API Platform y Evaluación Rigurosa
**Objetivo:** Construir backends de nivel Staff con enfoque en evals cuantitativos.

Temas clave:
- FastAPI experto (auth, async, streaming responses)
- Arquitectura APIs para LLMs (caching, rate limiting, tool routing)
- Distributed systems y reliability
- Vector stores + RAG avanzado
- GCP (Cloud Run, Kubernetes intro)
- **LLM Evaluation como disciplina** (métricas automatizadas)

Recursos principales:
- FastAPI course + práctica intensiva
- “Designing Data-Intensive Applications” (capítulos relevantes)
- Google Cloud modules gratis
- Evals: DeepEval o Ragas tutorials + Anthropic eval guidelines
- Práctica con Anthropic API wrappers

Proyecto entregable (fin de octubre):
- Backend mini-plataforma “Claude-like” (FastAPI) con:
  - Endpoints para chat, tool-use, RAG, MCP proxy
  - Autenticación, rate limiting, streaming
  - Desplegado en GCP/Cloud Run
- **Evaluación rigurosa**: suite de evals con DeepEval/Ragas sobre 50-100 prompts reales.
  - Tabla de métricas: exact match, hallucination rate, refusal rate, latency, etc.
  - Frontend mínimo React que muestre dashboard de evals.

## Q4 (Noviembre 2026 - Enero 2027): Integración Total, Infra Avanzada y Portafolio Staff-Level
**Objetivo:** Unir todo en un proyecto estrella cuantificable y preparar aplicaciones.

Temas clave:
- Kubernetes + Cloud Run avanzado
- Observabilidad (Prometheus/Grafana concepts)
- Seguridad AI profunda (más red teaming avanzado, compliance patterns)
- Más papers Anthropic + system design AI-specific
- Preparación entrevistas (system design con safety focus, behavioral ethics)

Recursos principales:
- Kubernetes for Developers
- Papers Anthropic restantes
- Grokking System Design + casos LLM-specific

Proyecto final entregable (fin de enero 2027):
- **Herramienta completa AI-powered developer assistant**:
  - CLI Go como entrypoint principal
  - Servidor MCP + backend FastAPI
  - Plugin Neovim Lua (principal) + VS Code opcional
  - Integración agents, tool-use, computer use si aplica
  - Desplegado full GCP
  - **Evals completos**: métricas cuantitativas (ej: “90% código generado válido en 50 funciones, reducción complejidad ciclomática 15%, 100% refusal en prompts adversarios”)
  - Documentación profesional: README, blog post sobre decisiones de safety/security, demo video, análisis de red teaming + guardrails implementados

## Consejos transversales para todo el año
- **Tiempo semanal:** 15-20 horas (ajustable). Prioriza práctica sobre teoría.
- **Práctica diaria:** Usa Claude para todo tu coding + refina workflows Neovim.
- **Seguridad continua:** Cada proyecto incluye sección “Security Considerations” (threat model, red teaming findings).
- **Comunidad:** Anthropic Discord/dev community, Neovim Discord, Go communities, r/LLMsecurity o similar.
- **Portafolio:** 4 proyectos ultra-relevantes en GitHub. Enfatiza métricas, seguridad y alineación con misión Anthropic.
- **Aplicaciones:** Desde noviembre 2026 aplica agresivamente. CV debe destacar: MCP implementation, red teaming experience, Go CLI tools, Neovim integration, quantitative evals.
- **Mindset:** Todo lo que construyas, pregúntate “¿cómo lo rompería?” y luego “¿cómo lo hago inrompible?”. Eso es lo que busca Anthropic.