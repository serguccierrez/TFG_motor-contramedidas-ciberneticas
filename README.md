# 🛡️ Motor de Recomendación de Contramedidas Cibernéticas

## Trabajo Fin de Grado (TFG)

Este repositorio contiene el **código fuente** desarrollado en el marco del **Trabajo Fin de Grado (TFG)** del Grado en Ingeniería de Tecnologías y Servicios de Telecomunicación (GITST), ETSIT.

El proyecto consiste en el diseño e implementación de un **motor de recomendación de contramedidas de ciberseguridad** frente a ataques cibernéticos, orientado a **escenarios multidominio** y basado en **modelos formales de riesgo, dependencias entre activos y conocimiento doctrinal**.

---

## 📌 Descripción del Proyecto

El objetivo del TFG es desarrollar un motor capaz de:

* **Analizar una amenaza cibernética** (por ejemplo, técnicas y tácticas MITRE ATT&CK).
* **Evaluar su impacto potencial** sobre un conjunto de activos interdependientes.
* **Estimar el riesgo residual** sobre los atributos de seguridad (Confidencialidad, Integridad y Disponibilidad – CIA).
* **Recomendar contramedidas cibernéticas** que mitiguen dicho riesgo, minimizando la interrupción operativa.

El sistema no se centra en la detección de la amenaza, sino en la **correlación, análisis y recomendación automática de contramedidas** una vez la amenaza ha sido identificada.

---

## 🧠 Enfoque Conceptual

El motor combina varios elementos clave:

* **Catálogo de activos y dependencias**, modelado como un grafo dirigido.
* **Modelo de amenazas**, basado en técnicas y tácticas de MITRE ATT&CK.
* **Modelo probabilístico (Red Bayesiana)** para la estimación de riesgo e impacto.
* **Evaluación de contramedidas**, diferenciando entre medidas preventivas y reactivas.
* **Soporte a escenarios multidominio**, considerando dependencias cruzadas entre activos.

El resultado es un sistema que permite **razonar sobre el riesgo** y **priorizar contramedidas** de forma coherente y justificable.

---

## 🛠️ Contenido del Repositorio

Este repositorio aloja exclusivamente el **código del motor**, incluyendo:

* Creación y carga del catálogo de activos.
* Definición y construcción del grafo de dependencias.
* Integración del modelo MITRE ATT&CK.
* Implementación de la red bayesiana de riesgo.
* Ejecución del pipeline de análisis y recomendación.

La documentación teórica, la memoria del TFG y los resultados experimentales se mantienen fuera de este repositorio o en carpetas separadas.

---

## ⚙️ Tecnologías Utilizadas

* **Python 3**
* **NetworkX** (modelado de grafos)
* **pgmpy** (redes bayesianas)
* **SQLite** (catálogo de activos)
* **JSON** (modelos y configuraciones)

---

## ▶️ Ejecución

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el motor (según configuración actual):

```bash
python main.py
```

---

## 📚 Contexto Académico

Este proyecto se desarrolla con fines **estrictamente académicos** como parte de un **Trabajo Fin de Grado**.
El repositorio permite:

* Control de versiones del código.
* Trazabilidad del desarrollo.
* Posibilidad de auditoría técnica por parte del tribunal evaluador.

---

## 👤 Autor

**Sergi**
Grado en Ingeniería de Tecnologías y Servicios de Telecomunicación
ETSIT – Universidad Politécnica de Madrid

