#=============================[IMPORTS]===========================================#
import random
import networkx as nx
from pathlib import Path
from tabulate import tabulate

import src.database.load_data as load_data
import src.cyberrecom.mitre as mitre
import src.graph.grafo as grafo
import src.database.create_db as create_db

#=============================[CONSTANTS]===========================================#
DB_PATH = Path(__file__).parent.parent.parent / "tfg_catalog_v1.0.0.db"
EXCEL_PATH = Path(__file__).parent.parent.parent / "asset_catalog_validado_v1.0.0_ajustado.xlsx"

#==============================[MAIN FUNCTION]===========================================#

def main() -> None:
    """
    Función principal: orquesta todo el flujo.
    1. Crear estructura BD
    2. Cargar datos desde Excel
    3. Construir grafo MDO
    4. Cargar TTPs MITRE ATT&CK
    5. Realizar simulaciones de ataque TTP
    """   
    print("\n" + "#"*80)
    print("# Motor de recomendacion de contramedidas en entornos MDO - TFG V1.0.0")
    print("#"*80)
    
    
    # ============ PASO 1: Crear base de datos ============
    print("\n" + "="*80)
    print("PASO 1: CREANDO ESTRUCTURA DE BASE DE DATOS")
    print("="*80)
    if DB_PATH.exists():
        print(f"Base de datos ya existe: {DB_PATH}.")
    else:
        create_db.create_db(DB_PATH, recreate=True)
        print(f"Base de datos creada: {DB_PATH}\n")
    
    
    # ============ PASO 2: Cargar datos desde Excel ============
    print("\n" + "="*80)
    print("PASO 2: CARGAR DATOS DESDE EXCEL")
    print("="*80)
    
    
   # load_data.load_and_insert_data(EXCEL_PATH, DB_PATH)
    
    
    # ============ PASO 3: Construir grafo MDO ============
    print("\n" + "="*80)
    print("PASO 3: CONSTRUIR GRAFO MDO")
    print("="*80)
    
    G_global = grafo.build_MDO_graph(str(DB_PATH))
    
    
    # ============ PASO 4: Simular llegada de una amenaza ============
    print("\n" + "="*80)
    print("PASO 4: SIMULAR LLEGADA DE UNA AMENAZA")
    print("="*80)
    
    random_asset = random.choice(list(G_global.nodes))
    random_threat_vector = mitre.ttp_simulation()
    random_threat_vector['asset'] = random_asset
    
    print(f"\nSimulación de amenaza: TTP={random_threat_vector['ttp_id']}, Confidence={random_threat_vector['confidence']:.2f}, Asset={random_threat_vector['asset']}")
  
    #test
        # ============ PASO 5: Analizar impacto en el grafo MDO ============
    print("\n" + "="*80)
    print("PASO TEST: ANALIZAR IMPACTO EN EL GRAFO MDO")
    print("="*80)
    
    affected_nodes = grafo.get_infected_nodes(G_global, random_threat_vector['asset'])
    
    for level, nodes in affected_nodes.items():
        print(f"Nivel {level}: {nodes}")
    
    
    
    
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
#=================================[ENTRY_POINT]===========================================#    
if __name__ == "__main__":
    main()