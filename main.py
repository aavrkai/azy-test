"""
main.py
--------------------
Pipeline for processing the SRFF Raw Crash Data export:
  1. Import CSV (skip the legal disclaimer header row)
  2. Clean Dataset
  - Drop fully empty columns
  - Standardize null values
  - Remove crashes on interstates, ramps, and miscellaneous trafficways
  3. Rename column headers
  - Apply explicit renames for key fields in KAI format
  - Apply snake_case formatting to remaining columns
  4. Standardize date and time formats
  - Convert date to (YYYY-MM-DD)
  - Convert time to HH:MM (24-hour)
  - Create day of week field
  5. Create WA-specific variables
  - Lane departure flag (WA_SHSP_LD)
  - State highway flag (WA_ST_HWY)
  - Weekday flag (WA_WEEKDAY)
  - MV-VRU flag (WA_MV_VRU)
  6. Create binary flags for Fatal and Serious Injury crashes
  - Normalize severity string values
  - Create K_SCREEN (numeric severity)
  - Create K_FSI (Fatal/Serious Injury flag)
  7. Create vehicle-only flags
  - K_SOLOVEH: solo vehicle crash.
  - K_ONLYVEH: crash involving only vehicles (motorcycles count as vehicles).
  8. Clean crash type field (K_TYPE)
  - Normalize and classify crash types into consistent categories
  9. Clean contributing circumstances
  - Normalize contributing circumstance fields (WA_CIRC_1, WA_CIRC_2) into consistent categories
  10. Classify human errors (WA_ERROR, WA_ER_CAT)
  - Assign typical driver errors utilizing rule-based logic on crash type, contributing circumstances, and intersection context
  - Applies geometry based fall-back to handle cases of missing/unknown data
  - Assign Error Categories (Decision, Execution, Violation, Environmental, Vehicle-Related)
  11. Summary and export
  - Print dataset summary and flag distributions
  - Save cleaned dataset to output file. Ready for CrashKIT!
"""

import argparse
import re

import pandas as pd
import numpy as np
from pyproj import Transformer


def to_snake_case(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[/\-–—]", " ", name)
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name.lower()


EXPLICIT_RENAMES = {
    "COUNTY"                                        : "K_COUNTY",
    "CITY"                                          : "K_PLACE",
    "REPORT NUMBER"                                 : "K_ID",
    "PRIMARY TRAFFICWAY"                            : "K_ROAD_NAME",
    "DATE"                                          : "K_DATE",
    "YEAR"                                          : "K_YEAR",
    "MONTH"                                         : "K_MONTH",
    "24 HR TIME"                                    : "K_HOUR",
    "MOST SEVERE INJURY TYPE"                       : "K_SEVERITY",
    "TOTAL VEHICLES"                                : "WA_VEH_CNT",
    "TOTAL PEDESTRIANS INVOLVED"                    : "WA_PED_CNT",
    "TOTAL BICYCLISTS INVOLVED"                     : "WA_BIKE_CNT",
    "FIRST COLLISION TYPE / OBJECT STRUCK"          : "WA_Type",
    "WEATHER"                                       : "K_WEATHER",
    "ROAD SURFACE CONDITIONS"                       : "K_ROADSURF",
    "LIGHTING CONDITIONS"                           : "K_LIGHTING",
    "WA STATE PLANE SOUTH - X"                      : "K_LONG",   # X = easting = longitude
    "WA STATE PLANE SOUTH - Y"                      : "K_LAT",    # Y = northing = latitude
    "TZ Work Zone Related Collision Indicator"      : "K_WRK_ZONE",
    "TZ Pedestrian Involved Indicator"              : "K_PED",
    "TZ Bicyclist Involved Indicator"               : "K_BIKE",
    "TZ MV Driver 65 Plus Years Involved Person Indicator" : "WA_SHSP_OD",
    "TZ Heavy Vehicle Crash Indicator"               : "WA_SHSP_CV",
    "TZ Unlicensed Driver Indicator"                 : "WA_SHSP_DL",
    "TZ Unrestrained Occupant Indicator"             : "WA_SHSP_OP",
    "TZ Wildlife Involved Indicator"                 : "WA_ANIMAL",
    "DIST FROM REF POINT"                            : "WA_DIST_FT",
    "MV Driver 15 To 24 Years Involved Person Indicator" : "WA_SHSP_YD",
    "TZ Wrong Way Vehicle Indicator"                 : "WA_TZ_WW",
    "TZ Speeding Driver Indicator"                   : "WA_SHSP_SP",
    "TZ Drowsy Driver Indicator"                     : "WA_TZ_DO",
    "TZ Non Junction Opposite Direction Crash Indicator" : "WA_TZ_NJ",
    "VEH 1 MV DRIVER CONTRIBUTING CIRCUMSTANCE 1" : "WA_CIRC_1",
    "VEH 2 MV DRIVER CONTRIBUTING CIRCUMSTANCE 1" : "WA_CIRC_2",
    "VEH 1 ACTION"                              : "WA_ACTION",
    "VEH 1 TRAFFIC CONTROL"                     : "K_TRAFFIC_CONTROL",

}

SEVERITY_MAP = {
    "Dead at Scene"            : 1,
    "Died in Hospital"         : 1,
    "Dead on Arrival"          : 1,
    "Fatal Injury"             : 1,
    "Serious Injury"           : 2,
    "Minor Injury"             : 3,
    "Possible Injury"          : 4,
    "No Injury"                : 0,
    "Property Damage Only"     : 0,
    "Unknown"                  : 0,
}

import pandas as pd
def main():
    print("Hello from azy-test!")
    print("Hello from azy-test!")
def main2():
    print("Main 2")

if __name__ == "__main__":
    main()
    main2()

    def _transform_state_plane_to_wgs84(df: pd.DataFrame) -> pd.DataFrame:
        df = pd.Dataframe()
        result = df.copy()
        transformer = Transformer.from_crs("EPSG:2927", "EPSG:4326", always_xy=True)

        if "WA_X" in result.columns and "WA_Y" in result.columns:
            x = pd.to_numeric(result["WA_X"], errors="coerce")
            y = pd.to_numeric(result["WA_Y"], errors="coerce")
            lon, lat = transformer.transform(x, y)
            result["K_LONG"] = lon.round(6)
            result["K_LAT"] = lat.round(6)
        else:
            result["K_LONG"] = pd.Series(pd.NA, index=result.index, dtype="float64")
            result["K_LAT"] = pd.Series(pd.NA, index=result.index, dtype="float64")

        return result
