def main():
    print("Hello from azy-test!")
    print("Hello from azy-test!")
def main2():
    print("Main 2")

if __name__ == "__main__":
    main()
    main2()

    def _transform_state_plane_to_wgs84(df: pd.DataFrame) -> pd.DataFrame:
    
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
