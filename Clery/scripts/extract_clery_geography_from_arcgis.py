"""
Extract Clery geography feature classes from ArcGIS Pro projects.

Walks Clery project folders, discovers .gdb geodatabases and .aprx projects,
lists feature classes, and exports them to Standards/Clery for institution
geography reference data.

Requires: ArcGIS Pro (arcpy)
Usage: Run from ArcGIS Pro Python or Pro conda environment.
       python extract_clery_geography_from_arcgis.py [--export] [--dry-run]

Author: R. A. Carucci
Date: 2026-03-09
"""

import argparse
import json
import os
from pathlib import Path
import datetime

# Paths
CLERY_PROJECTS_ROOT = Path(
    r"C:\Users\carucci_r\OneDrive - City of Hackensack\10_Projects\Clery\2024"
)
STANDARDS_OUTPUT = Path(__file__).resolve().parent.parent / "DataDictionary" / "current" / "institutions"
INSTITUTION_INDEX = STANDARDS_OUTPUT / "institution_clery_geography_index.json"

# Institution folder names to process
INSTITUTION_FOLDERS = [
    "Bergen Academies",
    "Bergen Community College",
    "Bergen Community College Clery Act",
    "Eastwick College",
    "FDU Clery Act",
    "Parisian",
    "Rutgers",
]


def _get_fc_count(arcpy, fc_path):
    """Get feature count for a feature class."""
    try:
        # Pro 2.9+: arcpy.management.GetCount; older: arcpy.GetCount_management
        get_count = getattr(arcpy.management, "GetCount", None) or getattr(
            arcpy, "GetCount_management", None
        )
        if get_count:
            result = get_count(fc_path)
            return int(result[0])
    except Exception:
        pass
    return None


def get_arcpy():
    """Import arcpy if available. Returns None if ArcGIS Pro not installed."""
    try:
        import arcpy
        return arcpy
    except ImportError:
        return None


def walk_geodatabases(root_path: Path):
    """Find all .gdb folders under root_path."""
    gdbs = []
    for path in root_path.rglob("*"):
        if path.is_dir() and path.suffix.lower() == ".gdb":
            # Skip scratch/scratch.gdb - typically temp
            if "scratch" in path.name.lower():
                continue
            gdbs.append(path)
    return sorted(gdbs)


def list_feature_classes(arcpy, gdb_path: Path):
    """List all feature classes in a geodatabase using arcpy.da.Walk."""
    fc_list = []
    try:
        for dirpath, dirnames, filenames in arcpy.da.Walk(
            str(gdb_path), datatype="FeatureClass"
        ):
            for fc in filenames:
                fc_path = os.path.join(dirpath, fc)
                try:
                    desc = arcpy.Describe(fc_path)
                    fc_list.append({
                        "name": fc,
                        "path": fc_path,
                        "shape_type": desc.shapeType,
                        "spatial_ref": desc.spatialReference.name if desc.spatialReference else None,
                        "feature_count": _get_fc_count(arcpy, fc_path),
                    })
                except Exception as e:
                    fc_list.append({
                        "name": fc,
                        "path": fc_path,
                        "error": str(e),
                    })
    except Exception as e:
        return {"error": str(e), "feature_classes": []}
    return {"feature_classes": fc_list}


def export_to_geojson(arcpy, fc_path: str, output_path: Path):
    """Export a feature class to GeoJSON."""
    try:
        arcpy.conversion.FeaturesToJSON(
            fc_path,
            str(output_path),
            format_json="GEOJSON",
        )
        return True, None
    except Exception as e:
        return False, str(e)


def extract_from_aprx(arcpy, aprx_path: Path):
    """Extract layer data sources from an .aprx project."""
    layers = []
    try:
        aprx = arcpy.mp.ArcGISProject(str(aprx_path))
        for map_obj in aprx.listMaps():
            for layer in map_obj.listLayers():
                if layer.supports("dataSource") and layer.dataSource:
                    layers.append({
                        "map": map_obj.name,
                        "layer_name": layer.name,
                        "data_source": layer.dataSource,
                    })
    except Exception as e:
        return {"error": str(e), "layers": []}
    return {"layers": layers}


def main():
    parser = argparse.ArgumentParser(
        description="Extract Clery geography from ArcGIS Pro projects"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export feature classes to GeoJSON in Standards/Clery",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List only, do not export. Overrides --export.",
    )
    args = parser.parse_args()

    arcpy = get_arcpy()
    if arcpy is None:
        print("ERROR: arcpy not available. Run from ArcGIS Pro Python environment.")
        print("  Options: ArcGIS Pro Python window, or: conda activate arcgispro-py3")
        return 1

    if not CLERY_PROJECTS_ROOT.exists():
        print(f"ERROR: Clery projects root not found: {CLERY_PROJECTS_ROOT}")
        return 1

    # Ensure output directory exists
    STANDARDS_OUTPUT.mkdir(parents=True, exist_ok=True)

    inventory = {
        "timestamp": datetime.datetime.now().isoformat(),
        "source_root": str(CLERY_PROJECTS_ROOT),
        "output_root": str(STANDARDS_OUTPUT),
        "institutions": {},
    }

    for folder_name in INSTITUTION_FOLDERS:
        inst_path = CLERY_PROJECTS_ROOT / folder_name
        if not inst_path.exists():
            inventory["institutions"][folder_name] = {"status": "folder_not_found"}
            continue

        inst_key = folder_name.replace(" ", "_").replace("'", "")
        inst_data = {
            "folder": folder_name,
            "geodatabases": [],
            "aprx_projects": [],
            "feature_classes": [],
            "exported": [],
        }

        # Find geodatabases
        gdbs = walk_geodatabases(inst_path)
        for gdb in gdbs:
            rel = gdb.relative_to(CLERY_PROJECTS_ROOT)
            fc_result = list_feature_classes(arcpy, gdb)
            inst_data["geodatabases"].append({
                "path": str(gdb),
                "relative": str(rel),
            })
            if "error" in fc_result:
                inst_data["geodatabases"][-1]["error"] = fc_result["error"]
            else:
                for fc in fc_result.get("feature_classes", []):
                    fc["gdb"] = str(gdb)
                    inst_data["feature_classes"].append(fc)

                    # Export if requested
                    if args.export and not args.dry_run and "error" not in fc:
                        out_name = f"{inst_key}_{fc['name']}.geojson"
                        out_path = STANDARDS_OUTPUT / out_name
                        ok, err = export_to_geojson(arcpy, fc["path"], out_path)
                        if ok:
                            inst_data["exported"].append(out_name)
                        else:
                            inst_data["exported"].append({"file": out_name, "error": err})

        # Find .aprx projects
        aprx_files = list(inst_path.rglob("*.aprx"))
        for aprx in aprx_files:
            aprx_result = extract_from_aprx(arcpy, aprx)
            inst_data["aprx_projects"].append({
                "path": str(aprx),
                "layers": aprx_result.get("layers", []),
                "error": aprx_result.get("error"),
            })

        inventory["institutions"][folder_name] = inst_data

    # Write inventory
    index_path = INSTITUTION_INDEX
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2)

    # Print summary
    print("=" * 60)
    print("Clery Geography Extraction Summary")
    print("=" * 60)
    print(f"Source: {CLERY_PROJECTS_ROOT}")
    print(f"Output: {STANDARDS_OUTPUT}")
    print(f"Index:  {index_path}")
    print()

    for inst_name, data in inventory["institutions"].items():
        if data.get("status") == "folder_not_found":
            print(f"  {inst_name}: folder not found")
            continue
        gdb_count = len(data.get("geodatabases", []))
        fc_count = len(data.get("feature_classes", []))
        aprx_count = len(data.get("aprx_projects", []))
        exported = len(data.get("exported", []))
        print(f"  {inst_name}:")
        print(f"    Geodatabases: {gdb_count}, Feature classes: {fc_count}")
        print(f"    APRX projects: {aprx_count}")
        if exported:
            print(f"    Exported: {exported} files")
        for fc in data.get("feature_classes", [])[:5]:
            name = fc.get("name", "?")
            shape = fc.get("shape_type", "?")
            count = fc.get("feature_count", "?")
            print(f"      - {name} ({shape}, n={count})")
        if len(data.get("feature_classes", [])) > 5:
            print(f"      ... and {len(data['feature_classes']) - 5} more")
        print()

    if args.dry_run:
        print("(Dry run - no files exported)")
    elif args.export:
        print("Export complete.")

    return 0


if __name__ == "__main__":
    exit(main())
