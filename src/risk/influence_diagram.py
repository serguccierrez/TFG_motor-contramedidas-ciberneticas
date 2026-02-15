import red_bayes
import json
from pathlib import Path

def read_constants():
    with open(Path(__file__).parent.parent.parent / "configs" / "constants.json", "r") as f:
        constants = json.load(f)
    return constants

def read_cms():
    with open(Path(__file__).parent.parent.parent / "configs" / "bn_CPDs.json", "r") as f:
        cms = json.load(f)["CM"]["states"]
    return cms


#=============================[CONSTANTS]===========================================#
IMPACT_LEVELS = read_constants()["impact_levels"]
print(f"Constantes de impacto: {IMPACT_LEVELS}")

COUNTERMEASURES = read_cms()
print(f"Countermeasures disponibles: {COUNTERMEASURES}")

#========================================[NUMERIC_IMPACT_CALCULATION]========================================#
def calculate_numeric_impact():
    '''
    Función para calcular un impacto numérico a partir de las probabilidades de los resultados de confidencialidad, integridad y disponibilidad.
    '''
    # Obtener el modelo y el inferidor de la red bayesiana
    infer = red_bayes.bayesian_network_construction()

    #Definimos un diccionario para almacenar los impactos numéricos de cada contramedida
    numeric_impacts = {}

    for cm in COUNTERMEASURES:
        print(f"\nEvaluando impacto para la contramedida: {cm}")
        
        # Obtenemos los valores de CIA_RES (alto, medio, bajo) para obtener un 'impacto'
        c_res = infer.query(variables=["C_res"], evidence={"CM": cm})
        c_res_levels = red_bayes.get_cia_res_levels(c_res)

        i_res = infer.query(variables=["I_res"], evidence={"CM": cm})
        i_res_levels = red_bayes.get_cia_res_levels(i_res)

        a_res = infer.query(variables=["A_res"], evidence={"CM": cm})
        a_res_levels = red_bayes.get_cia_res_levels(a_res)
        
        # Calculamos un impacto numérico ponderando cada nivel de impacto por su probabilidad
        c_res_impact = sum(prob * int(IMPACT_LEVELS[level]) for level, prob in c_res_levels.items())
        numeric_impacts[cm] = {"C_res": c_res_impact}
        print(f"Impacto numérico de C_res: {c_res_impact}")
        i_res_impact = sum(prob * int(IMPACT_LEVELS[level]) for level, prob in i_res_levels.items())
        numeric_impacts[cm]["I_res"] = i_res_impact
        print(f"Impacto numérico de I_res: {i_res_impact}")
        a_res_impact = sum(prob * int(IMPACT_LEVELS[level]) for level, prob in a_res_levels.items())
        numeric_impacts[cm]["A_res"] = a_res_impact
        print(f"Impacto numérico de A_res: {a_res_impact}")
        
    return numeric_impacts
    
h = calculate_numeric_impact()
print("\nImpactos numéricos calculados para cada contramedida:")
print(h)