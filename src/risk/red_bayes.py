#========================================[IMPORTS]========================================#
from pathlib import Path
from pgmpy.models import DiscreteBayesianNetwork #Clase para construir BN discretas
from pgmpy.factors.discrete import TabularCPD #Clase para definir tablas de probabilidades ocndicionales
from pgmpy.inference import VariableElimination #Clase para realizar inferencia por eliminación de variables (conocoer probabilidades dada una evidencia)

import json 
#========================================[CONFIG]========================================#
confidence = 0.2  # confianza en la amenaza (P(Threat=yes))

with open(Path(__file__).parent.parent / "Configs" / "bn_probs.json", "r") as data:
    cpd_data = json.load(data)


#========================================[BN_MODEL]========================================#
'''
Modelo de grafo de la red bayesiana (DEBE SER ACÍCLICO):
Cada tupla (A, B) representa una arista dirigida A -> B
'''
model = DiscreteBayesianNetwork([
    ("Threat", "Risk"),
    ("Risk", "C_res"),
    ("Risk", "I_res"),
    ("Risk", "A_res"),
    ("CM", "C_res"),
    ("CM", "I_res"),
    ("CM", "A_res"),
])


'''Definición de las CPDs (probabilidades condicionales)'''
#Threat: P(Threat=yes)={confidence}, P(Threat=no)=1- {confidence}
cpd_threat = TabularCPD(
    variable="Threat",
    variable_card=len(cpd_data["Threat"]["states"]),
    values=[[1 - confidence], [confidence]],
    state_names={"Threat": cpd_data["Threat"]["states"]}
)


# Countermeasure: uniforme entre todas las opciones (3 en este caso = 1/3)
cpd_cm = TabularCPD(
    variable="CM",
    variable_card=len(cpd_data["CM"]["states"]),
    values=[[p] for p in cpd_data["CM"]["values"]],
    state_names={"CM": cpd_data["CM"]["states"]}
)

#Riesgo condicionado a amenaza:
cpd_risk = TabularCPD(
    variable="Risk",
    variable_card=len(cpd_data["Risk"]["states"]),
    values=cpd_data["Risk"]["values"],
    evidence=["Threat"],
    evidence_card=[len(cpd_data["Threat"]["states"])],
    state_names={
        "Risk": cpd_data["Risk"]["states"],
        "Threat": cpd_data["Threat"]["states"]
    }
)


#La probabilidad de que el riesgo residual que impacta en la confidencialidad, integridad y disponibilidad sea alto, medio o bajo en función del riesgo y las contramedidas
cpd_c_res = TabularCPD(
    variable="C_res",
    variable_card=len(cpd_data["C_res"]["states"]),
    values=
        cpd_data["C_res"]["values"]
    ,
    evidence=["Risk", "CM"],
    evidence_card=[len(cpd_data["Risk"]["states"]), len(cpd_data["CM"]["states"])],
    state_names={
        "C_res": cpd_data["C_res"]["states"],
        "Risk": cpd_data["Risk"]["states"],
        "CM": cpd_data["CM"]["states"]
    }
)

cpd_i_res = TabularCPD(
    variable="I_res",
    variable_card=len(cpd_data["I_res"]["states"]),
    values=cpd_data["I_res"]["values"],
    evidence=["Risk", "CM"],
    evidence_card=[
        len(cpd_data["Risk"]["states"]),
        len(cpd_data["CM"]["states"])
    ],
    state_names={
        "I_res": cpd_data["I_res"]["states"],
        "Risk": cpd_data["Risk"]["states"],
        "CM": cpd_data["CM"]["states"]
    }
)


cpd_a_res = TabularCPD(
    variable="A_res",
    variable_card=len(cpd_data["A_res"]["states"]),
    values=cpd_data["A_res"]["values"],
    evidence=["Risk", "CM"],
    evidence_card=[
        len(cpd_data["Risk"]["states"]),
        len(cpd_data["CM"]["states"])
    ],
    state_names={
        "A_res": cpd_data["A_res"]["states"],
        "Risk": cpd_data["Risk"]["states"],
        "CM": cpd_data["CM"]["states"]
    }
)


#=================================[INFERENCE]========================================#
'''Inferencia del modelo'''

# Añadimos CPDs al grafo del modelo para que pueda funcionar correctamente
model.add_cpds(cpd_threat, cpd_cm, cpd_risk, cpd_c_res, cpd_i_res, cpd_a_res)

# Ejecutamos un sanity check para asegurarnos de que el modelo es correcto (todas las CPDs están bien definidas y consistentes)
assert model.check_model()

# Cargamos el modelo en el motor de inferencia (Variable Elimination)
infer = VariableElimination(model)

# Pregunta: ¿Cuál es C_res si aplico firewall?
q1 = infer.query(variables=["C_res"], evidence={"CM": "firewall"})
print("\nP(C_res | CM=firewall):")
print(q1)

# Pregunta: ¿Cuál es I_res si aplico firewall?
q1 = infer.query(variables=["I_res"], evidence={"CM": "firewall"})
print("\nP(I_res | CM=firewall):")
print(q1)

# Pregunta: ¿Cuál es A_res si aplico firewall?
q1 = infer.query(variables=["A_res"], evidence={"CM": "firewall"})
print("\nP(A_res | CM=firewall):")
print(q1)

# Pregunta (opcional): ¿y si además sabemos que hay amenaza?
q2 = infer.query(variables=["C_res"], evidence={"CM": "firewall", "Threat": "yes"})
print("\nP(C_res | CM=firewall, Threat=yes):")
print(q2)

# Pregunta probabilidad de riesgo alto dado que hay amenaza
q3 = infer.query(variables=["Risk"], evidence={"Threat": "yes", "CM": "firewall"})
print("\nP(Risk | Threat=yes, CM=firewall):")
print(q3)

