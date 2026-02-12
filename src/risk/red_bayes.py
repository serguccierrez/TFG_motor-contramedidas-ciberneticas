#========================================[IMPORTS]========================================#
from pathlib import Path
from pgmpy.models import DiscreteBayesianNetwork #Clase para construir BN discretas
from pgmpy.factors.discrete import TabularCPD #Clase para definir tablas de probabilidades ocndicionales
from pgmpy.inference import VariableElimination #Clase para realizar inferencia por eliminación de variables (conocoer probabilidades dada una evidencia)

import json 
#========================================[CONFIG]========================================#
confidence = 0.2  # confianza en la amenaza (P(Threat=yes))

bn_cpds_path = Path(__file__).parent.parent.parent / "configs" / "bn_CPDs.json"
with open(bn_cpds_path, "r") as data:
    cpd_data = json.load(data)


#========================================[BN_MODEL]========================================#
def bayesian_network_construction():
    '''
    Función para construir el modelo de red bayesiana a partir de las CPDs definidas en el archivo JSON.
    '''
    
    
   
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
    assert model.check_model(), "Error: El modelo de red bayesiana no es correcto. Revisa las CPDs y la estructura del grafo."

    # Cargamos el modelo en el motor de inferencia (Variable Elimination)
    infer = VariableElimination(model)
    
    return infer


''''
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
'''

def get_cia_res_levels(cia_res_query):
    '''
    Función para obtener los niveles de impacto de CIA_RES (Alto, Medio, Bajo) a partir de las probabilidades inferidas.
    '''
    probs_cia_res = cia_res_query.values
    states_names = cia_res_query.state_names[cia_res_query.variables[0]]
    
    cia_res = {}
    for state, prob in zip(states_names, probs_cia_res):
        cia_res[state] = float(prob)
    
    return cia_res
    



infer = bayesian_network_construction()
'''
#Obtenemos los valores de CIA_RES (alto, medio, bajo) para obtener un 'impacto'
c_res = infer.query(variables=["C_res"])
print("\nP(C_res):")
print(c_res)
c_res_levels = get_cia_res_levels(c_res)

i_res = infer.query(variables=["I_res"])
print("\nP(I_res):")
print(i_res)
i_res_levels = get_cia_res_levels(i_res)

a_res = infer.query(variables=["A_res"])
print("\nP(A_res):")
print(a_res)
a_res_levels = get_cia_res_levels(a_res)
'''

