#!/usr/bin/env python3
"""
Crea una base de datos SQLite para el TFG con tablas:
- assets
- dependencies

Por defecto se crea la BD en el directorio actual (working directory).

Uso:
  python create_db.py
  python create_db.py --recreate (borra y recrea si ya existe)
  python create_db.py --db otra_ruta.db --recreate (usa otra ruta que se quiera especificar)
"""

#===============================================[IMPORTS]===============================================
import argparse
import sqlite3
from pathlib import Path

#===============================================[DATABASE_SCHEMA]===============================================

# Definición del esquema de la base de datos en lenguaje SQL
DataDefinitionLanguage = """
PRAGMA foreign_keys = ON;

-- Tabla de activos (nodos) con comprobaciones de sus atributos
CREATE TABLE IF NOT EXISTS assets (
  asset_pk          INTEGER PRIMARY KEY AUTOINCREMENT,
  asset_id         TEXT NOT NULL UNIQUE, -- clave estable (slug) referenciable
  name              TEXT NOT NULL,
  asset_type        TEXT NOT NULL,
  domain            TEXT NOT NULL,
  criticality       REAL NOT NULL CHECK (criticality >= 0 AND criticality <= 1),
  cia_c             REAL NOT NULL CHECK (cia_c >= 0 AND cia_c <= 1),
  cia_i             REAL NOT NULL CHECK (cia_i >= 0 AND cia_i <= 1),
  cia_a             REAL NOT NULL CHECK (cia_a >= 0 AND cia_a <= 1),
  operational_state TEXT NOT NULL,
  CHECK (abs((cia_c + cia_i + cia_a) - 1.0) <= 0.01)
);

-- Tabla de dependencias (aristas) con comprobaciones de sus atributos
-- Convención: from_asset = consumidor, to_asset = proveedor
CREATE TABLE IF NOT EXISTS dependencies (
  dep_pk          INTEGER PRIMARY KEY AUTOINCREMENT,
  dependency_id    TEXT NOT NULL UNIQUE, -- clave estable (slug) referenciable
  from_asset        TEXT NOT NULL,
  to_asset          TEXT NOT NULL,
  dependency_type TEXT NOT NULL,
  cia_couple_c    REAL NOT NULL CHECK (cia_couple_c >= 0 AND cia_couple_c <= 1),
  cia_couple_i    REAL NOT NULL CHECK (cia_couple_i >= 0 AND cia_couple_i <= 1),
  cia_couple_a    REAL NOT NULL CHECK (cia_couple_a >= 0 AND cia_couple_a <= 1),
  -- Evita duplicados exactos de la misma relación
  UNIQUE (from_asset, to_asset, dependency_type),
  -- Integridad referencial: solo se permiten keys existentes en assets
  FOREIGN KEY (from_asset) REFERENCES assets(asset_id) ON DELETE CASCADE,
  FOREIGN KEY (to_asset)   REFERENCES assets(asset_id) ON DELETE CASCADE,
  CHECK (from_asset <> to_asset)
);

-- Índices útiles para consultas y construcción de grafo
CREATE INDEX IF NOT EXISTS idx_deps_from_asset ON dependencies(from_asset);
CREATE INDEX IF NOT EXISTS idx_deps_to_asset   ON dependencies(to_asset);
"""

#===============================================[FUNCTIONS]===============================================
def create_db(db_path: Path, recreate: bool) -> None:
    """
    Crea (o recrea) una base de datos SQLite con el esquema definido en DataDefinitionLanguage.
    - db_path: ruta del fichero .db
    - recreate: si True, borra el fichero si existe y lo crea desde cero
    """
    if recreate and db_path.exists():
        db_path.unlink()

    # Se intenta conectar con la base de datos (si no existe, SQLite crea el fichero automáticamente)
    con = sqlite3.connect(db_path)
    try:
        # En SQLite, las FKs se activan por conexión
        con.execute("PRAGMA foreign_keys = ON;")

        # Ejecuta todas las sentencias del DataDefinitionLanguage (múltiples CREATE TABLE/INDEX)
        con.executescript(DataDefinitionLanguage)

        con.commit()
    finally:
        con.close()


#===============================================[MAIN]===============================================
def main() -> None:
    parser = argparse.ArgumentParser(description="Crea la BD SQLite (assets + dependencies).")

    # Por defecto: BD en el directorio actual
    default_db = Path.cwd() / "tfg_catalog_v1.0.0.db"

    parser.add_argument(
        "--db",
        default=str(default_db),
        help=f"Ruta del fichero .db (por defecto: {default_db})",
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Borra y recrea la BD si ya existe",
    )

    args = parser.parse_args()
    create_db(Path(args.db), recreate=args.recreate)
    print(f"OK: BD creada en {args.db}")

#===============================================[ENTRY_POINT]===============================================
if __name__ == "__main__":
    main()
